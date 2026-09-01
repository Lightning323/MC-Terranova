# pack github repo
this github repo can be used to download a pack using Packwiz, edit and develop the pack easily, by treating it as prism launcher instance.

# Prerequisites
## Git LFS
You must setup lfs to upload large attatchmnets to github
https://git-lfs.com/

## Packwiz
Packwiz is required to develop this modpack
https://github.com/packwiz/packwiz

use the bootstrap launcher to download and update the pack
https://github.com/packwiz/packwiz-installer-bootstrap

# Maintaining
* To build the project run `./build.sh`
* To build and push to github, run `./push.sh`
* To pull changes and import the mods to the development instance, run `./pull.sh`

# Downloading the modpack with packwiz bootstrap
While packwiz is Used by the dev to build and manage the pack, Packwiz bootstrap is used by players to stay updated

## To update/install the modpack
`java -jar packwiz-installer-bootstrap.jar https://raw.githubusercontent.com/Lightning323/MC-Terranova/main/pack/pack.toml`

## Running bootstrap command in prism launcher
`"$INST_JAVA" -jar "$INST_MC_DIR/packwiz-installer-bootstrap.jar" --no-gui https://raw.githubusercontent.com/Lightning323/MC-Terranova/main/pack/pack.toml`
