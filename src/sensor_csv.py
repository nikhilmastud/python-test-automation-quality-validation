"""CSV validation functions used by the automated test suite."""
import csv
from pathlib import Path

REQUIRED_COLUMNS = {"elapsed_ms", "temperature_c", "humidity_pct"}


def validate_sensor_csv(path: Path) -> list[str]:
    """Return validation issues; an empty list means the file passed."""
    issues = []
    try:
        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                return ["File is empty or has no header"]
            missing = REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing:
                return [f"Missing required columns: {', '.join(sorted(missing))}"]
            for line_number, row in enumerate(reader, start=2):
                if not any((value or "").strip() for value in row.values()):
                    issues.append(f"Line {line_number}: blank record")
                    continue
                try:
                    elapsed = float(row["elapsed_ms"])
                    temperature = float(row["temperature_c"])
                    humidity = float(row["humidity_pct"])
                except (TypeError, ValueError):
                    issues.append(f"Line {line_number}: non-numeric or missing value")
                    continue
                if elapsed < 0:
                    issues.append(f"Line {line_number}: elapsed_ms must be >= 0")
                if not -40 <= temperature <= 80:
                    issues.append(f"Line {line_number}: temperature outside -40 to 80 C")
                if not 0 <= humidity <= 100:
                    issues.append(f"Line {line_number}: humidity outside 0 to 100%")
    except UnicodeDecodeError:
        return ["File is not valid UTF-8 text"]
    return issues
