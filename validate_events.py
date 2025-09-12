#!/usr/bin/env python3
"""
Validation script for events.csv
- Class-based modular design
- Validates schema, nulls, and column types
- Generates a summary report
- Prints to console AND writes schema check + validation report to a JSON file
"""

import csv
import sys
import ipaddress
import json
from datetime import datetime
from pathlib import Path


class EventsValidator:
    EXPECTED_COLUMNS = [
        "event_id",
        "timestamp",
        "user_id",
        "ip",
        "country",
        "event_type",
        "amount",
    ]

    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.total_rows = 0
        self.passed_rows = 0
        self.failed_rows = 0
        self.failed_details = []
        self.schema_ok = False

    # ---------- Column Validators ----------
    def validate_event_id(self, val: str) -> bool:
        return val.startswith("e") and len(val) > 1

    def validate_timestamp(self, val: str) -> bool:
        try:
            datetime.fromisoformat(val.replace("Z", "+00:00"))
            return True
        except Exception:
            return False

    def validate_user_id(self, val: str) -> bool:
        return val.startswith("u_") and len(val) > 2

    def validate_ip(self, val: str) -> bool:
        try:
            ipaddress.ip_address(val)
            return True
        except ValueError:
            return False

    def validate_country(self, val: str) -> bool:
        return len(val) == 2 and val.isalpha()

    def validate_event_type(self, val: str) -> bool:
        return val in {"login", "change_password", "payment"}

    def validate_amount(self, val: str) -> bool:
        try:
            float(val)
            return True
        except ValueError:
            return False

    # ---------- Helper for null check ----------
    def check_null(self, value: str, row_num: int, col_name: str) -> bool:
        """Return False if value is empty/null, log failure details"""
        if value.strip() == "":
            self.failed_details.append((row_num, col_name, "<NULL>"))
            return False
        return True

    # ---------- Main run ----------
    def run(self):
        with open(self.csv_file, newline="") as f:
            reader = csv.reader(f)
            header = next(reader)

            # Validate schema
            if header == self.EXPECTED_COLUMNS:
                self.schema_ok = True
                print("Schema check PASSED (expected columns match)")
            else:
                raise ValueError(
                    f"Schema check FAILED!\nExpected: {self.EXPECTED_COLUMNS}\nFound: {header}"
                )

            validators = [
                self.validate_event_id,
                self.validate_timestamp,
                self.validate_user_id,
                self.validate_ip,
                self.validate_country,
                self.validate_event_type,
                self.validate_amount,
            ]

            for row in reader:
                self.total_rows += 1
                row_ok = True

                for i, validator in enumerate(validators):
                    col_name = self.EXPECTED_COLUMNS[i]
                    value = row[i].strip()

                    # First: null check
                    if not self.check_null(value, self.total_rows, col_name):
                        row_ok = False
                        continue

                    # Then: type-specific check
                    if not validator(value):
                        row_ok = False
                        self.failed_details.append(
                            (self.total_rows, col_name, value)
                        )

                if row_ok:
                    self.passed_rows += 1
                else:
                    self.failed_rows += 1

    # ---------- Reporting ----------
    def report(self, json_file="validation_report.json"):
        report_data = {
            "schema_check": "PASSED" if self.schema_ok else "FAILED",
            "checks_performed": [
                "Schema check",
                "Null check",
                "Type/Format check",
                "Allowed values check",
            ],
            "summary": {
                "total_rows": self.total_rows,
                "passed_rows": self.passed_rows,
                "failed_rows": self.failed_rows,
            },
            "failed_details": [
                {"row": r, "column": col, "invalid_value": val}
                for r, col, val in self.failed_details
            ],
        }

        # Print to console
        print("\n--- Validation Report ---")
        print(
            "Checks performed: [Schema check, Null check, Type/Format check, Allowed values check]"
        )

        if self.failed_rows > 0:
            print(
                f"Row-level validation FAILED ({self.failed_rows} issues found)")
        else:
            print("All rows PASSED row-level validation")

        print(f"Total rows   : {self.total_rows}")
        print(f"Passed rows  : {self.passed_rows}")
        print(f"Failed rows  : {self.failed_rows}")

        if self.failed_rows > 0:
            print("\nFailed details:")
            for r, col, val in self.failed_details:
                print(f"  Row {r}: Column '{col}' invalid value '{val}'")

        # Save JSON
        with open(json_file, "w") as jf:
            json.dump(report_data, jf, indent=4)

        print(
            f"\nValidation report also written to {Path(json_file).resolve()}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_events.py events.csv")
        sys.exit(1)

    csv_file = sys.argv[1]
    validator = EventsValidator(csv_file)
    validator.run()
    validator.report()


if __name__ == "__main__":
    main()
