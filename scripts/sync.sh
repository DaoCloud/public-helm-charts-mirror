#!/usr/bin/env bash

# Perpare the charts-syncer environment
if ! command -v charts-syncer &>/dev/null; then
  echo "charts-syncer could not be found, use https://github.com/yankay/charts-syncer."
  exit
fi

# Generate chart-sync config file
mkdir -p config
python3 scripts/generate-sync-config.py

# Use chart-sync to Sync

search_dir=config
total=0
sync=0
failed=()
for entry in "$search_dir"/*; do
  echo "SYNC: ${entry}"
  charts-syncer -c "${entry}" sync
  if [[ $? -eq 0 ]]; then
    ((sync++))
  else
    failed+=("${entry}")
  fi

  ((total++))
done

echo "${sync}/${total}"

if [[ "${#failed[*]}" -ne 0 ]]; then
  echo "Failed: ${failed[*]}"
fi

if [[ "${badge}" == "true" ]]; then
  echo "https://img.shields.io/badge/Sync-${sync}%2F${total}-blue" -O badge.svg
  wget "https://img.shields.io/badge/Sync-${sync}%2F${total}-blue" -O badge.svg
fi

# Clean Up
rm -rf config
