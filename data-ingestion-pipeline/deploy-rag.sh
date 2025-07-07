#!/bin/sh

#
# login with ADC
gcloud auth application-default login

# Get the ID of the currently configured gcloud project
PROJECT_ID=$(gcloud config get-value project)

# Get the project number for that project
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")

# Grant the AI Platform Admin role to the default Compute Engine service account
# for the *current* project.
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/aiplatform.admin" --quiet

cd rag_corpus_deployment || exit
gcloud builds submit --config cloudbuild.yaml




