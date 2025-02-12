# Copyright 2022 The AI Flow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from notification_service.storage.in_memory.memory_event_storage import MemoryEventStorage
from notification_service.server.server import NotificationServer
from notification_service.rpc.service import NotificationService


def run_server():
    storage = MemoryEventStorage()
    master = NotificationServer(service=NotificationService(storage), port=50051)
    master.run(is_block=True)


if __name__ == '__main__':
    run_server()
