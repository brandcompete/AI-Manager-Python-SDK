#!/bin/bash

if [ -d "dist" ];
then
  echo "[BCCICD] Cleaning previous builds"
  rm dist/*
else
	echo "First build, nothing to clean"
fi

echo "[BCCICD] Building"
python3.12 -m build

echo "[BCCICD] Publishing with twine"
python3.12 -m twine upload -r local dist/* --config-file pypirc.local

echo "[BCCICD] Done ... Exiting"
