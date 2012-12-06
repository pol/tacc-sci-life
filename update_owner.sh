#!/bin/bash

echo "Changing ownership of all spec files to build + CompBioApps"
chown  "build:G-800657" *.spec
chmod  ug+rw *.spec
echo "Done"

