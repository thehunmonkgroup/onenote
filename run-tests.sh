#!/usr/bin/env bash

CWD=$(pwd)

progdir="$(dirname ${0})"
cd ${progdir}

echo "Running onenote script tests..."
echo
basht onenote_test
echo
echo "Running onenote hook tests..."
echo
python manage_notes_annotation_test.py
echo
echo "Done!"

cd ${CWD}

