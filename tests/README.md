## Unit Tests

## Installation
Install pytest
```
pip install pytest
```

## Environment
Source the environment file at top level of repo
```
source env.sh
```
Note: If any errors occur (ModuleNotFoundError), remember this step!

## Run tests
Run the whole suite
```
pytest -v
```
Run an individual test file
```
pytest tests/test_hardware.py -v
```
Run an indivudal test case
```
pytest tests/test_hardware.py::TestHardware::test_co2 -v
```
