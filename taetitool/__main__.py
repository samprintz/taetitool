#!/usr/bin/env python
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
                        default="../config.ini",
                        help="configuration file")

    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)

    project_data_file_path = config.get("default", "project_data_file")
    default_project = config.get("default", "default_project")
    default_task = config.get("default", "default_task")
    support_task = config.get("default", "support_task")

    date = util.parse_date(args.file)
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
