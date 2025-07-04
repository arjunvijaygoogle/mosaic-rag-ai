#!/bin/sh
cd infra_deployment || exit

terraform init
terraform apply --auto-approve