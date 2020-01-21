
# README.md


## Preparation

Prepare a virtual environment

```shell
cd silvereye_wps_demo
python -m venv env
source env/bin/activate
```

Install dependencies:
```shell
pip install -e .
```

Install dependencies for development:
```shell
pip install -r ".[dev]"
```

## To Execute 

```shell
env/bin/pserve development.ini --reload

```

