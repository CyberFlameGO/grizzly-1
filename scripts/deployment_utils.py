# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functionality for work with PROTO files."""
import datetime
import glob
import os
from typing import Any, Dict

import google.auth.transport.requests
from google.cloud import bigquery
from google.cloud.bigquery import Table
import proto
import yaml


class Utils:
  """Methods for work with files in PROTO format.

  This class is used by deployment scripts responsible for upload and deployment
  of DataCatalog and DLP configurations.
  """

  @classmethod
  def remove_files(cls, path: str, files_filter: str):
    """"Remove files."""

    deleted_files = []

    files = glob.glob(f'{path}/{files_filter}')
    for f in files:
      os.remove(f)
      print(f'Removed file: {f}')
      deleted_files.append(f)

    return deleted_files

  @classmethod
  def proto_save(cls, obj: proto.Message, class_message: Any,
                 file_name: str, path: str) -> str:
    """Save proto file."""

    f = open(f'{path}/{file_name}', 'w+')
    json_data = class_message.to_json(obj)
    f.write(json_data)
    f.close()

    return f'{path}/{file_name}'

  @classmethod
  def proto_load(cls, path: str, filter: str,
                 proto_class: Any) -> Dict[str, Any]:
    """Load file in proto format."""
    proto_messages = {}

    path = f'{path}/'

    for filename in glob.glob(os.path.join(path, filter)):
      with open(os.path.join(os.getcwd(), filename), 'r') as f:
        message: proto_class = proto_class.from_json(f.read())
        proto_messages[filename] = message

    return proto_messages

  @classmethod
  def yaml_load(cls, path: str, file_filter: str):
    """Load yaml file and return it."""
    files = cls.get_files_by_filter(path=path, file_filter=file_filter)

    res = {filename: cls.parse_yml_file(filename) for filename in files}

    return res

  @classmethod
  def get_files_by_filter(cls, path: str, file_filter: str):
    """Return files by path and filter."""
    walk_dir = path

    print('walk_dir = ' + walk_dir)

    # If your current working directory may change during
    # script execution, it's recommended to
    # immediately convert program arguments to an absolute path.
    # Then the variable root below will
    # be an absolute path as well. Example:
    walk_dir = os.path.abspath(walk_dir)
    print(f'walk_dir (absolute) = {walk_dir}/{file_filter}')

    files = glob.glob(f'{walk_dir}/{file_filter}', recursive=True)

    return files

  @classmethod
  def files_load(cls, path: str, file_filter: str):
    """Load files."""

    files = cls.get_files_by_filter(path=path, file_filter=file_filter)

    res = {filename: open(filename, 'rb').read().decode('utf-8')
           for filename in files}

    return res

  @classmethod
  def parse_yml_file(cls, yml_file):
    """Parsing yaml fiiles."""

    with open(yml_file) as f:
      yml_values = yaml.safe_load(f.read())
    return yml_values

  @classmethod
  def auth(cls, scopes=None):
    """Auth function."""

    if not scopes:
      scopes = ['https://www.googleapis.com/auth/cloud-platform']

    credentials, _ = google.auth.default(scopes=scopes)

    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)

  @classmethod
  def get_bq_client(cls, project):
    return bigquery.Client(project=project)


class BQUtils:
  """Provides basic functionality to work with BQ."""

  def __init__(self, gcp_project_id: str) -> None:
    Utils.auth()
    self.gcp_project_id = gcp_project_id
    self.bq_client = Utils.get_bq_client(project=self.gcp_project_id)
    pass

  def create_temp_table(self,
                        table_name: str,
                        table_schema) -> Table:
    """Create temorary table based on name."""

    suffix: str = datetime.datetime.now().strftime('%m%d%Y%H%M%S')
    table_name: str = f'{table_name}_{suffix}'
    ret: Table = self.create_table(table_name=table_name,
                                   table_schema=table_schema)

    return ret

  def create_table(self,
                   table_name: str,
                   table_schema,
                   exists_ok: bool = True) -> Table:
    """Create table."""

    table_name_ref = f'{self.gcp_project_id}.{table_name}'
    table: Table = bigquery.Table(table_ref=table_name_ref,
                                  schema=table_schema)
    ret: Table = self.bq_client.create_table(table=table,
                                             exists_ok=exists_ok)

    return ret


class ImportToolConfig:
  """Import tool configuration class."""

  def __init__(self,
               env,
               env_config_file,
               env_tag_name: str = 'GCP_ENVIRONMENT') -> None:
    """Initializing class.

    Args:
      env (str): environment name
      env_config_file (str): config file name with environments
      env_tag_name (str): the tag name with information about GCP Environment
    """
    self.env = env
    self.env_config_file = env_config_file

    self.gcp_environment_target = self._get_environment_configuration(
        env_configs_file=env_config_file,
        environment=env,
        env_tag_name=env_tag_name)

  def _get_environment_configuration(self,
                                     env_configs_file: str,
                                     environment: str,
                                     env_tag_name: str):
    """Getting the environment configuration."""

    env_config = Utils.parse_yml_file(f'{env_configs_file}')
    return env_config[environment][env_tag_name]
