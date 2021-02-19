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
Run the whole suite (with no dependencies)
```
pytest -v --ignore=tests/test_hardware.py
```
Run the whole suite (with dependencies --> see IoT README to install)
```
pytest -v
```
Run an individual test file
```
pytest tests/test_hardware_emulator.py -v
```
Run an indivudal test case
```
pytest tests/test_hardware_emulator.py::TestHardwareEmulator::test_co2 -v
```
