#!/bin/bash

echo "Changing ownership of all spec files to build + CompBioApps"
chown -R "build:G-800657" *.spec
echo "Done"

