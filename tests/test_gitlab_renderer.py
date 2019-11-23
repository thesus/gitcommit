from gitcommit.renderer import GitlabRenderer

import pytest


def test_checklist_checking():
    real_checklist = """
* [x] checked item
* [ ] unchecked 1
* [ ] unchecked 2"""

    text, line_number = GitlabRenderer.parse_checklist(real_checklist)

    assert text == "unchecked 1"
    assert line_number == 2

    checked_checklist = """
* [x] checked
    """

    text, line_number = GitlabRenderer.parse_checklist(checked_checklist)
    assert text == None
    assert line_number == -1
