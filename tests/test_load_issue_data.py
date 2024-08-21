import unittest

from taetitool import util


class TestAssignmentRuleParsing(unittest.TestCase):
    def test_load_issue_data(self):
        issue_data = util.load_issue_data('files/issue_titles.csv',
                                          'files/project_data.csv',
                                          'Default project',
                                          'Default task')

        expected_issue_ids = ['1123', '1987', '3123', '3987', '5123', '5124',
                              '5223', '5224', '7123', '7987', '7124']

        self.assertListEqual(list(issue_data.keys()), expected_issue_ids)

        # issue with both issue title and project data
        self.assertEqual(issue_data['1123'].project, 'ACME')
        self.assertEqual(issue_data['1123'].task, 'Customizing')
        self.assertEqual(issue_data['1123'].description, 'Data import')
        self.assertEqual(issue_data['1123'].title, 'Data import for CSV')

        # issue with issue title but no project data
        self.assertEqual(issue_data['7123'].project, 'Support')
        self.assertEqual(issue_data['7123'].task, '')
        self.assertEqual(issue_data['7123'].description, '')
        self.assertEqual(issue_data['7123'].title, 'Support case 223')

        # issue with project data but no issue title
        self.assertEqual(issue_data['5123'].project, 'Fancy Project')
        self.assertEqual(issue_data['5123'].task, 'AP02-01 Concept Module A')
        self.assertEqual(issue_data['5123'].description, '')
        self.assertEqual(issue_data['5123'].title, None)

    def test_load_issue_data_tsv(self):
        issue_data = util.load_issue_data('files/issue_titles.tsv',
                                          'files/project_data.tsv',
                                          'Default project',
                                          'Default task')

        expected_issue_ids = ['1123', '1987', '3123', '3987', '5123', '5124',
                              '5223', '5224', '7123', '7987', '7124']

        self.assertListEqual(list(issue_data.keys()), expected_issue_ids)

        # issue with both issue title and project data
        self.assertEqual(issue_data['1123'].project, 'ACME')
        self.assertEqual(issue_data['1123'].task, 'Customizing')
        self.assertEqual(issue_data['1123'].description, 'Data import')
        self.assertEqual(issue_data['1123'].title, 'Data import for CSV')

        # issue with issue title but no project data
        self.assertEqual(issue_data['7123'].project, 'Support')
        self.assertEqual(issue_data['7123'].task, '')
        self.assertEqual(issue_data['7123'].description, '')
        self.assertEqual(issue_data['7123'].title, 'Support case 223')

        # issue with project data but no issue title
        self.assertEqual(issue_data['5123'].project, 'Fancy Project')
        self.assertEqual(issue_data['5123'].task, 'AP02-01 Concept Module A')
        self.assertEqual(issue_data['5123'].description, '')
        self.assertEqual(issue_data['5123'].title, None)


if __name__ == '__main__':
    unittest.main()
