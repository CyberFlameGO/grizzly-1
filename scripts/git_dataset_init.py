# Copyright 2022 Google LLC
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

"""Import git dataset."""
import argparse
import sys

from deployment_utils import BQUtils
from deployment_utils import ImportToolConfig
from grizzly.forecolor import ForeColor
from grizzly_git.config import CB_TRIGGER_EXECUTION_TABLE_NAME
from grizzly_git.config import CB_TRIGGER_EXECUTION_TABLE_SCHEMA
from grizzly_git.config import GIT_COMMITS_TABLE_NAME
from grizzly_git.config import GIT_COMMITS_TABLE_SCHEMA
from grizzly_git.config import GIT_DATASET
from grizzly_git.config import GIT_FILES_TABLE_NAME
from grizzly_git.config import GIT_FILES_TABLE_SCHEMA
from grizzly_git.config import GIT_FILES_VERSION_TABLE_NAME
from grizzly_git.config import GIT_FILES_VERSION_TABLE_SCHEMA
from grizzly_git.config import JOB_BUILD_TABLE_NAME
from grizzly_git.config import JOB_BUILD_TABLE_SCHEMA
from grizzly_git.config import SQL_CREATE_VW_JOB_GIT_FILES
from grizzly_git.config import SQL_CREATE_VW_SUBJECT_AREA_BUILD_FILES
from grizzly_git.config import SUBJECT_AREA_BUILD_TABLE_NAME
from grizzly_git.config import SUBJECT_AREA_BUILD_TABLE_SCHEMA
from grizzly_git.config import SUBJECT_AREA_TABLE_NAME
from grizzly_git.config import SUBJECT_AREA_TABLE_SCHEMA


def create_table(bq_uitls: BQUtils,
                 table_name: str,
                 table_schema: str) -> None:
  table_name = f'{GIT_DATASET}.{table_name}'
  bq_uitls.create_table(table_name=table_name, table_schema=table_schema)


def main(args: argparse.Namespace) -> None:
  """Import data catalog.

  Args:
    args (argparse.Namespace): arguments passed in the commandline
  """
  env = args.env.lower()
  env_config_file = args.env_config_file

  config = ImportToolConfig(env=env, env_config_file=env_config_file)

  bq_utils = BQUtils(gcp_project_id=config.gcp_environment_target)

  create_table(bq_uitls=bq_utils,
               table_name=GIT_COMMITS_TABLE_NAME,
               table_schema=GIT_COMMITS_TABLE_SCHEMA)
  create_table(bq_uitls=bq_utils,
               table_name=GIT_FILES_TABLE_NAME,
               table_schema=GIT_FILES_TABLE_SCHEMA)
  create_table(bq_uitls=bq_utils,
               table_name=GIT_FILES_VERSION_TABLE_NAME,
               table_schema=GIT_FILES_VERSION_TABLE_SCHEMA)
  create_table(bq_uitls=bq_utils,
               table_name=JOB_BUILD_TABLE_NAME,
               table_schema=JOB_BUILD_TABLE_SCHEMA)
  create_table(bq_uitls=bq_utils,
               table_name=CB_TRIGGER_EXECUTION_TABLE_NAME,
               table_schema=CB_TRIGGER_EXECUTION_TABLE_SCHEMA)
  create_table(bq_uitls=bq_utils,
               table_name=SUBJECT_AREA_TABLE_NAME,
               table_schema=SUBJECT_AREA_TABLE_SCHEMA)
  create_table(bq_uitls=bq_utils,
               table_name=SUBJECT_AREA_BUILD_TABLE_NAME,
               table_schema=SUBJECT_AREA_BUILD_TABLE_SCHEMA)

  sql = SQL_CREATE_VW_SUBJECT_AREA_BUILD_FILES.format(GIT_DATASET=GIT_DATASET)
  bq_utils.bq_client.query(sql).result()

  sql = SQL_CREATE_VW_JOB_GIT_FILES.format(GIT_DATASET=GIT_DATASET)
  bq_utils.bq_client.query(sql).result()


if __name__ == '__main__':
  try:
    # Construct the argument parser
    ap = argparse.ArgumentParser(
        description='Script used for SYNC/MERGE of DLP templates')
    # Add the arguments to the parser
    ap.add_argument(
        '-e',
        '--env',
        dest='env',
        required=True,
        help='Env of GCP project.')
    ap.add_argument(
        '-c',
        '--env_config_file',
        dest='env_config_file',
        required=True,
        help='Environment file')

    args_val = ap.parse_args()
    main(args=args_val)
  except:
    print(f'{ForeColor.RED}Unexpected error:{ForeColor.RESET}',
          sys.exc_info()[1])
    raise
