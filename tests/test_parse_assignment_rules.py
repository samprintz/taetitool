import unittest

from taetitool import util


class TestParseAssignmentRules(unittest.TestCase):
    def test_valid_config(self):
        rule_tuples = [('rule_break_attribute', 'description'),
                       ('rule_break_pattern', 'Break|^Private'),
                       ('rule_break_project', 'Break'),
                       ('rule_break_task', 'Break'),
                       ('rule_meeting_attribute', 'description'), (
                           'rule_meeting_pattern',
                           'Daily|Weekly|Sprint Retrospective|Product Management Round Table'),
                       ('rule_meeting_project', 'Internal tasks'),
                       ('rule_meeting_task', 'Meeting'),
                       ('rule_support_attribute', 'project'),
                       ('rule_support_pattern', 'Support'),
                       ('rule_support_project', 'External tasks'),
                       ('rule_support_task', 'Support')]

        expected = [
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

        result = util.parse_assignment_rules(rule_tuples)

        self.assertListEqual(sorted(result, key=lambda x: x['name']), expected)


if __name__ == '__main__':
    unittest.main()
