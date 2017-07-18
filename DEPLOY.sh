#!/bin/bash
rm -rf backend/www
cp -r frontend/app backend/www
$1/gcloud --project modular-security-system app deploy backend/app.yaml pubsub/app.yaml
