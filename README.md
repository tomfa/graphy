
## Graphy - a demo of Graphene-Django

Code and demonstation of the transition from
[Django REST Framework](https://www.django-rest-framework.org/) (DRF) to [Graphene-Django](https://docs.graphene-python.org/).

Parts of the documentation of Graphene is currently a bit slim. 
The purpose of this repository is to show code examples compared against DRF, 
and help getting started with GraphQL on a Django backend, or transitioning from DRF.

_Slides used for related [Python meetup talk](https://meetup.com/oslo-python/events/256206700/) 
can be found [here](https://slides.com/tomasfagerbekk/graphql-w-graphene)_

### Summary

- Transition from DRF is surprisingly easy, and is done in quite few lines
of code.
- Documentation from Django `help_text` will be reused in schema generated 
from GraphQL.
- You can reuse existing DRF serializers and validation
- Addressing authentication and authorization is not a part of GraphQL spec and 
there's little help in Graphene or documentation about it. Own implementation 
can be found at [graphy/utils/graphql.py](https://github.com/tomfa/graphy/blob/master/graphy/utils/graphql.py)
- Graphene performs comparably to DRF even if you have "ideal" REST endpoints 
that avoid overfetching.

### Examples

- [3d55467](https://github.com/tomfa/graphy/commit/3d554670874e5ede6dbd4b363fcb2bb56b25f84a) - Adding your first GraphQL endpoint and _query_.
- [c71967a](https://github.com/tomfa/graphy/commit/c71967ad14cd674e1c9620b6966acfd54760c648) - Adding your first GraphQL test.
- [e7a366c](https://github.com/tomfa/graphy/commit/e7a366cf0af7134eefce8860e0356107ff27d8a0) - Reusing DRF serializer to create your first _mutation_.
- [3a72f29](https://github.com/tomfa/graphy/commit/3a72f295611faf829c7a9afc526d566ed906f3f9) -  `@auth_required` wrapper added, returning a HTTP 401 or error object (Two different views).
- [ece2cf0](https://github.com/tomfa/graphy/commit/ece2cf0bd778dcdbc88ac2e60a66f88324a3ccac) - Disallowing queries over a given depth.

### Performance comparison

Since the nature of GraphQL and REST APIs are quite different, a performance 
comparision might not map to the differences in your real life situation.

While it makes perfect sense to prefetch (`select_related` with Django ORM)
to a REST endpoint that needs the prefetched data, the same can not be said for 
GraphQL endpoints, since a single GraphQL Query (comparable to a View in DRF,
or an endpoint in a typical REST API) can be used for quite different cases.

For an ideal implementation (performance wise), where a Graphene Query and a 
DRF endpoint is implemented to serve a single, given data request, it 
looks like DRF is performing better: 1-5% when the `select_related` is
not used, and 10-50% when `select_related` is used. The relative difference
seems to to be larger the more instances are returned.

For real life implementations, overfetching is a problem that GraphQL
avoids to a much larger degree than REST, and we've seen (large) 
performance gains at [Otovo](https://github.com/otovo/) when switching from
DRF to GraphQL. But be aware that GraphQL list queries where nested models
are fetched can be slow when using Graphene naively. Consider adding
own endpoints using `select_related` for such queris, or implementing 
assistance that modifies the database query based on the GraphQL Query.

Details of tests can be found in

- `./graphy/location/views.py` (DRF) 
- `./graphy/location/gql_actions.py` (Graphene)
- `./graphy/location/tests/test_gql_vs_drf_performance.py` (GraphQL Query / REST call)

Numbers below are an average of 500 requests done when using curl against a 
non-debug server running postgres.

**WITHOUT `select_related`**

| Type                         | Avg time | Returned objects |
| ---------------------------- | -------- | ---------------- |
| Shallow GraphQL query        | 19.2 ms  | 1                |
| DRF                          | 27.9 ms  | 1                |
| Deep GraphQL query           | 28.1 ms  | 1                |
| Shallow GraphQL query        | 29.8 ms  | 100              |
| DRF                          | 422.1 ms | 100              |
| Deep GraphQL query           | 441.6 ms | 100              |

**WITH `select_related`**

| Type                         | Avg time | Returned objects |
| ---------------------------- | -------- | ---------------- |
| Shallow GraphQL query        | 22.8 ms  | 1                |
| DRF                          | 24.5 ms  | 1                |
| Deep GraphQL query           | 26.2 ms  | 1                |
| Shallow GraphQL query        | 49.9 ms  | 100              |
| DRF                          | 50.0 ms  | 100              |
| Deep GraphQL query           | 75.54 ms | 100              |

## Setup

#### Install python
This repo should work out of the box with python 3.7, and probably most other python 3 versions.

The commands below install 3.7 specifically on Mac / Linux
```
# See https://github.com/pyenv/pyenv-installer if you got Linux
brew install pyenv

# Installs 3.7.0, specified in .python-version
pyenv install
```

#### Install requirements
```
# Create and activate virtualenv
$(pyenv which python) -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

#### Load test data
```
python manage.py migrate
python manage.py loaddata db.json
```

This db dump includes a few instances of each model and a superuser
with username: `admin` and password `admin` (...)


## Run server
```
python manage.py migrate
python manage.py runserver
```

#### Admin panel
Admin panel runs at 
[localhost:8000/admin](http://localhost:8000/admin). If you need to, you can 
create a super user with `python manage.py createsuperuser`

#### GraphiQL
Interactive GraphiQL runs at [localhost:8000/graphql](http://location:8000/graphql).

### Tests
```
# Runs all tests
pytest
```


## Related reading
- [Django: Getting started with Django](https://www.djangoproject.com/start/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/)
