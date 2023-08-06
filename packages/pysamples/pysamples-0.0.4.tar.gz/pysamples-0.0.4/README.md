Pysamples Package

This is a python samples collection package.

How to upload package to pypi  
python -m pip 
install --user --upgrade setuptools wheel  
python .\setup.py sdist bdist_wheel  
python -m pip install --user --upgrade twine  
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*  
pip install -i https://test.pypi.org/simple/ pysamples==0.0.4  
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*  