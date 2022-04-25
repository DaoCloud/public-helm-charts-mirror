#!/usr/bin/env bash

# Perpare the charts-syncer environment
if ! command -v charts-syncer &> /dev/null
then
    echo "charts-syncer could not be found, use https://github.com/yankay/charts-syncer."
    exit
fi

# Generate chart-sync config file
mkdir -p config
python3 scripts/generate-sync-config.py

# Use chart-sync to Sync

search_dir=config
for entry in "$search_dir"/*
do
  echo "SYNC: $entry"
  charts-syncer -c $entry sync
done

# Clean Up
rm -rf config

