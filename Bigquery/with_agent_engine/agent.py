# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.adk.agents.llm_agent import LlmAgent
from google.adk.auth.auth_credential import AuthCredentialTypes
from google.adk.tools.bigquery.bigquery_credentials import BigQueryCredentialsConfig
from google.adk.tools.bigquery.bigquery_toolset import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.adk.tools.bigquery.config import WriteMode
import google.auth

##EA Addition
import os
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
import warnings
from typing import Any, Dict, List, Optional
import typing
from google.adk.sessions import Session
from google.adk.events import Event
import random
import vertexai
from vertexai.preview.reasoning_engines import AdkApp
from google.cloud import storage
from google.genai.types import Blob
from google.genai.types import Part
import logging
import base64
import mimetypes
import asyncio
#import pdfplumber
import requests
import io
import json
# Load environment variables from .env file
#from dotenv import load_dotenv
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter
from vertexai import agent_engines
#from . import prompt
from google.adk.tools import google_search
#load_dotenv()


# Define the desired credential type.
# By default use Application Default Credentials (ADC) from the local
# environment, which can be set up by following
# https://cloud.google.com/docs/authentication/provide-credentials-adc.
CREDENTIALS_TYPE = None

# Define an appropriate application name
BIGQUERY_AGENT_NAME = "adk_sample_bigquery_agent"

##EA Addition
warnings.filterwarnings("ignore")
#GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
STORAGE_BUCKET = "gs://agent_experiment_staging"
GOOGLE_CLOUD_PROJECT = "agent-test-470019"
GOOGLE_CLOUD_LOCATION = "us-central1"
GOOGLE_GENAI_USE_VERTEXAI="FALSE"
#CHECK_ORDER_STATUS_ENDPOINT = os.environ["CHECK_ORDER_STATUS_ENDPOINT"]
STAGING_BUCKET = "gs://agent_experiment_staging"
#ROOT_AGENT_NAME = "trend_spotter_agent"
PROJECT_ID = GOOGLE_CLOUD_PROJECT
staging_bucket = STAGING_BUCKET
logger = logging.getLogger(__name__)

USER_ID = "user123"
SESSION_ID = "demo"
#PROPOSAL_DOCUMENT_FILE_NAME =  "proposal_document_for_user.pdf"
MODEL_NAME = "gemini-2.5-flash"
from fastapi import HTTPException

# Define BigQuery tool config with write mode set to allowed. Note that this is
# only to demonstrate the full capability of the BigQuery tools. In production
# you may want to change to BLOCKED (default write mode, effectively makes the
# tool read-only) or PROTECTED (only allows writes in the anonymous dataset of a
# BigQuery session) write mode.
tool_config = BigQueryToolConfig(
    write_mode=WriteMode.ALLOWED, application_name=BIGQUERY_AGENT_NAME
)

if CREDENTIALS_TYPE == AuthCredentialTypes.OAUTH2:
  # Initiaze the tools to do interactive OAuth
  # The environment variables OAUTH_CLIENT_ID and OAUTH_CLIENT_SECRET
  # must be set
  credentials_config = BigQueryCredentialsConfig(
      client_id=os.getenv("OAUTH_CLIENT_ID"),
      client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
  )
elif CREDENTIALS_TYPE == AuthCredentialTypes.SERVICE_ACCOUNT:
  # Initialize the tools to use the credentials in the service account key.
  # If this flow is enabled, make sure to replace the file path with your own
  # service account key file
  # https://cloud.google.com/iam/docs/service-account-creds#user-managed-keys
  creds, _ = google.auth.load_credentials_from_file("service_account_key.json")
  credentials_config = BigQueryCredentialsConfig(credentials=creds)
else:
  # Initialize the tools to use the application default credentials.
  # https://cloud.google.com/docs/authentication/provide-credentials-adc
  application_default_credentials, _ = google.auth.default()
  credentials_config = BigQueryCredentialsConfig(
      credentials=application_default_credentials
  )

bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, bigquery_tool_config=tool_config
)

# The variable name `root_agent` determines what your root agent is for the
# debug CLI
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name=BIGQUERY_AGENT_NAME,
    description=(
        "Agent to answer questions about BigQuery data and models and execute"
        " SQL queries."
    ),
    instruction="""\
        You are a data science agent with access to several BigQuery tools.
        Make use of those tools to answer the user's questions.
    """,
    tools=[bigquery_toolset],
)

##EA Addition
app = AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

vertexai.init(
        project=PROJECT_ID,
        location=GOOGLE_CLOUD_LOCATION,
        staging_bucket=STAGING_BUCKET,
    )

remote_app = agent_engines.create(
        app,
        requirements=[
            "google-cloud-aiplatform[agent_engines,adk]>=1.88",
            "google-adk",
            #"pysqlite3-binary",
            #"toolbox-langchain==0.1.0",
            #"pdfplumber",
            "google-cloud-aiplatform",
            #"cloudpickle==3.1.1",
            #"pydantic==2.10.6",
            #"pytest",
            #"overrides",
            #"scikit-learn",
            #"reportlab",
            "google-auth",
            "google-cloud-storage",
        ],
    )
