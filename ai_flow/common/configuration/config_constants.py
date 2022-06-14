#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from .configuration import get_client_configuration, get_server_configuration
from .helpers import get_aiflow_home

CLIENT_CONF = get_client_configuration()
SERVER_CONF = get_server_configuration()

# Server Config

LOG_DIR = SERVER_CONF.get_str('log_dir', fallback='/tmp')

RPC_PORT = SERVER_CONF.get_str('rpc_port', fallback=50051)

INTERNAL_RPC_PORT = SERVER_CONF.get_str('internal_rpc_port', fallback=50000)

REST_PORT = SERVER_CONF.get_int('rest_port', fallback=8000)

METADATA_BACKEND_URI = SERVER_CONF.get_str('metadata_backend_uri',
                                           fallback='sqlite:///' + get_aiflow_home() + '/aiflow.db')

HISTORY_RETENTION = SERVER_CONF.get_str('history_retention', fallback='30d')

NOTIFICATION_SERVER_URI = SERVER_CONF.get_str('notification_server_uri', fallback='127.0.0.1:50052')

TASK_EXECUTOR = SERVER_CONF.get_str('task_executor', fallback='local')

TASK_EXECUTOR_HEARTBEAT_CHECK_INTERVAL = SERVER_CONF.get_int('task_executor_heartbeat_check_interval', fallback=10)

TASK_HEARTBEAT_TIMEOUT = SERVER_CONF.get_int('task_heartbeat_timeout', fallback=60)

TASK_HEARTBEAT_INTERVAL = SERVER_CONF.get_int('task_heartbeat_interval', fallback=10)

EXECUTE_TASKS_IN_NEW_INTERPRETER = SERVER_CONF.get_bool('execute_tasks_in_new_interpreter', fallback=False)

LOCAL_TASK_EXECUTOR_PARALLELISM = SERVER_CONF.get_int('local_executor_parallelism', fallback=10)

SQLALCHEMY_POOL_ENABLED = SERVER_CONF.get_bool('sql_alchemy_pool_enabled', fallback=True)

SQLALCHEMY_POOL_SIZE = SERVER_CONF.get_int('sql_alchemy_pool_size', fallback=5)

SQLALCHEMY_MAX_OVERFLOW = SERVER_CONF.get_int('sql_alchemy_max_overflow', fallback=10)

K8S_TASK_EXECUTOR_CONFIG = SERVER_CONF.get('k8s_executor_config', fallback={})

# Client Config

SERVER_ADDRESS = CLIENT_CONF.get_str('server_address', fallback='127.0.0.1:50051')


BLOB_MANAGER_DEFAULT_VALUE = {
    'blob_manager_class': 'ai_flow.blob_manager.impl.local_blob_manager.LocalBlobManager',
    'blob_manager_config': {
        'root_directory': '/tmp'
    }
}
BLOB_MANAGER = CLIENT_CONF.get('blob_manager', fallback=BLOB_MANAGER_DEFAULT_VALUE)