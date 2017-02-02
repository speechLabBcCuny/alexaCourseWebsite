#!/bin/bash

# Create zip file for upload to Amazon Lambda

TARGET=cisc1600status.zip

rm "$TARGET"
zip -r "$TARGET" * -x $0
