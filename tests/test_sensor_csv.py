import csv
import pytest
from src.sensor_csv import validate_sensor_csv

VALID_HEADER = ["elapsed_ms", "temperature_c", "humidity_pct"]


def write_csv(tmp_path, header, rows):
    path = tmp_path / "sensor.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
    return path


def test_valid_record_passes(tmp_path):
    assert validate_sensor_csv(write_csv(tmp_path, VALID_HEADER, [[0, 24.5, 45]])) == []


def test_multiple_valid_records_pass(tmp_path):
    path = write_csv(tmp_path, VALID_HEADER, [[0, 24, 45], [2000, 25, 46], [4000, 26, 47]])
    assert validate_sensor_csv(path) == []


def test_missing_temperature_column_fails(tmp_path):
    path = write_csv(tmp_path, ["elapsed_ms", "humidity_pct"], [[0, 45]])
    assert "Missing required columns: temperature_c" in validate_sensor_csv(path)[0]


def test_missing_humidity_column_fails(tmp_path):
    path = write_csv(tmp_path, ["elapsed_ms", "temperature_c"], [[0, 24]])
    assert "Missing required columns: humidity_pct" in validate_sensor_csv(path)[0]


def test_empty_file_fails(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    assert validate_sensor_csv(path) == ["File is empty or has no header"]


def test_non_numeric_temperature_fails(tmp_path):
    path = write_csv(tmp_path, VALID_HEADER, [[0, "warm", 45]])
    assert any("non-numeric or missing" in issue for issue in validate_sensor_csv(path))


def test_missing_temperature_fails(tmp_path):
    path = write_csv(tmp_path, VALID_HEADER, [[0, "", 45]])
    assert any("non-numeric or missing" in issue for issue in validate_sensor_csv(path))


def test_missing_humidity_fails(tmp_path):
    path = write_csv(tmp_path, VALID_HEADER, [[0, 24, ""]])
    assert any("non-numeric or missing" in issue for issue in validate_sensor_csv(path))

@pytest.mark.parametrize("temperature", [-40, 0, 24.5, 80])
def test_temperature_boundaries_pass(tmp_path, temperature):
    assert validate_sensor_csv(write_csv(tmp_path, VALID_HEADER, [[0, temperature, 45]])) == []

@pytest.mark.parametrize("temperature", [-40.1, 80.1])
def test_temperature_out_of_range_fails(tmp_path, temperature):
    assert any("temperature outside" in issue for issue in validate_sensor_csv(write_csv(tmp_path, VALID_HEADER, [[0, temperature, 45]])))

@pytest.mark.parametrize("humidity", [0, 45, 100])
def test_humidity_boundaries_pass(tmp_path, humidity):
    assert validate_sensor_csv(write_csv(tmp_path, VALID_HEADER, [[0, 24.5, humidity]])) == []

@pytest.mark.parametrize("humidity", [-0.1, 100.1])
def test_humidity_out_of_range_fails(tmp_path, humidity):
    assert any("humidity outside" in issue for issue in validate_sensor_csv(write_csv(tmp_path, VALID_HEADER, [[0, 24.5, humidity]])))


def test_negative_elapsed_time_fails(tmp_path):
    assert any("elapsed_ms must be >= 0" in issue for issue in validate_sensor_csv(write_csv(tmp_path, VALID_HEADER, [[-1, 24.5, 45]])))


def test_blank_record_is_reported(tmp_path):
    assert any("blank record" in issue for issue in validate_sensor_csv(write_csv(tmp_path, VALID_HEADER, [["", "", ""]])))


def test_multiple_defects_are_reported(tmp_path):
    issues = validate_sensor_csv(write_csv(tmp_path, VALID_HEADER, [[-1, 99, 101]]))
    assert len(issues) == 3
