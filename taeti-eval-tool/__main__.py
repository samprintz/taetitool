#!/usr/bin/env python
from argparse import ArgumentParser
from configparser import ConfigParser

import util
from config import project_assignments

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
default_project = config.get("default", "default_project")
default_task = config.get("default", "default_task")
support_task = config.get("default", "support_task")

project_data = util.read_project_data(project_data_file_path, default_project)
taeti_data = util.read_taeti_data(args.file)

if len(taeti_data) == 0:
    print(f'No taeti records found')
    exit(0)

taetis = util.build_taetis(taeti_data, project_data)
util.set_special_projects_and_tasks(taetis, project_assignments)

project_taetis = [t for t in taetis if t.issue_id is not None and t.project not in [default_project, support_task]]

print(taetis)
