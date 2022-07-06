# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for CreateAttestor
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-binaryauthorization


# [START binaryauthorization_v1_generated_BinauthzManagementServiceV1_CreateAttestor_sync]
from google.cloud import binaryauthorization_v1


def sample_create_attestor():
    # Create a client
    client = binaryauthorization_v1.BinauthzManagementServiceV1Client()

    # Initialize request argument(s)
    attestor = binaryauthorization_v1.Attestor()
    attestor.user_owned_grafeas_note.note_reference = "note_reference_value"
    attestor.name = "name_value"

    request = binaryauthorization_v1.CreateAttestorRequest(
        parent="parent_value",
        attestor_id="attestor_id_value",
        attestor=attestor,
    )

    # Make the request
    response = client.create_attestor(request=request)

    # Handle the response
    print(response)

# [END binaryauthorization_v1_generated_BinauthzManagementServiceV1_CreateAttestor_sync]
