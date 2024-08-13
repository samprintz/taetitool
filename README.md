# taetitool

## Installation

```sh
python setup.py install
```

For development use:

```sh
python setup.py develop
```

## Configuration

The default location for configuration file `config.ini`
is `~/.config/taetitool/config.ini`.
Another location can be specified with `--config`.

There are two auxiliary CSV files
that can be used to provide information about issues:

1. A file with issue titles can be specified
   in the configuration file with `issue_title_file`.
   An example is given in `tests/files/issue_titles.csv`
2. A file with project information about the issues can be specified
   in the configuration file with `project_data_file`.
   Currently, three levels of structure are possible:
   Project > Task > Topic.
   The CSV columns follow this order.
   An example is given in `tests/files/project_data.csv`.

## Usage

```sh
taetitool 20240215.taeti
```
