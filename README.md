
# README.md


## Preparation

Requires Python 3.7.x installed on your computer.

Clone this project:

```shell
git clone https://gitlab.rcs.griffith.edu.au/d.guillen/silvereye-wps-demo.git
```

Prepare and activate a virtual environment:

```shell
cd silvereye_wps_demo
python -m venv env
source env/bin/activate
```

Install dependencies:
```shell 
pip install -r requirements.txt
```

## To Execute 

```shell
env/bin/pserve development.ini --reload

```

## Troubleshooting 

If the above dependencies installation fails, 
or misses something, try the following:

Install dependencies:
```shell
pip install -e .
```

Install dependencies for development:
```shell
pip install -r ".[dev]"
```



