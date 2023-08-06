# DEV

```
<commit changes>
pip install --upgrade   git+file:///path/to/local-dev/conductor-maya@branch-name
```

# PYPI TEST

```
python setup.py sdist
twine upload --repository testpypi dist/conductor.maya-*.tar.gz
pip install --index-url https://test.pypi.org/simple/  conductor.maya 

```


# PYPI PROD

```
python setup.py sdist
twine upload dist/conductor.maya-*.tar.gz
pip install  conductor.maya 

```



