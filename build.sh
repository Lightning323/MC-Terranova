#!/bin/bash

cd pack

packwiz refresh
packwiz curseforge export -o ../dist/pack_prebuilt.zip

cd ../

./build-server.sh

java -jar packInstaller.jar -s ./minecraft -r -u ./pack/pack.toml
echo "Sync complete!"