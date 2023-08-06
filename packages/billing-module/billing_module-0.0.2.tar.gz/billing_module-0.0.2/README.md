# Billing module

##How to prepare to upload to Pip
python setup.py sdist

##upload to pip
pip install twine

note: you need a python pip in pypi.org account before continue 
twine upload dist/*

##How to use
pip install billing_module

##How to test

### Directly using code
Execute tests.py

### Command line
python -m unittest discover -s tests

note: Execute the code in root path
