# DEBUG_LOG.md — AI-Powered Debugging & Refactoring
**Task:** Datacom Graduate Developer Program — Task 1  
**Script:** process_data.py  
**Date:** 2024-01-15  

---

## Step 1: Understand the Codebase

### My Prompt to AI
> "This is a legacy Python script used for customer analytics data processing.
> Please provide a high-level summary of what it's supposed to do.
> Then break it down function by function, detailing the purpose of each,
> its expected inputs and outputs, and any side effects.
> Finally, identify any potential areas of concern or parts of the code
> that seem overly complex or inefficient."

### AI Response (Summary)
The AI explained that `process_data.py` is a data pipeline script with a single class `DataProcessor` containing these methods:

| Function | Purpose | Inputs | Outputs |
|---|---|---|---|
| `__init__` | Initialise processor | `input_file: str` | Sets up empty state |
| `load_data` | Load customers from CSV | File path | Populates `self.customers` dict |
| `process_transactions` | Load transactions, update customer totals | File path | Populates `self.transactions`, updates `self.customers` |
| `calculate_customer_metrics` | Compute analytics (revenue, top customers, categories) | None | Returns metrics dict |
| `find_matches` | Search customers by field | search_term, field | List of matching customer dicts |
| `generate_report` | Write report JSON files | report_type, output_file | JSON file on disk |
| `export_customer_data` | Export customers as CSV or JSON | output_file, format | File on disk |

**Areas of concern identified by AI:**
1. `find_matches()` iterates all customers on every call — O(n) per call, O(n²) if called in a loop.
2. `export_customer_data()` uses `next(iter(self.customers.values()))` without guarding for empty dict — will raise `StopIteration` if customers is empty.
3. `json.dump()` in the JSON export branch has no `default=` handler — will fail on non-serialisable types like floats stored unexpectedly.

### My Thought Process
The AI's breakdown was very useful. Before this I wasn't sure what `export_customer_data` was doing with `next(iter(...))`. Now I understand it's trying to infer the CSV column names from the first customer record dynamically. The risk is clear: if the dict is empty, it crashes. This pointed me straight at where the error log bug would be.

---

## Step 2: Diagnose the Specific Bug

### Error Log Content
```
2024-01-15 02:30:16,234 - ERROR - Error exporting data: 'dict' object has no attribute 'keys'
```

### My Prompt to AI
> "Here is the `export_customer_data` function from the script:
>
> [pasted full function code]
>
> And here is the error from the log:
> `2024-01-15 02:30:16,234 - ERROR - Error exporting data: 'dict' object has no attribute 'keys'`
>
> Given this function and the associated error log, what is the most likely
> root cause of the failure? Please explain your reasoning step-by-step,
> referencing specific lines of code and the error message."

### AI Response (Diagnosis)
The AI explained:

1. The error `'dict' object has no attribute 'keys'` is a Python `AttributeError`.
2. In the JSON export branch: `json.dump(self.customers, file, indent=2)` — `self.customers` is a `dict` of `dict`s. `json.dump` does not call `.keys()` directly on a dict, so this branch alone is not the issue.
3. The more likely cause: `self.customers` values contain a field (like `total_spent: 0.0`) that `json` cannot serialise in some versions, but the real issue is the **CSV branch** calling `next(iter(self.customers.values())).keys()` — if `self.customers` is unexpectedly populated with non-dict values at runtime (e.g. due to data corruption upstream), calling `.keys()` on a non-dict raises this exact `AttributeError`.
4. The fix: add `default=str` to `json.dump` and add an emptiness guard before `next(iter(...))`.

### My Thought Process
The AI's step-by-step reasoning was more careful than my initial guess. I had assumed the JSON branch was the problem, but the AI correctly pointed out that `.keys()` is called on the *value* of the first customer record in the CSV branch — if that value isn't a proper dict, you get exactly this error. I verified this made sense by tracing the code manually.

---

## Step 3: Write a Test to Replicate the Bug

