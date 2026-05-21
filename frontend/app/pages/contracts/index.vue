<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-medium text-gray-900">Insurance Contracts</h3>
      <AppButton @click="openCreateModal">
        Create New Contract
      </AppButton>
    </div>

    <AppTable :columns="columns" :items="contractsStore.contracts">
      <template #cell(client)="{ item }">
        {{ item.client_first_name }} {{ item.client_last_name }}
      </template>
      <template #cell(agent)="{ item }">
        {{ item.agent_first_name }} {{ item.agent_last_name }}
      </template>
      <template #cell(contract_amount)="{ item }">
        {{ item.contract_amount }}
      </template>
      <template #cell(status)="{ item }">
        <span
          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
          :class="item.is_active ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
        >
          {{ item.is_active ? 'Active' : 'Draft' }}
        </span>
      </template>
      <template #actions="{ item }">
        <div class="space-x-2">
          <AppButton
            v-if="!item.is_active"
            variant="secondary"
            class="text-xs"
            @click="activateContract(item)"
          >
            Activate
          </AppButton>
          <AppButton variant="ghost" class="text-red-600 hover:text-red-900" @click="confirmDelete(item)">
            Delete
          </AppButton>
        </div>
      </template>
    </AppTable>

    <!-- Create Contract Modal -->
    <AppModal v-model="isModalOpen" title="Create Contract">
      <form @submit.prevent="saveContract" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Client</label>
          <select v-model="form.client_id" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            <option disabled value="">Select Client</option>
            <option v-for="c in clientsStore.clients" :key="c.id" :value="c.id">
              {{ c.first_name }} {{ c.last_name }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Agent</label>
          <select v-model="form.agent_id" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            <option disabled value="">Select Agent</option>
            <option v-for="a in agentsStore.agents" :key="a.id" :value="a.id">
              {{ a.first_name }} {{ a.last_name }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Plan</label>
          <select v-model="form.plan_id" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            <option disabled value="">Select Plan</option>
            <option v-for="p in plansStore.plans" :key="p.id" :value="p.id">
              {{ p.name }} (${{ p.payment_amount }} / {{ p.payment_period }})
            </option>
          </select>
        </div>
      </form>
      <template #footer>
        <AppButton variant="ghost" @click="isModalOpen = false">Cancel</AppButton>
        <AppButton :loading="saving" :disabled="!isFormValid" @click="saveContract">
          Create Contract
        </AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { useContractsStore } from '~/stores/contracts';
import { useClientsStore } from '~/stores/clients';
import { useAgentsStore } from '~/stores/agents';
import { usePaidPlansStore } from '~/stores/plans';
import type { InsuranceContract } from '~/types/api';

const contractsStore = useContractsStore();
const clientsStore = useClientsStore();
const agentsStore = useAgentsStore();
const plansStore = usePaidPlansStore();

const columns = [
  { key: 'client', label: 'Client' },
  { key: 'agent', label: 'Agent' },
  { key: 'plan', label: 'Plan' },
  { key: 'status', label: 'Status' },
];

const isModalOpen = ref(false);
const saving = ref(false);

const form = reactive({
  client_id: '',
  agent_id: '',
  plan_id: '',
});

const isFormValid = computed(() => form.client_id && form.agent_id && form.plan_id);

function openCreateModal() {
  form.client_id = '';
  form.agent_id = '';
  form.plan_id = '';
  isModalOpen.value = true;
  clientsStore.fetchClients();
  agentsStore.fetchAgents();
  plansStore.fetchPlans();
}

async function saveContract() {
  saving.value = true;
  try {
    await contractsStore.createContract({ ...form });
    isModalOpen.value = false;
  } finally {
    saving.value = false;
  }
}

async function activateContract(contract: InsuranceContract) {
  if (confirm('Activate this contract?')) {
    await contractsStore.activateContract(contract.id);
  }
}

async function confirmDelete(contract: InsuranceContract) {
  if (confirm('Delete this contract?')) {
    await contractsStore.deleteContract(contract.id);
  }
}

onMounted(() => {
  contractsStore.fetchContracts();
});
</script>
