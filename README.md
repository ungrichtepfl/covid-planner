# covid-planner

Schedule meetings either in person or in zoom, based on the weather condition.

## Quick Start

For developing I use [poetry](https://python-poetry.org/).

### Install poetry

Linux/Mac:

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Windows:

```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

Test installation in shell:

```
poetry --version
```

### Clone Repository

Make sure
your [ssh](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
key is set up, or use _https_.

```
git clone git@github.com:ungrichtepfl/covid-planner.git
cd covid-planner
```

### Create virtual environment

Use venv or any other virtual environment creater of your choice (e.g. use directly poetry):

```
python3 -m venv venv
source venv/bin/activate
```

### Install with poetry

```
poetry install
```

### Run with poetry

```
poetry run covid-planner
```

## Add API Keys

Visit [Open Weather Map](https://openweathermap.org/appid#:~:text=The%20API%20key%20is%20all,additional%20API%20keys%20if%20needed.)
to create an open weather API key and follow the first part of the tutorial
found [here](https://www.geeksforgeeks.org/how-to-create-a-meeting-with-zoom-api-in-python/) to create an Zoom API key
and secret. Copy the file `api_keys_template.yaml` found in `src/covid_planner/templates/` to a file
in `config/api_keys.yaml`
(create directory and file if not yet existing or run program once). Add the generated keys at the appropriate
locations.