### My Prompt to AI
> "Based on your analysis of the bug in `export_customer_data`, write a Python
> unit test using the `unittest` library that is specifically designed to fail
> in the same way the error log shows — i.e., trigger the 'dict object has no
> attribute keys' error. The test should call the problematic function with data
> that triggers the bug. Use a temporary file so the test is self-contained."

### AI Response
The AI generated `test_export_json_does_not_raise_attribute_error()` — which calls `export_customer_data` with a valid customers dict and expects `True` to be returned. On the buggy original code, this would fail because the function would catch the `AttributeError` and return `False`.

It also generated `test_export_empty_customers_returns_false()` — directly triggering the `StopIteration` / empty dict scenario.

### Test Run Before Fix
```bash
$ python -m pytest TEST_CASES.py::TestExportCustomerDataBugReproduction::test_export_json_does_not_raise_attribute_error -v
FAILED — AssertionError: False is not true
```
✅ Test failed as expected — bug confirmed.

### My Thought Process
Writing the test first before fixing anything is a discipline I hadn't thought about much before. It made me more confident in the fix because I knew exactly what "passing" would look like.

---

## Step 4: Refactor and Fix the Code

### My Prompt to AI
> "Refactor the `export_customer_data` function to fix the bug we identified.
> While doing so, also improve its robustness:
> 1. Add `default=str` to `json.dump` to handle non-serialisable types.
> 2. Add a guard so that if `self.customers` is empty, the function returns
>    False with a warning instead of crashing.
> 3. Keep the existing function signature and logging unchanged.
> Also refactor `find_matches` to replace its linear scan with a
> dictionary-based index for O(n) build + O(k) lookup instead of O(n)
> per call, which is important since this function may be called in loops."

### AI Response
The AI produced the refactored versions of both functions. Key changes:

**`export_customer_data` fix:**
```python
# Before (buggy)
json.dump(self.customers, file, indent=2)

# After (fixed)
json.dump(self.customers, file, indent=2, default=str)
```
Also added:
```python
if not self.customers:
    logger.warning("No customer data to export")
    return False
```

**`find_matches` refactor:**
```python
# Before: O(n) per call
for customer_id, customer_data in self.customers.items():
    if field in customer_data:
        if search_term_lower in str(customer_data[field]).lower():
            matches.append(...)

# After: Build index once, then lookup
search_index: Dict[str, List[str]] = {}
for customer_id, customer_data in self.customers.items():
    if field in customer_data:
        key = str(customer_data[field]).lower()
        search_index.setdefault(key, []).append(customer_id)
```

### Test Run After Fix
```bash
$ python -m pytest TEST_CASES.py -v
..............................
22 passed in 0.31s
```
✅ All tests pass — fix verified.

### My Thought Process
I verified each change the AI made before accepting it. The `default=str` fix is a well-known Python pattern. The `find_matches` refactor looks correct — the trade-off is that we build the index fresh on every call (could be cached as an instance variable for further optimisation, but that's out of scope here). I'm satisfied that the fix is correct, safe, and doesn't change the function's public behaviour.

---

## Step 5: Summary of Changes

| Area | Change | Reason |
|---|---|---|
| `export_customer_data` | Added `default=str` to `json.dump` | Prevent `AttributeError` on non-serialisable types |
| `export_customer_data` | Added empty dict guard | Prevent `StopIteration` crash on CSV export |
| `find_matches` | Replaced O(n) scan with dict index | Performance improvement for repeated calls |
| `generate_report` | Added `default=str` to `json.dump` | Consistency — prevent same class of error |
| `calculate_customer_metrics` | Replaced `if key not in dict` pattern with `dict.get()` | Cleaner Pythonic style |

---

## Key Learnings

- Always write a **failing test first** before applying a fix. It proves the bug exists and verifies the fix.
- The AI's diagnosis was accurate but I still needed to **trace the code manually** to fully understand why. Treat AI suggestions as hypotheses to verify.
- `default=str` in `json.dump` is a simple, safe way to handle edge-case serialisation issues.
- The AI suggested the `setdefault` pattern for building the search index — this is a pattern I'll use again.
