#!/usr/bin/env python3
"""
TEST_CASES.py
Unit tests for process_data.py — Datacom Graduate Developer Task 1

These tests were authored to:
1. REPRODUCE the original bug (test_export_json_bug_reproduction)
2. VERIFY the fix works correctly (test_export_json_fixed)
3. Cover additional edge cases for robustness

Run with:
    python -m pytest TEST_CASES.py -v
    OR
    python -m unittest TEST_CASES.py -v
"""

import unittest
import json
import os
import tempfile
import csv
from unittest.mock import patch

# Import the class under test
from process_data_final import DataProcessor


def _make_processor_with_data() -> DataProcessor:
    """Helper: returns a DataProcessor instance pre-loaded with sample data."""
    processor = DataProcessor("dummy.csv")
    # Manually populate customers to avoid needing real CSV files
    processor.customers = {
        "C001": {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "join_date": "2023-01-10",
            "total_spent": 250.75,
            "transaction_count": 3,
        },
        "C002": {
            "name": "Bob Jones",
            "email": "bob@example.com",
            "join_date": "2023-03-22",
            "total_spent": 0.0,
            "transaction_count": 0,
        },
    }
    processor.transactions = [
        {"transaction_id": "T001", "customer_id": "C001", "amount": 100.0, "date": "2024-01-01", "category": "Electronics"},
        {"transaction_id": "T002", "customer_id": "C001", "amount": 50.75, "date": "2024-01-02", "category": "Clothing"},
        {"transaction_id": "T003", "customer_id": "C001", "amount": 100.0, "date": "2024-01-03", "category": "Electronics"},
    ]
    return processor


class TestExportCustomerDataBugReproduction(unittest.TestCase):
    """
    Tests that REPRODUCE the original bug described in error.log:
    'dict' object has no attribute 'keys'

    The bug occurred at:
        2024-01-15 02:30:16,234 - ERROR - Error exporting data: 'dict' object has no attribute 'keys'

    Root cause: export_customer_data() in the JSON branch did not handle
    non-serialisable types (floats stored as strings, nested objects, etc.)
    and lacked a guard for empty customers dict in CSV branch.
    """

    def test_export_json_does_not_raise_attribute_error(self):
        """
        Bug reproduction test: exporting to JSON should NOT raise
        'dict object has no attribute keys'.
        This test would FAIL on the original buggy code.
        """
        processor = _make_processor_with_data()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            tmp_path = f.name
        try:
            result = processor.export_customer_data(tmp_path, format="json")
            self.assertTrue(result, "export_customer_data should return True on success")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_export_json_produces_valid_json(self):
        """The exported JSON file should be parseable and contain correct data."""
        processor = _make_processor_with_data()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            tmp_path = f.name
        try:
            processor.export_customer_data(tmp_path, format="json")
            with open(tmp_path, "r") as f:
                data = json.load(f)
            self.assertIn("C001", data)
            self.assertIn("C002", data)
            self.assertEqual(data["C001"]["name"], "Alice Smith")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_export_csv_produces_correct_rows(self):
        """CSV export should write a header and one row per customer."""
        processor = _make_processor_with_data()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", newline="") as f:
            tmp_path = f.name
        try:
            result = processor.export_customer_data(tmp_path, format="csv")
            self.assertTrue(result)
            with open(tmp_path, "r") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertEqual(len(rows), 2)
            customer_ids = {row["customer_id"] for row in rows}
            self.assertIn("C001", customer_ids)
            self.assertIn("C002", customer_ids)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_export_empty_customers_returns_false(self):
        """Exporting when no customers are loaded should return False gracefully."""
        processor = DataProcessor("dummy.csv")
        # customers is empty by default
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            tmp_path = f.name
        try:
            result = processor.export_customer_data(tmp_path, format="json")
            self.assertFalse(result, "Should return False when customers dict is empty")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_export_unsupported_format_returns_false(self):
        """Unsupported format should return False without raising."""
        processor = _make_processor_with_data()
        result = processor.export_customer_data("output.xml", format="xml")
        self.assertFalse(result)


class TestCalculateCustomerMetrics(unittest.TestCase):
    """Tests for calculate_customer_metrics()."""

    def test_metrics_total_revenue(self):
        """Total revenue should equal sum of all customer total_spent."""
        processor = _make_processor_with_data()
        metrics = processor.calculate_customer_metrics()
        self.assertAlmostEqual(metrics["total_revenue"], 250.75)

    def test_metrics_average_transaction_value(self):
        """Average transaction value = total_revenue / total_transactions."""
        processor = _make_processor_with_data()
        metrics = processor.calculate_customer_metrics()
        expected_avg = 250.75 / 3
        self.assertAlmostEqual(metrics["average_transaction_value"], expected_avg, places=2)

    def test_metrics_category_breakdown(self):
        """Category breakdown should count transactions per category."""
        processor = _make_processor_with_data()
        metrics = processor.calculate_customer_metrics()
        self.assertEqual(metrics["category_breakdown"]["Electronics"], 2)
        self.assertEqual(metrics["category_breakdown"]["Clothing"], 1)

    def test_metrics_empty_customers_returns_empty_dict(self):
        """With no customers, metrics should return an empty dict."""
        processor = DataProcessor("dummy.csv")
        metrics = processor.calculate_customer_metrics()
        self.assertEqual(metrics, {})

    def test_metrics_top_customers_sorted(self):
        """Top customers should be sorted by total_spent descending."""
        processor = _make_processor_with_data()
        metrics = processor.calculate_customer_metrics()
        top = metrics["top_customers"]
        self.assertEqual(top[0][0], "C001")  # Alice has highest spend
        self.assertEqual(top[1][0], "C002")


class TestFindMatches(unittest.TestCase):
    """Tests for find_matches() — refactored from O(n^2) to dictionary lookup."""

    def test_find_by_name_returns_match(self):
        processor = _make_processor_with_data()
        results = processor.find_matches("alice", field="name")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["customer_id"], "C001")

    def test_find_by_name_case_insensitive(self):
        processor = _make_processor_with_data()
        results = processor.find_matches("ALICE", field="name")
        self.assertEqual(len(results), 1)

    def test_find_no_match_returns_empty(self):
        processor = _make_processor_with_data()
        results = processor.find_matches("zzznotexist", field="name")
        self.assertEqual(results, [])

    def test_find_partial_match(self):
        """Partial substring match should work."""
        processor = _make_processor_with_data()
        results = processor.find_matches("smi", field="name")  # matches "Smith"
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alice Smith")

    def test_find_by_email(self):
        processor = _make_processor_with_data()
        results = processor.find_matches("bob@", field="email")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["customer_id"], "C002")


class TestGenerateReport(unittest.TestCase):
    """Tests for generate_report()."""

    def test_generate_metrics_report(self):
        processor = _make_processor_with_data()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            tmp_path = f.name
        try:
            result = processor.generate_report("metrics", tmp_path)
            self.assertTrue(result)
            with open(tmp_path) as f:
                data = json.load(f)
            self.assertIn("metrics", data)
            self.assertIn("generated_at", data)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_generate_unknown_report_type_returns_false(self):
        processor = _make_processor_with_data()
        result = processor.generate_report("nonexistent_type", "out.json")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
