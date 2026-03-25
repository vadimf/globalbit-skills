#!/bin/bash
# gws-auth — Wrapper for gws CLI that auto-refreshes OAuth token
# Usage: gws-auth <gws args...>
# Uses the same OAuth client as google-docs-mcp

# ⚠️ Set these from your Google Cloud Console OAuth credentials
# or read from environment variables
CLIENT_ID="${GWS_CLIENT_ID:?Set GWS_CLIENT_ID environment variable}"
CLIENT_SECRET="${GWS_CLIENT_SECRET:?Set GWS_CLIENT_SECRET environment variable}"
TOKEN_FILE="$HOME/token.json"
CACHE_FILE="$HOME/.config/gws/cached_token.json"

# Read refresh token
REFRESH_TOKEN=$(python3 -c "import json; print(json.load(open('$TOKEN_FILE'))['refresh_token'])")

# Check if cached token is still valid (less than 50 minutes old)
if [ -f "$CACHE_FILE" ]; then
  CACHED_AGE=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE") ))
  if [ "$CACHED_AGE" -lt 3000 ]; then
    ACCESS_TOKEN=$(python3 -c "import json; print(json.load(open('$CACHE_FILE'))['access_token'])")
  fi
fi

# Refresh if needed
if [ -z "$ACCESS_TOKEN" ]; then
  RESPONSE=$(curl -s -X POST https://oauth2.googleapis.com/token \
    -d "client_id=$CLIENT_ID" \
    -d "client_secret=$CLIENT_SECRET" \
    -d "refresh_token=$REFRESH_TOKEN" \
    -d "grant_type=refresh_token")
  
  ACCESS_TOKEN=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
  
  if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" = "None" ]; then
    echo "Error: Failed to refresh token" >&2
    echo "$RESPONSE" >&2
    exit 1
  fi
  
  mkdir -p "$(dirname "$CACHE_FILE")"
  echo "$RESPONSE" > "$CACHE_FILE"
fi

# Run gws with the token
GOOGLE_WORKSPACE_CLI_TOKEN="$ACCESS_TOKEN" gws "$@"
