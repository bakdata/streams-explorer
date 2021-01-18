#!/usr/bin/env bash

(cd backend && python create_openapi_docs.py)

(cd frontend && npm run generate-fetcher)

CHANGED_UNSTAGED=$(git update-index --refresh)

if [[ $CHANGED_UNSTAGED == *"fetchers.tsx"* ]]
then
  printf "\n"
  printf "ERROR: Frontend API fetchers are not up to date with the API. Please run:\n"
  printf "\n"
  printf "\$ (cd backend && python create_openapi_docs.py)\n\$ (cd frontend && npm run generate-fetcher)\n"
  exit 1
fi
