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
          <q-btn round flat icon="key" @click="onViewCredentials(props.row)">
            <q-tooltip>View Credentials</q-tooltip>
          </q-btn>
          <q-btn round flat icon="mode_edit" @click="onEdit(props.row)">
            <q-tooltip>Edit</q-tooltip>
          </q-btn>
          <q-btn round flat icon="delete" @click="onDelete(props.row)">
            <q-tooltip>Delete</q-tooltip>
          </q-btn>
        </q-td>
      </template>
    </q-table>
    <q-btn class="q-mt-md" color="primary" label="Add new" @click="onCreate()" />
    <!-- Dialog -->
    <q-dialog persistent v-model="updateDialog">
      <q-card class="q-pa-lg">
        <span class="text-h6">{{ form_action_name }} App</span>
        <q-form @submit="onSubmit">
          <q-card-section>
            <q-input filled v-model="form_app_name" label="App name" stack-label />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="primary" v-close-popup></q-btn>
            <q-btn flat type="submit" label="Confirm" color="primary" v-close-popup></q-btn>
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { collection, getDocs, addDoc, doc, updateDoc, deleteDoc } from 'firebase/firestore'
import { db } from '../firebase'

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

export default {
  setup() {
    const rows = ref([]) // Dữ liệu từ Firestore
    const selected = ref([])
    const form_action_name = ref(null)
    const form_app_name = ref(null)
    const selectedId = ref(null)
    const updateDialog = ref(false)
    var appName = ''
    // Hàm lấy dữ liệu từ Firestore
    const fetchData = async () => {
      try {
        const querySnapshot = await getDocs(collection(db, 'apps'))
        rows.value = querySnapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
        }))
      } catch (error) {
        console.error('Error fetching data: ', error)
      }
    }

    // Hàm tạo mới ứng dụng
    const onCreate = () => {
      form_action_name.value = 'New'
      selectedId.value = ''
      updateDialog.value = true
    }

    // Hàm cập nhật ứng dụng
    const onEdit = (row) => {
      form_action_name.value = 'Edit'
      form_app_name.value = row.name
      selectedId.value = row.id
      updateDialog.value = true
    }

    const onSubmit = async () => {
      appName = form_app_name.value
      if (form_action_name.value == 'New') {
        try {
          const docRef = await addDoc(collection(db, 'apps'), {
            name: appName,
            created_at: new Date().toISOString(),
          })
          console.log('Document written with ID: ', docRef.id)
        } catch (error) {
          console.error('Error adding document: ', error)
        }
      } else {
        try {
          const docRef = doc(db, 'apps', selectedId.value)
          await updateDoc(docRef, {
            name: appName,
          })
          console.log('Document updated with ID: ', selectedId.value)
        } catch (error) {
          console.error('Error updating document: ', error)
        }
      }
      window.location.reload()
    }

    // Hàm xóa ứng dụng
    const onDelete = async (row) => {
      const confirmDelete = window.confirm(`Are you sure you want to delete '${row.name}'?`)
      if (confirmDelete) {
        try {
          await deleteDoc(doc(db, 'apps', row.id))
          rows.value = rows.value.filter((item) => item.id !== row.id)
          console.log(`Deleted row - '${row.name}'`)
        } catch (error) {
          console.error('Error deleting document: ', error)
        }
      }
    }

    // Hàm xem thông tin credentials
    const onViewCredentials = (row) => {
      console.log(`Viewing credentials for row - '${row.name}'`)
      // Bạn có thể mở một modal hoặc chuyển trang để hiển thị thông tin chi tiết ở đây
    }

    // Gọi hàm fetchData khi component được mount
    onMounted(() => {
      fetchData()
    })

    return {
      selected,
      columns,
      rows,
      onCreate,
      onEdit,
      onDelete,
      onViewCredentials,
      form_action_name,
      form_app_name,
      selectedId,
      updateDialog,
      onSubmit,

      getSelectedString() {
        return selected.value.length === 0
          ? ''
          : `${selected.value.length} record${selected.value.length > 1 ? 's' : ''} selected of ${rows.value.length}`
      },
    }
  },
}
</script>

<style lang="scss">
.q-btn:hover {
  color: $primary;
}
.q-card {
  width: 30%;
}
</style>
