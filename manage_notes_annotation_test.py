import unittest
import copy
import json

from pprint import pprint
from manage_notes_annotation import load_task_data, manage_notes_annotation

TASK_ADD_NO_NOTES = {
  "uuid": "test-uuid",
}

TASK_ADD_WITH_NOTES = {
  "uuid": "test-uuid",
  "notes": "test notes",
}

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

    def test_load_task_data_add(self):
      json_string = json.dumps(TASK_ADD_WITH_NOTES)
      task_before, task_after = load_task_data(json_string, "")
      self.assertEqual(task_before, {})
      self.assertEqual(task_after, TASK_ADD_WITH_NOTES)

    def test_load_task_data_modify(self):
      json_string_before = json.dumps(NOTE_ANNOTATION_NO_NOTES_BEFORE)
      json_string_after = json.dumps(NOTE_ANNOTATION_NO_NOTES_AFTER)
      task_before, task_after = load_task_data(json_string_before, json_string_after)
      self.assertEqual(task_before, NOTE_ANNOTATION_NO_NOTES_BEFORE)
      self.assertEqual(task_after, NOTE_ANNOTATION_NO_NOTES_AFTER)

    def test_add_task_no_notes(self):
      data = process_data({}, TASK_ADD_NO_NOTES)
      self.assertNotIn("annotations", data)

    def test_add_task_with_notes(self):
      data = process_data({}, TASK_ADD_WITH_NOTES)
      self.assertEqual(len(data["annotations"]), 1)
      self.assertEqual(data["annotations"][0]["description"], "[Notes]")

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
