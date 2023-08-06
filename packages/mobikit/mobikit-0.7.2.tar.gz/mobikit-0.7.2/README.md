# Mobikit Data Science Library

TODO: migrate what we want to keep into reStructuredText files with an `index.rst`
index page that's linked to from the top-level `index.rst` under `Components:`

## Public Distribution

Currently, the feeds portion of the data science library is approved for public distribution. In order to release a new version of the library, follow the steps below:

0. If necessary, install/upgrade `twine` with `pip install --upgrade twine`.

1. Make sure you have the credentials for Mobikit's PyPl account available. you will need these in order to publish.

1. Bump the library version appropriately in `setup_base.py`.

1. Bundle the library for distribution:
   `rm -rf dist && rm -rf build && python3 setup_public.py sdist bdist_wheel`

1. Distribute the library to PyPl: (you will be asked to provide Mobikit's PyPl credentials here)
   test index: `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
   production index: `twine upload dist/*`

1. Install your newly distributed `mobikit` library:
   install from test index: `pip install --index-url https://test.pypi.org/simple/ --no-deps mobikit`
   install from production index: `pip install mobikit`
