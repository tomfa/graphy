# Graphene demo

Tests and demonstrations for django-graphene + django rest framework.

## Setup

### Install python
This repo should work out of the box with python 3.7, and probably most other python 3 versions.

The commands below install 3.7 specifically
```
# See https://github.com/pyenv/pyenv-installer if you got Linux
brew install pyenv

# Installs 3.7.0, specified in .python-version
pyenv install
```

### Install requirements
```
# Create and activate virtualenv
$(pyenv which python) -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```


## Related reading
- [Django: Getting started with Django](https://www.djangoproject.com/start/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/)
