#!/usr/bin/env bash

PROGNAME="$(basename $0)"

function usage() {
  echo "
Usage: ${PROGNAME}
Usage: ${PROGNAME} --help

Converts the the OneNote 'notes' UDA from TaskWarrior 5.1 and prior format to
TaskWarrior 5.2 and beyond format.

This script requires the jq binary be in your path.

CAVEATS:

BACK UP YOUR DATA FIRST!!!

This is a one-way operation, and if there are issues, well, you should really
have a backup.

By default, this converts all tasks, including completed/deleted.
"
}

if [ $# -gt 0 ]; then
  usage
  exit 1
fi

if [ -z "$(which jq)" ]; then
  echo "ERROR: missing jq binary"
  usage
  exit 1
fi

uuids="$(task _uuids)"

for uuid in $uuids; do
  notes="$(task verbose=nothing ${uuid} export | jq .[0].notes?)"
  if [ "${notes}" != "null" ]; then
    adjusted_notes="$(echo "${notes}" | sed -e 's/###NEWLINE###/\\n/g')"
    #echo "${adjusted_notes}"
    task rc.confirmation=off ${uuid} modify notes:"${adjusted_notes}"
  fi
done

