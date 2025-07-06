#!/bin/sh
gcloud auth application-default login
cd infra_deployment || exit

terraform init
terraform apply --auto-approve