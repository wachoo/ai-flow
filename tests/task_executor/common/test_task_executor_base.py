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
import os
import time
import unittest
from unittest import mock

from ai_flow.common.util.db_util import session
from ai_flow.common.util.db_util.db_migration import init_db
from ai_flow.common.util.thread_utils import StoppableThread
from ai_flow.model.status import TaskStatus
from ai_flow.metadata.message import PersistentQueue
from ai_flow.model.action import TaskAction

from ai_flow.common.exception.exceptions import AIFlowException
from ai_flow.scheduler.schedule_command import TaskScheduleCommand
from ai_flow.model.task_execution import TaskExecutionKey
from ai_flow.task_executor.common.task_executor_base import TaskExecutorBase


class MockTaskExecutor(TaskExecutorBase):

    def start_task_execution(self, key: TaskExecutionKey):
        pass

    def stop_task_execution(self, key: TaskExecutionKey):
        pass

    def start(self):
        self.command_queue = PersistentQueue(maxsize=100)

    def stop(self):
        if not self.command_queue:
            raise AIFlowException("The executor should be started first!")


class TestTaskExecutorBase(unittest.TestCase):

    def setUp(self) -> None:
        self.file = 'test.db'
        self.db_uri = 'sqlite:///{}'.format(self.file)
        self._delete_db_file()
        init_db(self.db_uri)
        session.prepare_session(db_uri=self.db_uri)
        self.executor = MockTaskExecutor()
        self.executor.start()

    def tearDown(self) -> None:
        self._delete_db_file()
        self.executor.stop()
        session.clear_engine_and_session()

    def test_executor_not_started(self):
        command = TaskScheduleCommand(action=TaskAction.START,
                                      current_task_execution=TaskExecutionKey(1, 'task', 1),
                                      new_task_execution=None)
        with self.assertRaises(AIFlowException):
            executor = MockTaskExecutor()
            executor.schedule_task(command)

    @mock.patch('ai_flow.task_executor.common.task_executor_base.TaskExecutorBase._send_task_status_change')
    def test_schedule_task(self, mock_send):
        key = TaskExecutionKey(1, 'task', 1)
        command = TaskScheduleCommand(action=TaskAction.START,
                                      current_task_execution=key,
                                      new_task_execution=None)
        self.executor.schedule_task(command)
        mock_send.assert_called_once_with(task=key, status=TaskStatus.QUEUED)

        command = TaskScheduleCommand(action=TaskAction.STOP,
                                      current_task_execution=key,
                                      new_task_execution=None)
        self.executor.schedule_task(command)
        mock_send.assert_called_with(task=key, status=TaskStatus.STOPPING)

        command = TaskScheduleCommand(action=TaskAction.RESTART,
                                      current_task_execution=key,
                                      new_task_execution=None)
        self.executor.schedule_task(command)
        mock_send.assert_called_with(task=key, status=TaskStatus.RESTARTING)

    @mock.patch('ai_flow.task_executor.common.task_executor_base.TaskExecutorBase._send_task_status_change')
    def test__process_command(self, mock_send):
        try:
            command_processor = StoppableThread(target=self.executor._process_command)
            command_processor.start()

            key = TaskExecutionKey(1, 'task', 1)
            command = TaskScheduleCommand(action=TaskAction.START,
                                          current_task_execution=key,
                                          new_task_execution=None)
            self.executor.command_queue.put(command)
            command = TaskScheduleCommand(action=TaskAction.STOP,
                                          current_task_execution=key,
                                          new_task_execution=None)
            self.executor.command_queue.put(command)
            time.sleep(0.5)
            self.assertEqual(mock_send.call_count, 1)
        finally:
            command_processor.stop()

    @mock.patch('ai_flow.task_executor.common.task_executor_base.TaskExecutorBase._send_task_status_change')
    def test_process_restart_command(self, mock_send):
        try:
            command_processor = StoppableThread(target=self.executor._process_command)
            command_processor.start()
            key = TaskExecutionKey(1, 'task', 1)
            key_new = TaskExecutionKey(1, 'task', 2)
            command = TaskScheduleCommand(action=TaskAction.RESTART,
                                          current_task_execution=key,
                                          new_task_execution=key_new)
            self.executor.command_queue.put(command)
            time.sleep(0.5)
            self.assertEqual(mock_send.call_count, 1)
        finally:
            command_processor.stop()

    def _delete_db_file(self):
        if os.path.exists(self.file):
            os.remove(self.file)