# Test Case Matrix

| ID | Scenario | Expected result |
|---|---|---|
| TC-01 | Valid record | Pass |
| TC-02 | Multiple valid records | Pass |
| TC-03 | Missing temperature column | Fail with column message |
| TC-04 | Missing humidity column | Fail with column message |
| TC-05 | Empty file | Fail with header message |
| TC-06 | Non-numeric temperature | Fail with data-type message |
| TC-07 | Missing temperature | Fail with data-type message |
| TC-08 | Missing humidity | Fail with data-type message |
| TC-09 | Temperature at -40 C | Pass |
| TC-10 | Temperature at 80 C | Pass |
| TC-11 | Temperature below minimum | Fail |
| TC-12 | Temperature above maximum | Fail |
| TC-13 | Humidity at 0% | Pass |
| TC-14 | Humidity at 100% | Pass |
| TC-15 | Humidity below minimum | Fail |
| TC-16 | Humidity above maximum | Fail |
| TC-17 | Negative elapsed time | Fail |
| TC-18 | Blank record | Fail |
| TC-19 | Multiple defects in one record | Report all detected issues |

The automated test suite is the executable source of truth; this table is a human-readable overview.
