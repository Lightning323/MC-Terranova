#!/bin/bash

cd pack

packwiz refresh
# packwiz curseforge export -o ../dist/pack_prebuilt_cf.zip
packwiz modrinth export -o ../dist/pack_prebuilt.mrpack

#Regular build logic
cd ../
./build-server.sh
java -jar packInstaller.jar -s ./minecraft -r -u ./pack/pack.toml
echo "Sync complete!"