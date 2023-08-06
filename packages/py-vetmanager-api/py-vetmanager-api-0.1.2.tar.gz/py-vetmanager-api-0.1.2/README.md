# py-vetmanager-api

![Build Status](https://github.com/otis22/PyVetmanagerApi/workflows/Python%20package/badge.svg)

Python library for work with vetmanager api

# Examples

```
try:
    domain = DomainProd('tests')
    client = VetmanagerClient('test_app', domain)
    token = client.token('admin', 'mypassword')
catch  Exception as err: 
    print(str(err))
```


# For contributor

## Run tests

```python -m unittest discover tests```

## For publish package

```
python setup.py sdist
twine upload --skip-existing dist/* -r testpypi
twine upload --skip-existing dist/*
```