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

def check_notes_updated(data_before, data_after):
  if not "notes" in data_before and not "notes" in data_after:
    return False
  elif not "notes" in data_before and "notes" in data_after:
    return data_after["notes"].strip()
  elif "notes" in data_before and not "notes" in data_after:
    return data_before["notes"].strip()
  else:
    return data_before["notes"].strip() != data_after["notes"].strip()

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

def manage_notes_annotation(data_before, data_after):
  # Deletion case, just return the task as is.
  if data_before and not data_after:
    return data_before
  notes_exist = check_notes(data_after)
  notes_annotation_exists = check_notes_annotation(data_after)
  if check_notes_updated(data_before, data_after):
    # Force removal here and mark as removed, allows a new annotation
    # with an updated entry time for the notes.
    data_after = remove_notes_annotation(data_after)
    notes_annotation_exists = False
  if notes_exist and not notes_annotation_exists:
      data_after = add_notes_annotation(data_after)
  if not notes_exist and notes_annotation_exists:
      data_after = remove_notes_annotation(data_after)
  return data_after

def read_stdin():
  first_line = sys.stdin.readline()
  second_line = sys.stdin.readline()
  return first_line, second_line

def load_task_data(first_line, second_line):
  if second_line:
    try:
      task_before = json.loads(first_line)
      task_after = json.loads(second_line)
      return task_before, task_after
    except:
      exit_error()
  else:
    try:
      task_after = json.loads(first_line)
      return {}, task_after
    except:
      exit_error()

def exit_error():
  e = sys.exc_info()[0]
  log("Error: %s" % e)
  sys.exit(1)

if __name__ == '__main__':

  try:
    first_line, second_line = read_stdin()
    task_before, task_after = load_task_data(first_line, second_line)
    if task_before:
      if task_after:
        log("Modifying current task")
        log("Task before modification")
      else:
        log("Deleting current task")
        log("Task before deletion")
      log(json.dumps(task_before, sort_keys=True, indent=2))
    else:
      log("Adding new task")
    if task_after:
      log("Task after modification")
      log(json.dumps(task_after, sort_keys=True, indent=2))
    modified_task = manage_notes_annotation(task_before, task_after)
    log("Task after hook adjustments")
    log(json.dumps(modified_task, sort_keys=True, indent=2))
  except:
    exit_error()

  print(json.dumps(modified_task))
  sys.exit(0)
