# Copyright 2020 Google LLC
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

import datetime
import os

from google.cloud import automl
import pytest

import delete_dataset

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
BUCKET_ID = "{}-lcm".format(PROJECT_ID)


@pytest.fixture(scope="function")
def create_dataset():
    client = automl.AutoMlClient()
    project_location = client.location_path(PROJECT_ID, "us-central1")
    display_name = "test_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    metadata = automl.types.TextExtractionDatasetMetadata()
    dataset = automl.types.Dataset(
        display_name=display_name, text_extraction_dataset_metadata=metadata
    )
    response = client.create_dataset(project_location, dataset)
    dataset_id = response.result().name.split("/")[-1]

    yield dataset_id


def test_delete_dataset(capsys, create_dataset):
    # delete dataset
    delete_dataset.delete_dataset(PROJECT_ID, create_dataset)
    out, _ = capsys.readouterr()
    assert "Dataset deleted." in out
