import unittest
from datetime import date

from taetitool.attendance import (attendance_to_json, build_attendance_blocks,
                                  find_break_project)
from taetitool.model.issue import Issue
from taetitool.model.taeti import Taeti
from taetitool.taeti_aggregator import TaetiAggregator
from taetitool.util import DefaultKeyDict, parse_time

BREAK_RULE = {
    'name': 'break',
    'attribute': 'description',
    'pattern': 'Break|^Private',
    'project': 'Break',
    'task': 'Break'
}


def taeti(start, end, project=None):
    t = Taeti(parse_time(start), parse_time(end), 'description')
    t.project = project
    return t


def format_blocks(blocks):
    return [(s.strftime('%H:%M'), e.strftime('%H:%M')) for s, e in blocks]


class TestFindBreakProject(unittest.TestCase):
    def test_returns_project_of_break_rule(self):
        rules = [{'name': 'meeting', 'project': 'Internal tasks'}, BREAK_RULE]

        self.assertEqual(find_break_project(rules), 'Break')

    def test_returns_none_without_break_rule(self):
        rules = [{'name': 'meeting', 'project': 'Internal tasks'}]

        self.assertIsNone(find_break_project(rules))


class TestBuildAttendanceBlocks(unittest.TestCase):
    def test_merges_contiguous_entries(self):
        taetis = [taeti('08:00', '09:00'), taeti('09:00', '10:30')]

        blocks = build_attendance_blocks(taetis, 'Break')

        self.assertEqual(format_blocks(blocks), [('08:00', '10:30')])

    def test_splits_blocks_at_breaks(self):
        taetis = [
            taeti('08:00', '12:00'),
            taeti('12:00', '13:00', 'Break'),
            taeti('13:00', '16:00')
        ]

        blocks = build_attendance_blocks(taetis, 'Break')

        self.assertEqual(format_blocks(blocks),
                         [('08:00', '12:00'), ('13:00', '16:00')])

    def test_splits_blocks_at_gaps(self):
        taetis = [taeti('08:00', '09:00'), taeti('09:05', '10:00')]

        blocks = build_attendance_blocks(taetis, 'Break')

        self.assertEqual(format_blocks(blocks),
                         [('08:00', '09:00'), ('09:05', '10:00')])

    def test_sorts_entries_by_start_time(self):
        taetis = [taeti('09:00', '10:00'), taeti('08:00', '09:00')]

        blocks = build_attendance_blocks(taetis, 'Break')

        self.assertEqual(format_blocks(blocks), [('08:00', '10:00')])

    def test_drops_leading_and_trailing_breaks(self):
        taetis = [
            taeti('07:00', '08:00', 'Break'),
            taeti('08:00', '09:00'),
            taeti('09:00', '10:00', 'Break')
        ]

        blocks = build_attendance_blocks(taetis, 'Break')

        self.assertEqual(format_blocks(blocks), [('08:00', '09:00')])

    def test_keeps_all_entries_without_break_project(self):
        taetis = [taeti('08:00', '09:00'), taeti('09:00', '10:00', 'Break')]

        blocks = build_attendance_blocks(taetis, None)

        self.assertEqual(format_blocks(blocks), [('08:00', '10:00')])

    def test_raises_on_overlapping_entries(self):
        taetis = [taeti('08:00', '09:30'), taeti('09:00', '10:00')]

        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            build_attendance_blocks(taetis, 'Break')

    def test_raises_on_overlapping_break(self):
        taetis = [taeti('08:00', '09:30'), taeti('09:00', '10:00', 'Break')]

        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            build_attendance_blocks(taetis, 'Break')

    def test_raises_on_end_not_after_start(self):
        taetis = [taeti('09:00', '09:00')]

        with self.assertRaisesRegex(ValueError, 'End time'):
            build_attendance_blocks(taetis, 'Break')


class TestAttendanceToJson(unittest.TestCase):
    def test_formats_date_and_blocks(self):
        blocks = [(parse_time('05:45'), parse_time('09:30'))]
        self.assertEqual(attendance_to_json(date(2026, 10, 14), blocks), {
            'date': '2026-10-14',
            'blocks': [{'start': '05:45', 'end': '09:30'}]
        })

    def test_date_is_none_if_unknown(self):
        self.assertEqual(attendance_to_json(None, []),
                         {'date': None, 'blocks': []})


class TestExportAttendance(unittest.TestCase):
    def test_valid_file(self):
        default_issue = Issue(None, None, 'Default project', 'Default task')
        issue_data = DefaultKeyDict(default_issue, {})
        taeti_aggregator = TaetiAggregator(issue_data, [BREAK_RULE])

        attendance = taeti_aggregator.export_attendance(
            'files/20240215-valid.taeti')

        self.assertEqual(attendance, {
            'date': '2024-02-15',
            'blocks': [
                {'start': '07:15', 'end': '08:05'},
                {'start': '08:30', 'end': '08:55'},
                {'start': '09:25', 'end': '09:35'},
                {'start': '10:00', 'end': '10:30'},
                {'start': '10:35', 'end': '10:50'},
                {'start': '10:55', 'end': '15:20'},
                {'start': '15:30', 'end': '16:45'}
            ]
        })


if __name__ == '__main__':
    unittest.main()
