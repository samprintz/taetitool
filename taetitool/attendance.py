import taetitool.util as util

BREAK_RULE_NAME = 'break'


def find_break_project(assignment_rules):
    for rule in assignment_rules:
        if rule['name'] == BREAK_RULE_NAME:
            return rule['project']
    return None


def build_attendance_blocks(taetis, break_project):
    """Merge contiguous non-break taetis into (start, end) blocks."""
    taetis = sorted(taetis, key=lambda t: t.time_start)

    for taeti in taetis:
        if taeti.time_end <= taeti.time_start:
            raise ValueError(f'End time not after start time: "{taeti}"')

    for previous, current in zip(taetis, taetis[1:]):
        if current.time_start < previous.time_end:
            raise ValueError(f'Overlapping entries: "{previous}" and "{current}"')

    blocks = []
    for taeti in taetis:
        if break_project and taeti.project == break_project:
            continue
        if blocks and blocks[-1][1] == taeti.time_start:
            blocks[-1] = (blocks[-1][0], taeti.time_end)
        else:
            blocks.append((taeti.time_start, taeti.time_end))

    return blocks


def attendance_to_json(date, blocks):
    return {
        'date': date.isoformat() if date else None,
        'blocks': [
            {'start': util.format_time(start), 'end': util.format_time(end)}
            for start, end in blocks
        ]
    }
