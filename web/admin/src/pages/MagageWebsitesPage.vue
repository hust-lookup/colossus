<template>
  <div class="q-pa-md">
    <q-table
      flat
      bordered
      title="Websites"
      :rows="rows"
      :columns="columns"
      row-key="name"
    >
      <template v-slot:body-cell-action="props">
        <q-td :props="props">
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
        <span class="text-h6">{{ form_action_name }} Website</span>
        <q-form @submit="onSubmit">
          <q-card-section>
            <q-input
              filled
              v-model="form_web_name"
              label="Website name"
              stack-label
              hint="Website name"
            />
          </q-card-section>
          <q-card-section>
            <q-input
              filled
              v-model="form_web_url"
              label="Website url"
              stack-label
              hint="Website url"
            />
          </q-card-section>
          <q-card-section>
            <q-select
              filled
              v-model="form_status"
              label="Status"
              stack-label
              :options="statusOptions"
              behavior="menu"
            ></q-select>
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
import { collection, getDocs, doc, deleteDoc, addDoc, updateDoc } from 'firebase/firestore'
import { db } from '../firebase' // Đảm bảo bạn đã xuất db từ firebase.js

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

export default {
  setup() {
    const rows = ref([]) // Chứa dữ liệu lấy từ Firestore
    const selected = ref(null)
    const form_action_name = ref(null)
    const form_web_name = ref(null)
    const form_web_url = ref(null)
    const form_status = ref(null)
    const updateDialog = ref(false)
    var newData = {
      id:"",
      webName: '',
      webUrl: '',
      status: '',
    }
    // Lấy dữ liệu từ Firestore
    const fetchData = async () => {
      try {
        const querySnapshot = await getDocs(collection(db, 'websites'))
        rows.value = querySnapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
        }))
      } catch (error) {
        console.error('Error fetching data: ', error)
      }
    }

    // Gọi hàm fetchData khi component được mount
    onMounted(() => {
      fetchData()
    })

    const onEdit = (row) => {
      form_action_name.value = 'edit'
      form_web_name.value = row.name
      form_web_url.value = row.url
      form_status.value = row.status
      updateDialog.value = true
      selected.value = row.id
    }

    const onDelete = async (row) => {
      const confirmDelete = window.confirm(`Are you sure you want to delete '${row.name}'?`)
      if (confirmDelete) {
        try {
          await deleteDoc(doc(db, 'websites', row.id)) // Xóa document dựa trên ID
          rows.value = rows.value.filter((item) => item.id !== row.id) // Cập nhật danh sách rows
          console.log(`Deleted row - '${row.name}'`)
        } catch (error) {
          console.error('Error deleting document: ', error)
        }
      }
    }
    const onCreate = () => {
      form_action_name.value = 'New'
      newData.id = ""
      updateDialog.value = true
    }

    const onSubmit = async () => {
      newData = {
        webName: form_web_name.value,
        webUrl: form_web_url.value,
        status: form_status.value,
      }
      if (form_action_name.value == 'New') {
        try {
          const docRef = await addDoc(collection(db, 'websites'), {
            name: newData.webName,
            url: newData.webUrl,
            status: newData.status,
            create_at: new Date().toISOString(),
          })
          console.log('Document written with ID: ', docRef.id)
        } catch (error) {
          console.error('Error adding document: ', error)
        }
      } else {
        try {
          const docRef = doc(db, 'websites', selected.value)
          await updateDoc(docRef, {
            name: newData.webName,
            url: newData.webUrl,
            status: newData.status,
            create_at: newData.create_at || new Date().toISOString(),
          })
          console.log('Document updated with ID: ', selected.value)
        } catch (error) {
          console.error('Error updating document: ', error)
        }
      }
      window.location.reload();
    }
    return {
      selected,
      columns,
      rows,
      onEdit,
      onDelete,
      onCreate,
      onSubmit,
      statusOptions: ['Active', 'Disable'],
      form_action_name,
      form_web_name,
      form_web_url,
      form_status,
      updateDialog,
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
