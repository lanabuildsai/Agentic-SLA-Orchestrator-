# Dataset Information

## Source

**Dataset Name:** Customer Support Ticket Dataset  
**Source:** Kaggle  
**URL:** https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset  
**Author:** Suraj Yadav  
**License:** CC0 1.0 Universal (Public Domain)  
**Published:** 2023  
**Downloads:** 15,000+

---

## Dataset Description

This dataset contains 20,000 customer support tickets with the following fields:

| Field Name            | Type     | Description                                    |
|-----------------------|----------|------------------------------------------------|
| Ticket_ID             | String   | Unique identifier for each ticket              |
| Customer              | String   | Customer name                                  |
| Email                 | String   | Customer email address                         |
| Ticket_Subject        | String   | Brief description of the issue                 |
| Ticket_Description    | Text     | Detailed problem statement                     |
| Issue_Category        | Category | Technical, Billing, Account, Fraud, General    |
| Priority_Level        | Category | Low, Medium, High, Critical                    |
| Resolution_Time_Hours | Float    | Time taken to resolve the ticket (hours)       |
| Satisfaction_Score    | Integer  | Customer satisfaction rating (1-5)             |
| Assigned_Agent        | String   | Name of the support agent                      |
| Ticket_Channel        | Category | Email, Chat, Phone, Web                        |
| Submission_Date       | Datetime | When the ticket was created                    |

---

## Enhancements Made

For this project, the original dataset was enhanced with:

1. **SLA Policy Definitions**
   - Critical: 4 hours
   - High: 8 hours
   - Medium: 24 hours
   - Low: 72 hours

2. **Event Timeline Synthesis**
   - Created: ticket submission time
   - Assigned: ~40% through total resolution time
   - In Progress: ~60% through total resolution time
   - Resolved: final timestamp

3. **Risk Calculations**
   - SLA consumption percentage
   - Risk levels (low/medium/high/breached)
   - Intervention candidate flags

4. **Derived Metrics**
   - Remaining SLA hours
   - Urgency scores
   - Event sequences

---

## Usage

To download the dataset:

1. Visit the [Kaggle dataset page](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)
2. Click "Download" (requires Kaggle account)
3. Extract the CSV file to this `data/` directory
4. Rename to `enhanced_customer_support_data.csv` (if different)

**Or use the Kaggle API:**

```bash
pip install kaggle

# Configure Kaggle API credentials
kaggle datasets download -d suraj520/customer-support-ticket-dataset

# Extract
unzip customer-support-ticket-dataset.zip -d data/
```

---

## License & Attribution

This dataset is licensed under **CC0 1.0 Universal (Public Domain)**, which means:

✅ You can copy, modify, and distribute the data  
✅ You can use it for commercial purposes  
✅ No attribution required (but appreciated)

**Suggested Attribution:**
```
Dataset: Customer Support Ticket Dataset by Suraj Yadav
Source: Kaggle (https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)
License: CC0 1.0 Universal (Public Domain)
```

---

## Data Privacy

This is a synthetic/anonymized dataset created for educational and research purposes. No real customer data is included.

---

## Statistics

- **Total Tickets:** 20,000
- **Date Range:** 2023 (synthetic timestamps)
- **File Size:** ~3.2 MB (CSV)
- **Categories:** 5 issue types
- **Priority Levels:** 4 levels
- **Channels:** 4 support channels
- **Agents:** Multiple (anonymized)

---

## Processing Pipeline

```
Raw CSV (20,000 rows)
    ↓
Data Validation & Cleaning
    ↓
SLA Policy Integration
    ↓
Event Timeline Generation (80,000 events)
    ↓
Risk Window Calculation
    ↓
Intervention Candidate Flagging (1,474 candidates)
    ↓
Ready for Orchestration
```

See `notebooks/agentic_sla_orchestrator.ipynb` for the complete data processing pipeline.

---

## Questions?

For questions about the original dataset, visit the [Kaggle discussion page](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/discussion).

For questions about enhancements made in this project, please open a GitHub issue.
