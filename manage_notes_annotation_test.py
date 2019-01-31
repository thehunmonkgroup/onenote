import unittest
import copy

from pprint import pprint
from manage_notes_annotation import manage_notes_annotation

NOTE_ANNOTATION_NO_NOTES = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
}

MULTIPLE_ANNOTATIONS_NO_NOTES = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
    {
      "description": "test description",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "",
}

NOTE_ANNOTATION_WITH_NOTES = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "test notes",
}

MISSING_ANNOTATIONS_WITH_NOTES = {
  "uuid": "test-uuid",
  "notes": "test notes",
}

NO_ANNOTATION_WITH_NOTES = {
  "annotations": [
    {
      "description": "test description",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "test notes",
}

MULTIPLE_ANNOTATIONS_WITH_NOTES = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
    {
      "description": "test description",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "test notes",
}

class TestManageNotesAnnotation(unittest.TestCase):

    def test_note_annotation_no_notes(self):
      data = manage_notes_annotation(copy.deepcopy(NOTE_ANNOTATION_NO_NOTES))
      self.assertNotIn("annotations", data)

    def test_multiple_annotations_no_notes(self):
      data = manage_notes_annotation(copy.deepcopy(MULTIPLE_ANNOTATIONS_NO_NOTES))
      self.assertEqual(len(data["annotations"]), len(MULTIPLE_ANNOTATIONS_NO_NOTES["annotations"]) - 1)
      self.assertEqual(data["annotations"][0]["description"], "test description")

if __name__ == '__main__':
    unittest.main()
