# Events CSV Validator

This Python script validates an `events.csv` file for schema correctness, null values, and column-level type/format checks.  
It is designed in a **class-based modular style** and outputs the results both to the **console** and to a **JSON report file**.

---

## ✅ Features

- **Schema validation**  
  Ensures the CSV file contains the expected columns in the correct order.

- **Row-level validation**

  - Null checks
  - Type/format checks (timestamp, IP address, numeric amount, etc.)
  - Allowed values validation (e.g., `event_type` must be one of `login`, `change_password`, or `payment`)

- **Detailed reporting**
  - Console output with summary and failed row details
  - JSON report written to `validation_report.json` (or a path you specify)

---

## 📊 Expected Schema

The CSV must contain the following columns (in order):

```csv
event_id,timestamp,user_id,ip,country,event_type,amount
```

Example row:

```csv
e123,2024-07-16T14:23:00Z,u_001,192.168.1.1,US,login,0.0
```

---

## 🚀 Usage

### 1. Run validation on a CSV file

```bash
python3 validate_events.py test_data/events.csv
```

```bash
python3 validate_events.py test_data/events_issues.csv
```

### 2. Console Output
<img width="938" height="281" alt="image" src="https://github.com/user-attachments/assets/6f343373-196b-494b-9345-15e1a28c6645" />

### 3. JSON Output

The same report is saved as `validation_report.json`:

```json
{
  "schema_check": "PASSED",
  "checks_performed": [
    "Schema check",
    "Null check",
    "Type/Format check",
    "Allowed values check"
  ],
  "summary": {
    "total_rows": 10,
    "passed_rows": 3,
    "failed_rows": 7
  },
  "failed_details": [
    {
      "row": 4,
      "column": "event_id",
      "invalid_value": "<NULL>"
    },
    {
      "row": 5,
      "column": "user_id",
      "invalid_value": "<NULL>"
    },
    {
      "row": 6,
      "column": "timestamp",
      "invalid_value": "INVALID_DATE"
    },
    {
      "row": 7,
      "column": "ip",
      "invalid_value": "999.999.999.999"
    },
    {
      "row": 8,
      "column": "country",
      "invalid_value": "USA"
    },
    {
      "row": 9,
      "column": "event_type",
      "invalid_value": "withdrawal"
    },
    {
      "row": 10,
      "column": "amount",
      "invalid_value": "abc"
    }
  ]
}
```

---

## ⚙️ Requirements

- Python 3.7+
- Standard library only (no external dependencies)

---

## 📌 Notes

- The script **fails fast** if the schema does not match.
- By default, the JSON report is saved as `validation_report.json` in the same directory.
- You can easily adapt the script to auto-generate filenames (e.g., `events_report.json`) if validating multiple files.

---

## 🏭 Production Use

For production-grade validation and data quality monitoring, consider using libraries like **[Great Expectations](https://greatexpectations.io/)**.  
These tools provide:

- Rich declarative expectations
- Automated validation pipelines
- Integration with databases, cloud storage, and real-time platforms

---

## 📌 Problem Statement (Original)

This was the original problem statement for the **real-time risk scoring platform**:

> Option A: A script that reads `events.csv`, validates schema/types, and outputs a report (pass/fail + row counts).
