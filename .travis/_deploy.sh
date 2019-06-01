#!/bin/sh

set -e

[ -z "${GITHUB_PAT}" ] && exit 0
[ "${TRAVIS_BRANCH}" != "master" ] && exit 0

git config --global user.email "${GIT_EMAIL}"
git config --global user.name "${GIT_USERNAME}"

if [ -d public ]; then

    # deploy site to repo
    git clone --depth 1 --branch gh-pages --single-branch https://${GITHUB_PAT}@github.com/${SITE_REPO}.git site
    cd site
    cp -r ../public/* ./

    NOW=$(date +"%Y-%m-%d %H:%M:%S %z")
    git add --all *
    git commit -m "Roster updated: ${NOW}" || true
    git push -q origin master

fi
