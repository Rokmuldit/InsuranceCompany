<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-medium text-gray-900">Agents</h3>
      <AppButton @click="openCreateModal">
        Register New Agent
      </AppButton>
    </div>

    <AppTable
      :columns="columns"
      :items="agentsStore.agents"
      :total="agentsStore.total"
      :page="agentsStore.page"
      :pages="agentsStore.pages"
      :size="agentsStore.size"
      @update:page="agentsStore.fetchAgents($event, agentsStore.size)"
      @update:size="agentsStore.fetchAgents(1, $event)"
    >
      <template #cell(name)="{ item }">
        {{ item.first_name }} {{ item.last_name }}
      </template>
      <template #cell(phone)="{ item }">
        {{ item.phone_number }}
      </template>
      <template #actions="{ item }">
        <AppButton variant="ghost" class="text-red-600 hover:text-red-900" @click="confirmDelete(item)">
          Delete
        </AppButton>
      </template>
    </AppTable>

    <!-- Register Agent Modal -->
    <AppModal v-model="isModalOpen" title="Register Agent">
      <div class="space-y-4">
        <p class="text-sm text-gray-500">
          Select an existing client to register as an agent.
        </p>
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">Client</label>
          <select
            v-model="selectedClientId"
            class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
          >
            <option disabled value="">Select a client</option>
            <option v-for="client in clientsStore.clients" :key="client.id" :value="client.id">
              {{ client.first_name }} {{ client.last_name }} ({{ client.phone_number }})
            </option>
          </select>
        </div>
      </div>
      <template #footer>
        <AppButton variant="ghost" @click="isModalOpen = false">Cancel</AppButton>
        <AppButton :loading="saving" :disabled="!selectedClientId" @click="saveAgent">
          Register Agent
        </AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { useAgentsStore } from '~/stores/agents';
import { useClientsStore } from '~/stores/clients';
import type { Agent } from '~/types/api';

const agentsStore = useAgentsStore();
const clientsStore = useClientsStore();

const columns = [
  { key: 'name', label: 'Full Name' },
  { key: 'phone', label: 'Phone' },
];

const isModalOpen = ref(false);
const saving = ref(false);
const selectedClientId = ref('');

function openCreateModal() {
  selectedClientId.value = '';
  isModalOpen.value = true;
  clientsStore.fetchClients();
}

async function saveAgent() {
  saving.value = true;
  try {
    await agentsStore.createAgent(selectedClientId.value);
    isModalOpen.value = false;
  } finally {
    saving.value = false;
  }
}

async function confirmDelete(agent: Agent) {
  if (confirm(`Are you sure you want to remove agent status for "${agent.first_name}"?`)) {
    await agentsStore.deleteAgent(agent.id);
  }
}

onMounted(() => {
  agentsStore.fetchAgents();
});
</script>
