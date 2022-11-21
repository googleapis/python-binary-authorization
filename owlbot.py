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

import json
from pathlib import Path
import shutil

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

clean_up_generated_samples = True

# Load the default version defined in .repo-metadata.json.
default_version = json.load(open(".repo-metadata.json", "rt")).get(
    "default_version"
)

for library in s.get_staging_dirs(default_version):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    # Rename package to 'google-cloud-binary-authorization'
    # Remove once cl/490002122 is submitted
    s.replace(
        [library / "google/**/*.py", library / "tests/**/*.py"],
        "google-cloud-binaryauthorization",
        "google-cloud-binary-authorization",
    )

    if library.name == "v1":
        # Fix import of grafeas
        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "from grafeas.v1",
            "from grafeas.grafeas_v1",
        )

        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "from grafeas.grafeas_v1 import attestation_pb2",
            "from grafeas.grafeas_v1.types import attestation",
        )

        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "from grafeas.grafeas_v1 import common_pb2",
            "from grafeas.grafeas_v1.types import common",
        )

        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "message=attestation_pb2",
            "message=attestation",
        )

        s.replace(
            [library / "google/**/*.py", library / "tests/**/*.py"],
            "grafeas.v1.attestation_pb2.AttestationOccurrence",
            "grafeas.grafeas_v1.types.attestation.AttestationOccurrence",
        )
    s.move(library, excludes=["setup.py", "**/gapic_version.py"])
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=100,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc", ".github/release-please.yml"])

python.py_samples(skip_readmes=True)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "format"], cwd=noxfile.parent, hide_output=False)
