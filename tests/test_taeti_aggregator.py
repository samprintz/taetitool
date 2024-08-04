import unittest
from datetime import datetime, timedelta

from taetitool.model.issue import Issue
from taetitool.taeti_aggregator import TaetiAggregator
from taetitool.util import DefaultKeyDict


class TestTaetiAggretator(unittest.TestCase):
    def test_valid_file(self):
        taeti_file_path = 'files/20240215-valid.taeti'

        default_issue = Issue(None, None, 'Default project', 'Default task')

        issue_data = DefaultKeyDict(default_issue, {
            '1123': Issue(1123, 'Data import for CSV', 'ACME', 'Customizing',
                          'Data import'),
            '1987': Issue(1987, 'None', 'ACME', 'Customizing', 'Testing'),
            '3123': Issue(3123, 'Support case 221', 'PI Fan AG',
                          'Remote Support', ''),
            '3987': Issue(3987, 'Configuration of another feature for tenant X',
                          'PI Fan AG', 'Configuration', ''),
            '5123': Issue(5123, 'None', 'Fancy Project',
                          'AP02-01 Concept Module A', ''),
            '5124': Issue(5124, 'None', 'Fancy Project',
                          'AP02-01 Concept Module B', ''),
            '5223': Issue(5223, 'Implementation of Module A', 'Fancy Project',
                          'AP02-02 Implementation Module A', ''),
            '5224': Issue(5224, 'Implementation of Module B', 'Fancy Project',
                          'AP02-02 Implementation Module B', ''),
            '7123': Issue(7123, 'Support case 223', 'Support', '', ''),
            '7987': Issue(7987, 'Support case 227', 'Support', '', ''),
            '7124': Issue(7124, 'Support case 224', 'Default project',
                          'Default task', 'None')
        })

        assignment_rules = [
            {
                'name': 'break',
                'attribute': 'description',
                'pattern': 'Break|^Private',
                'project': 'Break',
                'task': 'Break'
            },
            {
                'name': 'meeting',
                'attribute': 'description',
                'pattern': 'Daily|Weekly|Sprint Retrospective|Product Management Round Table',
                'project': 'Internal tasks',
                'task': 'Meeting'
            },
            {
                'name': 'support',
                'attribute': 'project',
                'pattern': 'Support',
                'project': 'External tasks',
                'task': 'Support'
            }
        ]

        taeti_aggregator = TaetiAggregator(issue_data, assignment_rules)
        date, total_times, taetis = taeti_aggregator.process(taeti_file_path)

        self.assertEqual(date, 'Thursday, 15.02.2024')

        self.assertEqual(total_times[0], datetime(1900, 1, 1, 7, 15))
        self.assertEqual(total_times[1], datetime(1900, 1, 1, 16, 45))
        self.assertEqual(total_times[2], timedelta(seconds=34200))

        self.assertListEqual(list(taetis.keys()),
                             ['Default project', 'ACME', None, 'Break',
                              'Internal tasks', 'PI Fan AG', 'Fancy Project',
                              'Support'])

        self.assertEqual(
            len(taetis['Break']['grouped_taetis']['Break']['grouped_taetis'][
                    None]['grouped_taetis'][None]['taetis']), 5)

        self.assertListEqual(
            list(taetis['Default project']['grouped_taetis']['Default task'][
                     'grouped_taetis'][None]['grouped_taetis']),
            ['9987', '9123'])

        self.assertEqual(
            len(taetis[None]['grouped_taetis'][None]['grouped_taetis'][None][
                    'grouped_taetis'][None]['taetis']), 7)

        self.assertEqual(
            [t.description for t in
             taetis['Internal tasks']['grouped_taetis']['Meeting'][
                 'grouped_taetis'][None]['taetis']],
            ['Daily', 'Product Management Round Table'])

        tasks = list(taetis['Fancy Project']['grouped_taetis'].keys())
        expected_tasks = ['AP02-01 Concept Module A',
                          'AP02-01 Concept Module B',
                          'AP02-02 Implementation Module A',
                          'AP02-02 Implementation Module B']
        self.assertListEqual(tasks, expected_tasks)

        descs = [t.description for t in
                 taetis['Fancy Project']['grouped_taetis'][
                     'AP02-02 Implementation Module A']['grouped_taetis'][''][
                     'grouped_taetis'][5223]['taetis']]
        expected_descs = ['Implementation feature X', 'Refactor feature X']
        self.assertEqual(descs, expected_descs)

        self.assertListEqual(list(taetis['ACME']['grouped_taetis'].keys()),
                             ['Customizing'])
        self.assertListEqual(list(
            taetis['ACME']['grouped_taetis']['Customizing'][
                'grouped_taetis'].keys()), ['Data import', 'Testing'])

        self.assertEqual(
            [t.issue_id for t in
             taetis['Support']['grouped_taetis']['']['grouped_taetis'][''][
                 'taetis']], [7123, 7987])


if __name__ == '__main__':
    unittest.main()
