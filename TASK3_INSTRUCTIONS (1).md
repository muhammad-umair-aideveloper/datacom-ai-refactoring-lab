# Task 3: Automating Business Analysis with Agentic AI

## Scenario

Congratulations on shipping the Kudos feature! The Head of Operations is overwhelmed by a manual process for handling new customer hardware orders and has asked your team for help. Your task is to analyse their workflow and propose an AI-driven automation solution.

## Learning Objectives

- The core principles that define an agentic AI system: autonomy, adaptability, goal-focus, and learning capability
- How to perform basic business process analysis to map workflows and identify inefficiencies
- How to design conceptual agentic workflows, defining an agent's goals, tools, and decision-making logic
- The crucial skill of communicating complex technical automation proposals to non-technical stakeholders

## Deliverables

A 3-slide presentation file (PowerPoint or Google Slides) that outlines:

1. Analysis of the current process
2. Design of the proposed agentic AI solution
3. Expected business impact and next steps

## The Manual Process

The current order processing workflow involves these steps:

1. **Email Reception**: A sales rep emails a PDF order form to a shared inbox
2. **Manual Reading**: An ops team member manually reads the PDF
3. **Account Verification**: They manually check the customer's account status in Salesforce
4. **Inventory Check**: They manually check inventory in a Google Sheet
5. **Decision Point**:
   - If everything is okay: They manually draft and send two emails (one to the customer, one to the warehouse)
   - If there's a problem: They email the sales rep, leading to long delays

## Step-by-Step Instructions

### Step 1: Analyse and Map the Current Process

1. Create a simple flowchart that maps the current manual process
2. Highlight the systems involved (Email, Salesforce, Google Sheets) and key decision points
3. Use this to identify bottlenecks and points of failure
4. Consider questions like:
   - How long does each step typically take?
   - What are the most common failure points?
   - What happens when staff are unavailable?
   - How many orders are processed per day/week?

### Step 2: Design the Agentic AI Solution

Design an autonomous AI agent, which we'll call 'OrderBot,' to handle this entire workflow. You are not coding this agent, but designing it conceptually.

Refer to the 'Anatomy of a Business Process Agent' table below to structure your thinking:

- What is its goal?
- What 'tools' (APIs) does it need?
- What decisions must it make?
- How does it handle exceptions?

### Step 3: Create Your Presentation for Management

Prepare a concise, professional 3-slide presentation for a non-technical audience.

#### Slide 1: The Problem - Our Current Order Process Is a Bottleneck

- Show your flowchart of the manual process
- Highlight the pain points (manual entry, delays, errors)
- Include key metrics if available (processing time, error rates, etc.)

#### Slide 2: The Solution - Introducing 'OrderBot,' Our Autonomous AI Agent

- Introduce your proposed agent
- Display a new, streamlined flowchart showing how OrderBot automates the process
- Explain how it works in simple, business-friendly terms
- Highlight the key benefits (speed, accuracy, 24/7 availability)

#### Slide 3: The Business Impact & Recommended Next Steps

- Outline the tangible business benefits:
  - Reduced processing time (from hours to minutes)
  - Eliminated manual errors
  - Freed-up staff time for higher-value work
  - Improved customer satisfaction
- Propose a clear, low-risk next step: a 'read-only' Proof of Concept to validate accuracy before full rollout

## Anatomy of a Business Process Agent

| Component              | Description                                                                                                     | Example Application for "OrderBot"                                                                                                                                                                                             |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Goal**               | The primary, high-level, and measurable objective that the agent is programmed to achieve.                      | To autonomously process all new hardware orders from email receipt to fulfillment confirmation within 5 minutes, with a target accuracy of 99.5%.                                                                              |
| **Perception (Tools)** | The set of tools and integrations that allow the agent to sense its digital environment and gather information. | • Email Reader Tool: Connects to the inbox API<br>• PDF Parsing Tool: Extracts structured data from attachments<br>• Salesforce API Tool: Queries customer records<br>• Google Sheets API Tool: Reads current inventory levels |
| **Planning**           | The agent's internal ability to break down its high-level goal into a dynamic sequence of steps.                | 1. New email detected<br>2. Parse PDF<br>3. Query Salesforce<br>4. Query Google Sheets<br>5. Decision: Analyse results and formulate a "success" or "exception" plan<br>6. Execute the chosen plan                             |
| **Action (Tools)**     | The set of tools the agent uses to act upon its digital environment and execute its plan.                       | • Email Sender Tool: Sends confirmation, fulfillment, or query emails<br>• Salesforce API Tool: Updates the customer's order history<br>• Google Sheets API Tool: Decrements the inventory count                               |
| **Memory / Learning**  | The capability of the agent to retain information from past interactions to improve its future performance.     | The agent logs every order outcome. Over time, it could learn to identify patterns, such as which sales reps frequently submit incomplete forms, and flag those for human review.                                              |

## Design Considerations

### Technical Architecture

- **Email Integration**: How will OrderBot monitor the inbox?
- **PDF Processing**: What tools will extract data from order forms?
- **API Connections**: How will it connect to Salesforce and Google Sheets?
- **Decision Logic**: What rules will determine success vs. exception handling?

### Risk Mitigation

- **Human Oversight**: Where should humans still be involved?
- **Error Handling**: What happens when the agent encounters unexpected situations?
- **Fallback Procedures**: How does the system handle technical failures?

### Business Impact Metrics

- **Processing Time**: Reduction from hours to minutes
- **Accuracy**: Target 99.5% success rate
- **Cost Savings**: Staff time freed up for higher-value work
- **Customer Satisfaction**: Faster order confirmation and fulfillment

## Presentation Guidelines

### Design Principles

- Keep it simple and visual
- Use business language, not technical jargon
- Focus on benefits, not features
- Include concrete examples and metrics
- Make the next steps clear and actionable

### Content Structure

1. **Problem Slide**: Current state with pain points clearly highlighted
2. **Solution Slide**: Proposed automation with clear benefits
3. **Impact Slide**: Quantified benefits and clear next steps

### Visual Elements

- Use flowcharts to show before/after processes
- Include icons or simple graphics to illustrate concepts
- Use color coding to highlight problems (red) and solutions (green)
- Keep text minimal - use bullet points and key phrases

## Reflection Questions

After completing the task, consider:

1. **What are the biggest risks or potential failure points in the agentic solution you designed?**

2. **In this fully automated workflow, where is human oversight still absolutely critical, and why?**

3. **How has this programme's progression—from AI-assisted coding to architecting autonomous systems—changed your view of a software developer's role and responsibilities in a modern, AI-driven business?**

## Tips for Success

- Focus on the business value, not the technical complexity
- Use concrete examples and metrics when possible
- Consider the human element - how does this affect the team?
- Think about scalability and future growth
- Be realistic about implementation challenges and timeline

This capstone task elevates your thinking from engineering a single software feature to designing an autonomous system that solves a broader business problem. You're no longer just a developer - you're a strategic technology partner.
