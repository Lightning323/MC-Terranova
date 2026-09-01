#!/bin/bash

# Sync files from /pack to /pack_server
rsync -av --delete --include-from='rsync-include.txt' ./pack/ ./pack_server/
cp -r ./server_mods/* ./pack_server/mods/

cd pack_server

################################################################################
## Edit server side mods ########################################################
################################################################################
#C2me or dynamic view but not both, pick one
packwiz curseforge add c2me -y
# packwiz curseforge add dynamic-view

packwiz curseforge add zfastnoise -y
packwiz curseforge add smooth-chunk-save -y
packwiz curseforge add leaky -y
#For disabling certain mobs (optional)
packwiz modrinth add in-control -y

# remove mods that would crash the server
rm ./mods/fastquit-forge.pw.toml
rm ./mods/sodium.pw.toml
rm ./mods/colorwheel.pw.toml
rm ./mods/irisshaders.pw.toml
# rm ./mods/xaeros-minimap.pw.toml

################################################################################
################################################################################
################################################################################

packwiz refresh
