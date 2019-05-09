python setup.py sdist
python -m unittest -v test.test_RSSD
python -m unittest -v test.test_yaVISA
twine upload .\dist\rssd-2019.5.4.tar.gz 
