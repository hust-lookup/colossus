<template>
  <div class="q-pa-md">
    <q-table
      flat
      bordered
      title="Apps"
      :rows="rows"
      :columns="columns"
      row-key="name"
      v-model:selected="selected"
    />
    <div class="q-mt-md">Selected: {{ JSON.stringify(selected) }}</div>
  </div>
</template>

<script>

const columns = [
  {
    name: 'source',
    required: true,
    label: 'Source',
    align: 'left',
    field: (row) => row.source,
    format: (val) => `${val}`,
    sortable: true,
  },
  { name: 'target', label: 'Target', field: 'target', align: 'left' },
  { name: 'action', label: 'Action', field: 'action', align: 'left' },
  { name: 'tag', label: 'Tag', field: 'tag', align: 'left' },
  { name: 'status', label: 'Status', field: 'status', align: 'center' },
  { name: 'timestamp', label: 'Timestamp', field: 'timestamp', align: 'right' },

]

const rows = [
  {
    "source": "API v1",
    "target": "Database A",
    "action": "Sync",
    "tag": "Data Transfer",
    "status": "Success",
    "timestamp": "2024-12-05T10:00:00Z"
  },
  {
    "source": "API v2",
    "target": "Database B",
    "action": "Fetch",
    "tag": "Data Query",
    "status": "Failed",
    "timestamp": "2024-12-06T14:30:00Z"
  },
  {
    "source": "File Upload",
    "target": "Storage Service",
    "action": "Upload",
    "tag": "File Transfer",
    "status": "Success",
    "timestamp": "2024-12-06T15:00:00Z"
  },
  {
    "source": "API v3",
    "target": "Database C",
    "action": "Backup",
    "tag": "Data Backup",
    "status": "In Progress",
    "timestamp": "2024-12-07T08:45:00Z"
  },
  {
    "source": "Manual Entry",
    "target": "Internal System",
    "action": "Log",
    "tag": "User Input",
    "status": "Success",
    "timestamp": "2024-12-07T09:30:00Z"
  }
]


export default {
  setup() {

    return {
      columns,
      rows,
    }
  },
}
</script>

<style lang="scss">
.q-btn:hover {
  color: $primary;
}
</style>
