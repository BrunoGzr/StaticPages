#!/usr/bin/env bash
set -e
cd /home/brunogzr/Bruno/static-site-generator
export PATH="$HOME/.local/bin:$PATH"

gh auth setup-git

git rm -q .gitpush.sh
rm -f .installgh.sh .ghauth.sh

git add -A
git commit -m "Remove local helper scripts"
git push -u origin main

git log --oneline -2
git status --short
