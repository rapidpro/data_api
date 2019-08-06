# ReadOnly API for Rapidpro data warehouse

This platform allows you to import RapidPRO data from multiple projects into a single place.
It consumes RapidPro data via APIs and and re-serves that same data via those same APIs (but in aggregate).
The current version is based off of the [RapidPro V2 APIs](https://app.rapidpro.io/api/v2/).

# Usage

To import and organization and all its data (once) run:

```
./manage.py sync_organization_data [apikey]
```

or

```
./manage.py sync_organization_data [apikey] --server https://myinstance.rapidpro.io
```

# Dev Setup / Installation

## Prerequisites

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)
- [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

## Setup Virtualenv

`mkvirtualenv --no-site-packages rapidpro-dataapi`

## Install requirements:

Make sure you are in the root directory of the repository then run:

`pipenv install -d`

## Configure settings

If you need non-default settings, create a `localsettings.py` file in `data_api`.
Else you can use `settings_dev`.

For all `./manage.py` commands, replace `[settings module]` with whichever settings module you need, e.g. `data_api.settings_dev`

If you don't want to specify your settings module every time, just add

`export DJANGO_SETTINGS_MODULE=data_api.localsettings`

to your `$VIRTUAL_ENV/bin/postactivate` file.

And add `unset DJANGO_SETTINGS_MODULE` to `$VIRTUAL_ENV/bin/predeactivate` to avoid it messing with other virtualenvs.

## Setup Database

```
sudo -u postgres createdb rapidpro_data_api
./manage.py migrate --settings=[settings module]
```

## Run Server

`./manage.py runserver --settings [settings module]`

## Run Tests

`./manage.py test`

Or to run individual tests:

`./manage.py test data_api.staging.tests.test_data_import.DataImportTest.test_import_boundaries`

# Deployment

Deployment is managed with `fabric`.

To deploy to the UNICEF environment run:

`fab production deploy`

To deploy to another environment you can run

`fab deploy`

and manually specify the host at runtime.

For more information about the UNICEF production instance, see [production.md](../docs/production.md).

For guides to accomplishing specific tasks see [cookbooks.md](../docs/cookbooks.md).
