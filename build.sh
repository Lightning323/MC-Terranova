#!/bin/bash

cd pack

packwiz refresh
cd ../

./build-server.sh

java -jar packInstaller.jar -s ./minecraft -r -u ./pack/pack.toml
echo "Sync complete!"