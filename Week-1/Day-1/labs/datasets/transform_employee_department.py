import csv
from pathlib import Path
from typing import Dict


DATASET_DIR = Path(__file__).resolve().parent
DEPARTMENTS_CSV = DATASET_DIR / "departments.csv"
EMPLOYEES_CSV = DATASET_DIR / "employees.csv"
OUTPUT_CSV = DATASET_DIR / "employees_with_department.csv"


def load_departments_by_id(path: Path) -> Dict[str, Dict[str, str]]:
    departments: Dict[str, Dict[str, str]] = {}
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dept_id = (row.get("department_id") or "").strip()
            if not dept_id:
                continue
            departments[dept_id] = {k: (v or "").strip() for k, v in row.items()}
    return departments


def transform_employees_with_department(
    employees_path: Path,
    departments_by_id: Dict[str, Dict[str, str]],
    output_path: Path,
) -> int:
    with employees_path.open("r", newline="", encoding="utf-8") as fin:
        reader = csv.DictReader(fin)
        employee_fieldnames = list(reader.fieldnames or [])

        out_fieldnames = employee_fieldnames.copy()
        if "department_name" not in out_fieldnames:
            out_fieldnames.insert(out_fieldnames.index("department_id") + 1, "department_name")

        with output_path.open("w", newline="", encoding="utf-8") as fout:
            writer = csv.DictWriter(fout, fieldnames=out_fieldnames)
            writer.writeheader()

            count = 0
            for emp in reader:
                dept_id = (emp.get("department_id") or "").strip()
                dept = departments_by_id.get(dept_id, {})
                emp_out = {k: (v or "").strip() for k, v in emp.items()}
                emp_out["department_name"] = dept.get("department_name", "Unknown")
                writer.writerow(emp_out)
                count += 1

    return count


def main() -> None:
    if not DEPARTMENTS_CSV.exists():
        raise FileNotFoundError(f"Missing departments dataset: {DEPARTMENTS_CSV}")
    if not EMPLOYEES_CSV.exists():
        raise FileNotFoundError(f"Missing employees dataset: {EMPLOYEES_CSV}")

    departments_by_id = load_departments_by_id(DEPARTMENTS_CSV)
    rows = transform_employees_with_department(EMPLOYEES_CSV, departments_by_id, OUTPUT_CSV)

    print(f"Wrote {rows} rows to: {OUTPUT_CSV}")
    print("Preview (employee_id, full_name, department_name):")

    with OUTPUT_CSV.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            full_name = f"{row.get('first_name','').strip()} {row.get('last_name','').strip()}".strip()
            print(f"- {row.get('employee_id')} | {full_name} | {row.get('department_name')}")
            if i >= 7:
                break


if __name__ == "__main__":
    main()

