# sandrina - A data engineering tool to provide data to people

[![Build Status](https://travis-ci.org/tropiano/sandrina.svg?branch=master)](https://travis-ci.org/tropiano/sandrina)

The aim of the project is to develop a tool and the whole underlying
infrastructure to provide easy access to open data to the people.
Not just providing data, but also useful algorithms able to make
easier their interpretation.

## directory hierarchy

The following is the directory schema of the project:

```
   datasets/      json_datasets/ notebooks/     src/
```

In the `dataset/` directory the original csv files are stored. The idea is to
store here also future new and updated datasets.

The `src/` directory contains the source codes for initial cleanup of csv files,
the import on a database engine, and the analysis.

The `json_datasets/` contains the produced cleaned data from csv in json format,
that are then imported in the database engine.

The `notebooks/` directory contains the `jupiter` notebooks produced for data
analysis experiments.

## data structure

Data, after the cleanup, is stored in a json key-value format. The main
sections are:

* `metadata`, reporting the info about when the data is referred and the source
* `data`, the section that store, in a list, all the record from the original
csv in key-value format

This should be the final format of the json:

```
{  
   "metadata": {
        "date": "01052017",
        "source": "regione toscana"
    },
    "data": [
        {
            "field1": "value1",
            "field2": "value2",
            "field3": "value3",
            ...
        },
        ...
    ]
}
```

[NOTE]
It is important to import all the field of the csv at this level. In particular,
it is important to import the city, and the reference year.

## how to set up a development environment

`pyenv` could be a good choice to set up a development environment. See
[pyenv web page](https://github.com/pyenv/pyenv).

All code, before passing to the test phase, has to be checked through
[flake8](http://flake8.pycqa.org/en/latest/) module.

All python modules should be installed through `pip`: once `pyenv` is installed
install a local 2.7.X environment, then install the related `pip` manager

```
pyenv install 2.7.13
pyenv local 2.7.13
easy_install pip=9.0.1
pip install <package>
```

no `sudo` privileges should be used here.

## how to create a requirements.txt file

We choose [`pipreqs`](https://github.com/bndr/pipreqs) to create the `requirements.txt` file. 

Instructions to re-create file:

- Navigate to the root of the project
- Type command: `pipreqs --force .`

The `requirements.txt` file will be over-written. 

## The infrastructure

The project will be based on a single Ubuntu Xenial 16.04 machine, with as many
Docker containers as many services will be needed (consider at the moment a DB,
a web server and probably a middleware layer for computation).

### Install docker

We are considering here just instructions for Mac OS environments, but they can
be easily adapted for any Unix-like environment.

* take care to have XCode and Brew installed in your system:
** https://itunes.apple.com/au/app/xcode/id497799835?mt=12
** https://brew.sh/

* Install Docker: for Mac OS user, download the package from https://docs.docker.com/docker-for-mac/

* (optional) if you want to execute `docker` commands without root privileges,
  add your user to `docker` group:
```
sudo dscl . create /Groups/docker
sudo dseditgroup -o edit -a $(whoami) -t user docker
```

### How to manage docker containers

The `docker/` directory contains the docker files to build a test environment.
Currently, it contains:

* all needed to build a container dedicated to `PostgreSQL`.
* all needed to build a container (`client`) to test connections to the database,
  and represents the base for the other services that will need to connect
  to it.

In `docker/` there's a script, `manage-datum-analitica`, able to manage all
`docker` commands to build, refresh and destroy the infrastructure. Use `-h`
option to read the header documentation of the script.

[NOTE]
If docker has not been confgured to be run without root privileges, consider
to run the commands with `sudo`.

The `Dockerfile`'s are able to completely configure the database and the `client`
container to connect to the database (as `root` system user, using RW and RO
database's roles). From the `client` container type (consider for instance RO
user to connect)
```
psql -U sandrina_ro -h postgresql -p 5432 -d sandrina
```

Authentication is automized through `pgpass` file that contains the access
credentials.

It is also possible to connect to the database from the host (local machine)
through
```
psql -U sandrina_ro -h localhost -p XXXXX -d sandrina
```

where `XXXXX` is the TCP port addressed to the `postgresql` container - it should
be obtainable through the `netstat` command. Actually, all is thought to enable
connections between docker containers.

**Useful docker commands**:

* `docker ps -a` to list the status of the containers
* `docker exec -it client bash` to login in the `client` container's shell (as
  `root` user)
* `docker exec -it postgresql bash` to login in the `postgresql` container's
  shell (as `root` user)

Other useful commands can be found in the `manage-datum-analitica` script.

[NOTE]
If docker has not been confgured to be run without root privileges, consider
to run the commands with `sudo`.

### Web Applications

Once run the `manage-datum-analitica` script with the command

* `manage-datum-analitica build`

Navigate to the following link: http://0.0.0.0:5000/. This is the home page. 

The template for every regione is the same. You can see here for Toscana: http://0.0.0.0:5000/Toscana/

To check for different regione just replace the regione name. For Sicilia http://0.0.0.0:5000/Sicilia/

Only 3 endpoints work for the moment:

- http://0.0.0.0:5000/regioni/
- http://0.0.0.0:5000/<nome_regione>
- http://0.0.0.0:5000/Toscana/<nome_comune>