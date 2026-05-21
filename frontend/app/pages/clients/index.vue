<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-medium text-gray-900">Clients</h3>
      <AppButton @click="openCreateModal">
        Add New Client
      </AppButton>
    </div>

    <AppTable :columns="columns" :items="clientsStore.clients">
      <template #cell(name)="{ item }">
        {{ item.first_name }} {{ item.last_name }}
      </template>
      <template #cell(phone)="{ item }">
        {{ item.phone_number }}
      </template>
      <template #cell(address)="{ item }">
        <span v-if="item" class="text-xs">
          {{ item.city }}, {{ item.street }}
        </span>
      </template>
      <template #actions="{ item }">
        <div class="space-x-2">
          <AppButton variant="ghost" class="text-red-600 hover:text-red-900" @click="confirmDelete(item)">
            Delete
          </AppButton>
        </div>
      </template>
    </AppTable>

    <!-- Create Client Modal -->
    <AppModal v-model="isModalOpen" title="Create New Client">
      <div class="space-y-6">
        <div class="grid grid-cols-2 gap-4">
          <AppInput v-model="pdForm.first_name" label="First Name" required />
          <AppInput v-model="pdForm.last_name" label="Last Name" required />
          <AppInput v-model="pdForm.middle_name" label="Middle Name" />
          <AppInput v-model="pdForm.birth_date" label="Birth Date" type="date" required />
          <AppInput v-model="pdForm.phone_number" label="Phone Number" required />
        </div>
        
        <div class="border-t pt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-4">Address</h4>
          <div class="grid grid-cols-2 gap-4">
            <AppInput v-model="pdForm.region" label="Region" required />
            <AppInput v-model="pdForm.city" label="City" required />
            <AppInput v-model="pdForm.street" label="Street" required />
            <div class="grid grid-cols-2 gap-2">
              <AppInput v-model="pdForm.house" label="House" required />
              <AppInput v-model="pdForm.apartment" label="Apt" />
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <AppButton variant="ghost" @click="isModalOpen = false">Cancel</AppButton>
        <AppButton :loading="saving" @click="saveClient">
          Create Client
        </AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { useClientsStore } from '~/stores/clients';
import { usePersonalDataStore } from '~/stores/personalData';
import type { Client } from '~/types/api';

const clientsStore = useClientsStore();
const pdStore = usePersonalDataStore();

const columns = [
  { key: 'name', label: 'Full Name' },
  { key: 'phone', label: 'Phone' },
  { key: 'address', label: 'Address' },
];

const isModalOpen = ref(false);
const saving = ref(false);

const pdForm = reactive({
  first_name: '',
  last_name: '',
  middle_name: '',
  birth_date: '',
  phone_number: '',
  region: '',
  city: '',
  street: '',
  house: '',
  apartment: '',
});

function openCreateModal() {
  Object.keys(pdForm).forEach(key => (pdForm[key as keyof typeof pdForm] = ''));
  isModalOpen.value = true;
}

async function saveClient() {
  saving.value = true;
  try {
    const pd = await pdStore.createPersonalData({ ...pdForm });
    await clientsStore.createClient(pd.id);
    isModalOpen.value = false;
  } finally {
    saving.value = false;
  }
}

async function confirmDelete(client: Client) {
  if (confirm(`Are you sure you want to delete client "${client.first_name}"?`)) {
    await clientsStore.deleteClient(client.id);
  }
}

onMounted(() => {
  clientsStore.fetchClients();
});
</script>
