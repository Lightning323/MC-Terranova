#!/bin/bash

cd pack

packwiz refresh
# packwiz curseforge export -o ../dist/pack_prebuilt_cf.zip
packwiz modrinth export -o ../dist/pack_prebuilt.mrpack