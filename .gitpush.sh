#!/usr/bin/env bash
set -e
cd /home/brunogzr/Bruno/static-site-generator

git config user.name "BrunoGzr"
git config user.email "BrunoGzr@users.noreply.github.com"

git branch -m main 2>/dev/null || true

git add -A
git commit -m "Initial commit: static site generator and generated site"

git remote add origin https://github.com/BrunoGzr/StaticPages.git 2>/dev/null \
  || git remote set-url origin https://github.com/BrunoGzr/StaticPages.git

GIT_TERMINAL_PROMPT=0 git push -u origin main
