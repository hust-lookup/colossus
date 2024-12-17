<template>
  <div class="q-pa-md">
    <q-table
      flat
      bordered
      title="Models"
      :rows="rows"
      :columns="columns"
      row-key="name"
      :selected-rows-label="getSelectedString"
      selection="multiple"
      v-model:selected="selected"
    >
      <template v-slot:body-cell-action="props">
        <q-td :props="props">
          <q-btn round flat icon="rocket" @click="onViewDeployment(props.row)"><q-tooltip> View Deployment </q-tooltip></q-btn>
          <q-btn round flat icon="mode_edit" @click="onEdit(props.row)"><q-tooltip> Edit </q-tooltip></q-btn>
          <q-btn round flat icon="delete" @click="onDelete(props.row)"><q-tooltip> Delete </q-tooltip></q-btn>
          <q-btn round flat icon="download" @click="onDownload(props.row)"><q-tooltip> Download </q-tooltip></q-btn>
        </q-td>
      </template>
    </q-table>
    <div class="q-mt-md">Selected: {{ JSON.stringify(selected) }}</div>
  </div>
</template>

<script>
import { ref } from 'vue'

const columns = [
  {
    name: 'name',
    required: true,
    label: 'Name',
    align: 'left',
    field: (row) => row.name,
    format: (val) => `${val}`,
    sortable: true,
  },
  { name: 'url', label: 'Url', field: 'url', sortable: true, align: 'left' },
  { name: 'status', label: 'Status', field: 'status', align: 'left' },
  { name: 'tag', label: 'Tag', field: 'tag', align: 'left' },
  { name: 'version', label: 'Version', field: 'version', align: 'left' },
  { name: 'create_at', label: 'Create at', field: 'create_at', align: 'left' },
  { name: 'action', label: 'Action', align: 'center' },
]

const rows = [
  {
    name: 'Project Alpha',
    url: 'https://www.alpha.com',
    status: 'Active',
    tag: 'Web',
    version: '1.0.0',
    create_at: '2024-01-15',
  },
  {
    name: 'Project Beta',
    url: 'https://www.beta.com',
    status: 'Inactive',
    tag: 'Mobile',
    version: '2.3.1',
    create_at: '2023-10-05',
  },
  {
    name: 'Project Gamma',
    url: 'https://www.gamma.com',
    status: 'Active',
    tag: 'Desktop',
    version: '3.1.0',
    create_at: '2024-02-20',
  },
  {
    name: 'Project Delta',
    url: 'https://www.delta.com',
    status: 'Active',
    tag: 'Web',
    version: '4.0.2',
    create_at: '2024-03-11',
  },
  {
    name: 'Project Epsilon',
    url: 'https://www.epsilon.com',
    status: 'Inactive',
    tag: 'Mobile',
    version: '1.8.4',
    create_at: '2023-09-22',
  },
]

export default {
  setup() {
    const selected = ref([])
    const onViewDeployment = (row) => {
      console.log(`Editing row - '${row.name}'`)
    }

    const onDelete = (row) => {
      console.log(`Deleting row - '${row.name}'`)
    }

    const onDownload = (row) => {
      console.log(`Download row - '${row.name}'`)
    }

    const onEdit = (row) => {
      console.log(`Editing row - '${row.name}'`)
    }
    return {
      selected,
      columns,
      rows,
      onViewDeployment,
      onDelete,
      onDownload,
      onEdit,

      getSelectedString() {
        return selected.value.length === 0
          ? ''
          : `${selected.value.length} record${selected.value.length > 1 ? 's' : ''} selected of ${rows.length}`
      },
    }
  },
}
</script>

<style lang="scss">
.q-btn:hover {
  color: $primary;
}
</style>
