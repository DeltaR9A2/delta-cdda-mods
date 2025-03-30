#!/bin/bash
for f in $( find . -type f -iname "*.json" ); do echo "$f" && jq type < "$f" ; done
