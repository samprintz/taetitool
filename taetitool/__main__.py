#!/usr/bin/env python
import os.path
from argparse import ArgumentParser
from configparser import ConfigParser

import taetitool.util as util
from taetitool.config import project_assignments


def main():
    parser = ArgumentParser(prog='taeti',
                            description='Taeti Evaluation Tool')

    parser.add_argument("file",
                        help="Taeti file to evaluate")
    parser.add_argument("--config",
                        default="~/.config/taetitool/config.ini",
                        help="configuration file")

    args = parser.parse_args()

    config_path = os.path.expanduser(args.config)
    taeti_file_path = os.path.expanduser(args.file)

    if not os.path.isfile(taeti_file_path):
        print(f'Taeti data file not found: "{taeti_file_path}"')
        exit(0)

    if not os.path.isfile(config_path):
        print(f'Configuration file not found: "{config_path}"')
        exit(0)

    config = ConfigParser()
    config.read(config_path)

    project_data_file_path = config.get("default", "project_data_file")
    default_project = config.get("default", "default_project")
    default_task = config.get("default", "default_task")

    if not os.path.isfile(project_data_file_path):
        print(f'Project data file not found: "{project_data_file_path}"')
        exit(0)

    date = util.parse_date(taeti_file_path)
    project_data = util.read_project_data(project_data_file_path,
                                          default_project,
                                          default_task)
    taeti_data = util.read_taeti_data(args.file)

    if len(taeti_data) == 0:
        print(f'No taeti records found')
        exit(0)

    taetis = util.build_taetis(taeti_data, project_data)
    util.set_special_projects_and_tasks(taetis, project_assignments)
    grouped_taetis = util.group_taetis(taetis)
    total_times = util.get_total_times(taetis)
    util.print_taetis(date, total_times, grouped_taetis)


if __name__ == "__main__":
    main()
