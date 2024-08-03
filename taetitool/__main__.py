#!/usr/bin/env python
import os.path
from argparse import ArgumentParser
from configparser import ConfigParser

import taetitool.util as util


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

    issue_title_file_path = config.get("default", "issue_title_file")
    project_data_file_path = config.get("default", "project_data_file")
    default_project = config.get("default", "default_project")
    default_task = config.get("default", "default_task")
    project_print_order = config.get("output", "project_print_order")

    issue_data = util.load_issue_data(issue_title_file_path,
                                      project_data_file_path,
                                      default_project,
                                      default_task)

    date = util.parse_date(taeti_file_path)
    taeti_data = util.read_taeti_data(args.file)

    if len(taeti_data) == 0:
        print(f'No taeti records found')
        exit(0)

    assignment_rules = util.parse_assignment_rules(config.items('rules'))

    taetis = util.build_taetis(taeti_data, issue_data)
    util.apply_assignment_rules(taetis, assignment_rules)
    grouped_taetis = util.group_taetis(taetis)
    total_times = util.get_total_times(taetis)
    util.print_taetis(date, total_times, grouped_taetis, project_print_order)


if __name__ == "__main__":
    main()
