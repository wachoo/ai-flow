<!--
Copyright 2022 The AI Flow Authors.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

<template>
  <page-header-wrapper>
    <a-card :bordered="false">
      <div class="table-page-search-wrapper">
        <a-form layout="inline">
          <a-row :gutter="48">
            <a-col :md="8" :sm="24">
              <a-form-item label="Workflow Execution ID">
                <a-input v-model="queryParam.workflow_execution_id" placeholder=""/>
              </a-form-item>
            </a-col>
            <a-col :md="!advanced && 8 || 24" :sm="24">
              <span class="table-page-search-submitButtons" :style="advanced && { float: 'right', overflow: 'hidden' } || {} ">
                <a-button type="primary" @click="$refs.table.refresh(true)">Query</a-button>
                <a-button style="margin-left: 8px" @click="() => this.queryParam = {}">Reset</a-button>
              </span>
            </a-col>
          </a-row>
        </a-form>
      </div>
      <s-table
        ref="table"
        size="default"
        rowKey="key"
        :columns="columns"
        :data="loadData"
        showPagination="auto"
      >
        <span slot="_properties" slot-scope="text">
          <ellipsis :length="32" tooltip>{{ text }}</ellipsis>
        </span>
        <span slot="_execution_label" slot-scope="text">
          <ellipsis :length="32" tooltip>{{ text }}</ellipsis>
        </span>
        <span slot="action" slot-scope="text, record">
          <template>
            <a @click="handleLog(record)">Log</a>
          </template>
        </span>
      </s-table>
    </a-card>
    <a-card :bordered="false">
      <span>Version: <a :href="'https://pypi.org/project/ai-flow/'+version" target="_blank">{{ version }}</a></span>
    </a-card>
  </page-header-wrapper>
</template>

<script>
import moment from 'moment'
import { STable, Ellipsis } from '@/components'
import { getJobExecutions, getVersion } from '@/api/manage'

function formateDate (date, fmt) {
  if (/(Y+)/.test(fmt)) {
    fmt = fmt.replace(RegExp.$1, date.getFullYear() + '')
  }
  const o = {
    'M+': date.getMonth() + 1,
    'd+': date.getDate(),
    'h+': date.getHours(),
    'm+': date.getMinutes(),
    's+': date.getSeconds()
  }
  for (const k in o) {
    if (new RegExp(`(${k})`).test(fmt)) {
      const str = o[k] + ''
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? str : padLeftZero(str))
    }
  }
  return fmt
}

function padLeftZero (str) {
  return ('00' + str).substr(str.length)
}

const columns = [
  {
    title: 'Job Execution ID',
    dataIndex: '_job_execution_id'
  },
  {
    title: 'Job Name',
    dataIndex: '_job_name'
  },
  {
    title: 'Status',
    dataIndex: '_status'
  },
  {
    title: 'Properties',
    dataIndex: '_properties',
    scopedSlots: { customRender: '_properties' }
  },
  {
    title: 'Execution Label',
    dataIndex: '_execution_label',
    scopedSlots: { customRender: '_execution_label' }
  },
  {
    title: 'Start Date',
    dataIndex: '_start_date',
    customRender: (t) => formateDate(new Date(parseInt(t)), 'YYYY-MM-dd hh:mm')
  },
  {
    title: 'End Date',
    dataIndex: '_end_date',
    customRender: (t) => formateDate(new Date(parseInt(t)), 'YYYY-MM-dd hh:mm')
  },
  {
    title: 'Action',
    dataIndex: 'action',
    width: '150px',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'JobExecution',
  components: {
    STable,
    Ellipsis
  },
  data () {
    this.columns = columns
    return {
      confirmLoading: false,
      advanced: false,
      queryParam: {},
      loadData: parameter => {
        const requestParameters = Object.assign({}, parameter, this.queryParam)
        console.log('loadData request parameters:', requestParameters)
        return getJobExecutions(requestParameters)
          .then(res => {
            console.log(res)
            return res
          })
      },
      version: ''
    }
  },
  mounted () {
    this.getAIFlowVersion()
  },
  methods: {
    handleLog (record) {
      if (record._job_type === 'bash' || record._job_type === 'python' || record._job_type === 'flink') {
        window.open(`/job-execution/log?workflow_execution_id=${encodeURIComponent(this.queryParam.workflow_execution_id)}&job_name=${encodeURIComponent(record._job_name)}&job_type=${encodeURIComponent(record._job_type)}&job_execution_id=${encodeURIComponent(record._job_execution_id)}`, '_blank')
      } else {
        alert(`Viewing logs of ${record._job_type} type of job is not supported.`)
      }
    },
    resetSearchForm () {
      this.queryParam = {
        date: moment(new Date())
      }
    },
    getAIFlowVersion () {
      getVersion()
        .then(res => {
          this.version = res
        })
    }
  }
}
</script>
