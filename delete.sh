#!/bin/bash

set -euo pipefail
export AWS_PAGER=""

APP_NAME="devops-midterm-app"
REGION="us-east-1"

echo "🔍 Fetching list of active Elastic Beanstalk environments..."
ENV_LIST=$(aws elasticbeanstalk describe-environments \
  --application-name "$APP_NAME" \
  --region "$REGION" \
  --query "Environments[?Status!='Terminated'].EnvironmentName" \
  --output text)

if [ -z "$ENV_LIST" ]; then
  echo "✅ No active environments found."
else
  echo "🧨 Terminating environments: $ENV_LIST"
  for ENV in $ENV_LIST; do
    echo "⏳ Terminating environment: $ENV"
    aws elasticbeanstalk terminate-environment \
      --environment-name "$ENV" \
      --region "$REGION" || echo "⚠️ Failed to terminate environment $ENV"
  done
fi

# OPTIONAL: Uncomment this block if you also want to delete the application itself
echo "🗑️ Deleting application: $APP_NAME"
aws elasticbeanstalk delete-application \
    --application-name "$APP_NAME" \
    --region "$REGION"

echo "✅ Done."