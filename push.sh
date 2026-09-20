#!/bin/bash


./build.sh


git add .
git commit -m "Update packs"

#Squash all staged commits into one
git reset --soft @{u}
git commit -m "Update packs"

git push