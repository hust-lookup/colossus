<template>
  <div class="q-pa-md">
    <q-table
      flat
      bordered
      title="Websites"
      :rows="rows"
      :columns="columns"
      row-key="name"
      :selected-rows-label="getSelectedString"
      selection="multiple"
      v-model:selected="selected"
    >
      <template v-slot:body-cell-action="props">
        <q-td :props="props">
          <q-btn round flat icon="mode_edit" @click="onEdit(props.row)"><q-tooltip> Edit </q-tooltip></q-btn>
          <q-btn round flat icon="delete" @click="onDelete(props.row)"><q-tooltip> Delete </q-tooltip></q-btn>
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
  { name: 'create_at', label: 'Create at', field: 'create_at', align: 'left' },
  { name: 'action', label: 'Action', align: 'center' },
]

const rows = [
  {
    name: 'Google',
    url: 'https://www.google.com',
    status: 'Active',
    create_at: '2024-01-15T08:45:00Z',
  },
  {
    name: 'Facebook',
    url: 'https://www.facebook.com',
    status: 'Active',
    create_at: '2024-02-20T09:30:00Z',
  },
  {
    name: 'Amazon',
    url: 'https://www.amazon.com',
    status: 'Inactive',
    create_at: '2024-03-10T12:00:00Z',
  },
  {
    name: 'Twitter',
    url: 'https://www.twitter.com',
    status: 'Active',
    create_at: '2024-04-05T14:25:00Z',
  },
  {
    name: 'LinkedIn',
    url: 'https://www.linkedin.com',
    status: 'Pending',
    create_at: '2024-05-18T16:40:00Z',
  },
]

export default {
  setup() {
    const selected = ref([])
    const onEdit = (row) => {
      console.log(`Editing row - '${row.name}'`)
    }

    const onDelete = (row) => {
      console.log(`Deleting row - '${row.name}'`)
    }

    return {
      selected,
      columns,
      rows,
      onEdit,
      onDelete,

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