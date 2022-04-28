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

"""Converts SQL to audit SQL.

  Typical usage example:

  sql_exec = ETLAudit.get_sql_statment(
      execution_context= self.execution_context,
      task_config=self.task_config)
"""

import pathlib
from typing import Optional
from grizzly.grizzly_typing import TGrizzlyOperator
from grizzly.grizzly_typing import TGrizzlyTaskConfig
import jinja2


class ETLAudit:
  """ETLAudit converts SQL to audit SQL and add columns if needed.

  If task yaml file  contains tag
    target_audit_indicator: Y
  then ETLAudit will be used in Extractors plugins.

  Attributes:
    supported_write_mode (list(str)): List of support write modes.
    _add_audit_columns_jinja_template (str): Reference to audit column JINJA2
      template.
    _select_audit_jinja_template (str): Reference to Select query audit JINJA2
      template.
  """

  supported_write_mode = ["WRITE_APPEND", "WRITE_EMPTY", "WRITE_TRUNCATE"]

  # Templates used in audited objects
  _add_audit_columns_jinja_template = "audit/add_audit_columns.sql.jinja2"
  _select_audit_jinja_template = "audit/select_audit.sql.jinja2"

  @classmethod
  def get_sql_statement(cls,
                        execution_context: TGrizzlyOperator,
                        task_config: TGrizzlyTaskConfig,
                        sql: Optional[str] = None) -> str:
    """Return SQL stetment with audit values.

    This method used to inject additional columns
    into user's sql to execute in BQ.

    Args:
      execution_context (TGrizzlyOperator): execution context of task
      task_config (TGrizzlyTaskConfig): task configuration
      sql (str, optional): sql text for execution

    Returns:
      SQL statment with injected audit columns.
    """

    template_folder = pathlib.Path("/home/airflow/gcs/plugins/templates")
    data = {"sql": sql}

    exec_template = template_folder / cls._select_audit_jinja_template

    exec_query = jinja2.Template(exec_template.read_text()).render(
        task_config=task_config,
        execution_context=execution_context,
        data=data)

    return exec_query

  @classmethod
  def get_column_statement(cls,
                           execution_context: TGrizzlyOperator,
                           task_config: TGrizzlyTaskConfig) -> str:
    """Return SQL stetment - DDL statement for adding new columns.

    This method returns safe DDL script to add new audit columns into table
    alter table table_1 add if not exists sys_job_id integer.

    Args:
      execution_context (TGrizzlyOperator): execution context of task
      task_config (TGrizzlyTaskConfig): task configuration

    Returns:
      safe DDL statement to add columns into the target table.
    """

    template_folder = pathlib.Path("/home/airflow/gcs/plugins/templates")
    dataset, table = task_config.target_table_name.split(".")
    data = {"dataset": dataset, "table": table}

    exec_template = template_folder / cls._add_audit_columns_jinja_template

    exec_query = jinja2.Template(exec_template.read_text()).render(
        task_config=task_config,
        execution_context=execution_context,
        data=data)

    return exec_query
