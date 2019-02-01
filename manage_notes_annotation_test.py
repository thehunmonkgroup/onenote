import unittest
import copy

from pprint import pprint
from manage_notes_annotation import manage_notes_annotation

NOTE_ANNOTATION_NO_NOTES_BEFORE = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
}

NOTE_ANNOTATION_NO_NOTES_AFTER = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "",
}

MULTIPLE_ANNOTATIONS_NO_NOTES_BEFORE = {
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

MULTIPLE_ANNOTATIONS_NO_NOTES_AFTER = {
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
}

NOTE_ANNOTATION_WITH_NOTES_BEFORE = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "test notes",
}

NOTE_ANNOTATION_WITH_NOTES_AFTER = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "test notes",
}

NOTE_ANNOTATION_WITH_CHANGED_NOTES_BEFORE = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "test notes",
}

NOTE_ANNOTATION_WITH_CHANGED_NOTES_AFTER = {
  "annotations": [
    {
      "description": "[Notes]",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "test notes changed",
}

MISSING_ANNOTATIONS_WITH_NOTES_BEFORE = {
  "uuid": "test-uuid",
  "notes": "test notes",
}

MISSING_ANNOTATIONS_WITH_NOTES_AFTER = {
  "uuid": "test-uuid",
  "notes": "test notes",
}

NO_ANNOTATION_WITH_NOTES_BEFORE = {
  "annotations": [
    {
      "description": "test description",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "test notes",
}

NO_ANNOTATION_WITH_NOTES_AFTER = {
  "annotations": [
    {
      "description": "test description",
      "entry": "20190131T194834Z"
    },
  ],
  "uuid": "test-uuid",
  "notes": "test notes",
}

MULTIPLE_ANNOTATIONS_WITH_NOTES_BEFORE = {
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

MULTIPLE_ANNOTATIONS_WITH_NOTES_AFTER = {
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

def process_data(data_before, data_after):
  data = manage_notes_annotation(copy.deepcopy(data_before), copy.deepcopy(data_after))
  return data

class TestManageNotesAnnotation(unittest.TestCase):

    def test_note_annotation_no_notes(self):
      data = process_data(NOTE_ANNOTATION_NO_NOTES_BEFORE, NOTE_ANNOTATION_NO_NOTES_AFTER)
      self.assertNotIn("annotations", data)

    def test_multiple_annotations_no_notes(self):
      data = process_data(MULTIPLE_ANNOTATIONS_NO_NOTES_BEFORE, MULTIPLE_ANNOTATIONS_NO_NOTES_AFTER)
      self.assertEqual(len(data["annotations"]), len(MULTIPLE_ANNOTATIONS_NO_NOTES_AFTER["annotations"]) - 1)
      self.assertEqual(data["annotations"][0]["description"], "test description")

    def test_note_annotation_with_notes(self):
      data = process_data(NOTE_ANNOTATION_WITH_NOTES_BEFORE, NOTE_ANNOTATION_WITH_NOTES_AFTER)
      self.assertEqual(len(data["annotations"]), len(NOTE_ANNOTATION_WITH_NOTES_AFTER["annotations"]))
      self.assertEqual(data["annotations"][0]["description"], "[Notes]")

    def test_note_annotation_with_changed_notes(self):
      data = process_data(NOTE_ANNOTATION_WITH_CHANGED_NOTES_BEFORE, NOTE_ANNOTATION_WITH_CHANGED_NOTES_AFTER)
      self.assertEqual(len(data["annotations"]), len(NOTE_ANNOTATION_WITH_CHANGED_NOTES_AFTER["annotations"]))
      self.assertEqual(data["annotations"][0]["description"], "[Notes]")
      self.assertNotEqual(data["annotations"][0]["entry"], NOTE_ANNOTATION_WITH_CHANGED_NOTES_AFTER["annotations"][0]["entry"])

    def test_missing_annotations_with_notes(self):
      data = process_data(MISSING_ANNOTATIONS_WITH_NOTES_BEFORE, MISSING_ANNOTATIONS_WITH_NOTES_AFTER)
      self.assertEqual(len(data["annotations"]), 1)
      self.assertEqual(data["annotations"][0]["description"], "[Notes]")

    def test_no_annotation_with_notes(self):
      data = process_data(NO_ANNOTATION_WITH_NOTES_BEFORE, NO_ANNOTATION_WITH_NOTES_AFTER)
      self.assertEqual(len(data["annotations"]), len(NO_ANNOTATION_WITH_NOTES_AFTER["annotations"]) + 1)
      self.assertEqual(data["annotations"][0]["description"], "test description")
      self.assertEqual(data["annotations"][1]["description"], "[Notes]")

    def test_multiple_annotations_with_notes(self):
      data = process_data(MULTIPLE_ANNOTATIONS_WITH_NOTES_BEFORE, MULTIPLE_ANNOTATIONS_WITH_NOTES_AFTER)
      self.assertEqual(len(data["annotations"]), len(MULTIPLE_ANNOTATIONS_WITH_NOTES_AFTER["annotations"]))
      self.assertEqual(data["annotations"][0]["description"], "[Notes]")
      self.assertEqual(data["annotations"][1]["description"], "test description")

if __name__ == '__main__':
    unittest.main()
