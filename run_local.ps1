C:\VirtualEnvs\cascade\Scripts\activate.ps1
cd D:\GitHub\cascade

black .
flake8 .

mypy --install-types
mypy cascade tests docs/examples

pytest --doctest-modules

# building
pip install wheel
pip install build
python -m build --wheel
python -m build --sdist