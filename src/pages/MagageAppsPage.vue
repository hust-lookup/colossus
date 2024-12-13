<template>
  <div class="q-pa-md">
    <q-table
      flat
      bordered
      title="Apps"
      :rows="rows"
      :columns="columns"
      row-key="name"
      :selected-rows-label="getSelectedString"
      selection="multiple"
      v-model:selected="selected"
    >
      <template v-slot:body-cell-action="props">
        <q-td :props="props">
          <q-btn round flat icon="key" @click="onViewCredentials(props.row)"><q-tooltip> View Credentials </q-tooltip></q-btn>
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
    style: 'width: 80%;',
  },
  { name: 'action', label: 'Action', align: 'center' },
]

const rows = [
  {
    name: 'Shoppe',
  },
  {
    name: 'Lazada',
  },
  {
    name: 'Amazon',
  },
  {
    name: 'Taobao',
  },
  {
    name: 'TikTok Shop',
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

    const onViewCredentials = (row) => {
      console.log(`Deleting row - '${row.name}'`)
    }

    return {
      selected,
      columns,
      rows,
      onEdit,
      onDelete,
      onViewCredentials,

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
