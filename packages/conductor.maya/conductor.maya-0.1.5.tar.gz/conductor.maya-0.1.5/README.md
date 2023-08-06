# DEV

```
<commit changes>
pip install --upgrade   git+file:///path/to/local-dev/conductor-maya@branch-name
setup_maya
<run maya>
e.g.

pip install --upgrade  git+file:///Users/julian/dev/conductor/conductor-maya@conductor-job-node && setup_maya && maya

pip install --upgrade  git+file:///Users/julian/dev/conductor/conductor-core@resolve-qt --target=/Users/julian/fooTest

```

# PYPI TEST

```
python setup.py sdist
twine upload --repository testpypi dist/conductor.maya-*.tar.gz
pip install --upgrade --index-url https://test.pypi.org/simple/  conductor.maya 

```


# PYPI PROD

```
python setup.py sdist
twine upload dist/conductor.maya-*.tar.gz
<enter your creds>
pip install --upgrade conductor.maya 

```

```
pip uninstall conductor.maya && \
pip install --upgrade  git+file:///Users/julian/dev/conductorconductor-maya@conductor-job-node && \
setup_maya && \
maya
```
 

 ```
 install  --upgrade git+file:///Users/julian/dev/conductor/conductor-maya@conductor-job-node --extra-index-url https://test.pypi.org/simple/  --target=/Users/julian/dev/conductor/conductor-installers/packages


install  --upgrade git+file:///Users/julian/dev/conductor/conductor-maya@conductor-job-node --extra-index-url https://test.pypi.org/simple/  --target=/Users/julian/dev/conductor/conductor-installers/packages

install  --upgrade  git+file:///Users/julian/dev/conductor/conductor-maya@conductor-job-node --extra-index-url https://test.pypi.org/simple/  --target=${installdir}/packages



install  --upgrade pip --target=/Users/julian/dev/conductor/conductor-installers/packages 


 ```