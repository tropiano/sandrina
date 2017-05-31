# sandrina - A data engineering tool to provide data to people

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
