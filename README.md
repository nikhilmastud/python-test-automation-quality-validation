# Python-Based Test Automation & Quality Validation

A QA-focused project using `pytest` to test CSV sensor data for required columns, numeric fields, and acceptable value ranges. It includes positive and negative test cases with readable pass/fail output.

## Skills demonstrated
- Test case design and boundary-value testing
- Negative testing for invalid or missing data
- CSV/data validation
- Defect messages and repeatable automated tests

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows Git Bash:
source .venv/Scripts/activate
# Windows Command Prompt instead: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run tests
From the repository root:

```bash
python -m pytest -v
```

Tests use temporary CSV files, so no Arduino hardware is required. `sample_data/` contains illustrative example inputs. Parameterized tests create more than 12 test scenarios; the exact count can change as tests are extended.

## Scope
This is a learning/portfolio project, not a claim of industrial certification or production-grade coverage. The dataset validator can be used with CSV output from the companion Smart Environmental Monitoring project.
