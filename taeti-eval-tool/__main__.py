#!/usr/bin/env python
from argparse import ArgumentParser
from configparser import ConfigParser

import util

parser = ArgumentParser(prog='taeti',
                        description='Taeti Evaluation Tool')

parser.add_argument("file",
                    help="Taeti file to evaluate")
parser.add_argument("--config",
                    default="../config.ini",
                    help="configuration file")

args = parser.parse_args()

config = ConfigParser()
config.read(args.config)

project_data_file_path = config.get("default", "project_data_file")

project_data = util.read_project_data(project_data_file_path, config.get("default", "default_project"))
taeti_data = util.read_taeti_data(args.file)

if len(taeti_data) == 0:
    print(f'No taeti records found')
    exit(0)

taetis = util.build_taetis(taeti_data, project_data)

print(taetis)
