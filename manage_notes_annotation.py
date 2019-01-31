#!/usr/bin/env python

import os
import sys
import time
import json

LOG_FILEPATH = "/tmp/onenote.log"
NOTES_ANNOTATION_DESCRIPTION = "[Notes]"
DEBUG = "ONENOTE_DEBUG" in os.environ

def log(message):
  if DEBUG:
    with open(LOG_FILEPATH, 'a') as logfile:
      logfile.write("%s\n" % message)

def to_iso_string(time_struct):
  format_string = "%Y%m%dT%H%M%SZ"
  return time.strftime(format_string, time_struct)

def current_time():
  return time.gmtime(time.time())

def current_time_iso():
  return to_iso_string(current_time())

def check_notes(data):
  return "notes" in data and data["notes"].strip()

def check_notes_annotation(data):
  if "annotations" in data:
    for i, annotation in enumerate(data["annotations"]):
      if annotation["description"] == NOTES_ANNOTATION_DESCRIPTION:
        log("Found %s annotation for task: %s" % (NOTES_ANNOTATION_DESCRIPTION, data["uuid"]))
        return True
  return False

def add_notes_annotation(data):
  if not "annotations" in data:
    data["annotations"] = []
  annotation = {
    "entry": current_time_iso(),
    "description": NOTES_ANNOTATION_DESCRIPTION,
  }
  data["annotations"].append(annotation)
  log("Added %s annotation for task: %s" % (NOTES_ANNOTATION_DESCRIPTION, data["uuid"]))
  return data

def remove_notes_annotation(data):
  if "annotations" in data:
    for i, annotation in enumerate(data["annotations"]):
      if annotation["description"] == NOTES_ANNOTATION_DESCRIPTION:
        data["annotations"].pop(i)
        log("Removed %s annotation for task: %s" % (NOTES_ANNOTATION_DESCRIPTION, data["uuid"]))
    if not data["annotations"]:
      data.pop('annotations', None)
  return data

def manage_notes_annotation(data):
  notes_exist = check_notes(data)
  notes_annotation_exists = check_notes_annotation(data)
  if notes_exist and not notes_annotation_exists:
      data = add_notes_annotation(data)
  if not notes_exist and notes_annotation_exists:
      data = remove_notes_annotation(data)
  return data

if __name__ == '__main__':

  task = json.loads(sys.stdin.readline())
  modified_task = manage_notes_annotation(task)
  log(json.dumps(modified_task, sort_keys=True, indent=2))

  print(json.dumps(modified_task))
  sys.exit(0)
