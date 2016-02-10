#!/bin/sh

#New Relic
export NEW_RELIC_LICENSE_KEY="$(python $HOME/.profile.d/newrelic_license.py)"
echo "added environment variable NEW_RELIC_LICENSE_KEY with value: $NEW_RELIC_LICENSE_KEY"

export NEW_RELIC_APP_NAME="$(python $HOME/.profile.d/app_name.py)"
echo "added environment variable NEW_RELIC_APP_NAME with value: $NEW_RELIC_APP_NAME"

export NEW_RELIC_LOG="stdout"
echo "added environment variable NEW_RELIC_LOG with value: $NEW_RELIC_LOG"
