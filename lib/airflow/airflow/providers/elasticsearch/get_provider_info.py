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
def get_provider_info():
    return {
        'package-name': 'apache-airflow-providers-elasticsearch',
        'name': 'Elasticsearch',
        'description': '`Elasticsearch <https://https//www.elastic.co/elasticsearch>`__\n',
        'versions': ['1.0.0'],
        'integrations': [
            {
                'integration-name': 'Elasticsearch',
                'external-doc-url': 'https://www.elastic.co/elasticsearch',
                'tags': ['software'],
            }
        ],
        'hooks': [
            {
                'integration-name': 'Elasticsearch',
                'python-modules': ['airflow.providers.elasticsearch.hooks.elasticsearch'],
            }
        ],
        'hook-class-names': ['airflow.providers.elasticsearch.hooks.elasticsearch.ElasticsearchHook'],
    }