#!/bin/sh
# ./nameChg.sh
# https://devtut.github.io/git/rewriting-history-with-filter-branch.html

git filter-branch --env-filter '
WRONG_EMAIL="me@email.com"
NEW_NAME="rsa23770"
NEW_EMAIL="martin.lim@rsa.rohde-schwarz.com"

if [ "$GIT_COMMITTER_EMAIL" = "$WRONG_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$NEW_NAME"
    export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$WRONG_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$NEW_NAME"
    export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags -f