# Popcorntime Api
Library to use the api of popcorntime in python

## Getting started
<!-- Install the library from pypi via `pip install openean` -->
Install the library from git with `pip install git+ssh://git@github.com/DavidM42/popcornTimeApi.git@master#egg=popcornTimeApi`

```python
from popcorntimeapi.Popcorn import PopcornTimeApi

popcorn = PopcornTimeApi()

random_movie = popcorn.get_random()

print(random_movie.title)

```
