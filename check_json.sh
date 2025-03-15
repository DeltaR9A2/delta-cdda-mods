#!/bin/bash
for f in $( find . -type f -iname "*.json" ); do jq type < "$f" ; done
