<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-medium text-gray-900">Insurance Contracts</h3>
      <AppButton @click="openCreateModal">
        Create New Contract
      </AppButton>
    </div>

    <AppTable
      :columns="columns"
      :items="contractsStore.contracts"
      :total="contractsStore.total"
      :page="contractsStore.page"
      :pages="contractsStore.pages"
      :size="contractsStore.size"
      @update:page="contractsStore.fetchContracts($event, contractsStore.size)"
      @update:size="contractsStore.fetchContracts(1, $event)"
    >
      <!-- Клиент: ПИО + Телефон -->
      <template #cell(client)="{ item }">
        <div class="font-medium text-gray-900">
          {{ item.client_first_name }} {{ item.client_last_name }}
        </div>
        <div class="text-xs text-gray-500">{{ item.client_phone_number }}</div>
      </template>

      <!-- Агент: ПИО + Телефон -->
      <template #cell(agent)="{ item }">
        <div class="font-medium text-gray-900">
          {{ item.agent_first_name }} {{ item.agent_last_name }}
        </div>
        <div class="text-xs text-gray-500">{{ item.agent_phone_number }}</div>
      </template>

      <!-- Детали: Сумма + Даты -->
      <template #cell(detail)="{ item }">
        <div class="font-medium text-gray-900">${{ item.contract_amount }}</div>
        <div v-if="item.start_date" class="text-xs text-gray-500">
          {{ item.start_date }} &mdash; {{ item.end_date }}
        </div>
        <div v-else class="text-xs text-gray-400">Not activated</div>
      </template>

      <!-- Статус -->
      <template #cell(status)="{ item }">
        <span
          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
          :class="item.is_active ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-gray-800'"
        >
          {{ item.is_active ? 'Active' : 'Draft' }}
        </span>
      </template>

      <!-- Действия -->
      <template #actions="{ item }">
        <div class="flex items-center space-x-2">
          <AppButton
            variant="secondary"
            class="text-xs"
            @click="openDetailsModal(item)"
          >
            View
          </AppButton>
          <AppButton
            v-if="!item.is_active"
            variant="secondary"
            class="text-xs"
            @click="activateContract(item)"
          >
            Activate
          </AppButton>
          <AppButton variant="ghost" class="text-red-600 hover:text-red-900 p-1" @click="confirmDelete(item)">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </AppButton>
        </div>
      </template>
    </AppTable>

    <!-- Create Contract Modal -->
    <AppModal v-model="isModalOpen" title="Create Contract">
      <form @submit.prevent="saveContract" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Client</label>
          <div class="mt-1 space-y-2">
            <input
              v-model="clientSearchQuery"
              type="text"
              placeholder="Search client by last name..."
              class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm p-2 border"
            />
            <select v-model="form.client_id" class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
              <option disabled value="">Select Client</option>
              <option v-for="c in clientsStore.clients" :key="c.id" :value="c.id">
                {{ c.first_name }} {{ c.last_name }} ({{ c.phone_number }})
              </option>
            </select>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Agent</label>
          <div class="mt-1 space-y-2">
            <input
              v-model="agentSearchQuery"
              type="text"
              placeholder="Search agent by last name..."
              class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm p-2 border"
            />
            <select v-model="form.agent_id" class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
              <option disabled value="">Select Agent</option>
              <option v-for="a in agentsStore.agents" :key="a.id" :value="a.id">
                {{ a.first_name }} {{ a.last_name }} ({{ a.phone_number }})
              </option>
            </select>
          </div>
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

    <!-- View Contract Details Modal -->
    <AppModal v-model="isDetailsModalOpen" title="Contract Details">
      <div v-if="selectedContract" class="space-y-6 max-h-[70vh] overflow-y-auto pr-2">
        <!-- Contract Info -->
        <section>
          <h4 class="text-sm font-semibold text-blue-600 border-b border-blue-100 pb-1 mb-2 uppercase tracking-wider">General Information</h4>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div class="space-y-1">
              <span class="text-gray-500 block">Contract ID</span>
              <span class="font-mono text-xs bg-gray-50 p-1 rounded">{{ selectedContract.contract_id }}</span>
            </div>
            <div class="space-y-1">
              <span class="text-gray-500 block">Status</span>
              <span
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                :class="selectedContract.is_active ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-gray-800'"
              >
                {{ selectedContract.is_active ? 'Active' : 'Draft' }}
              </span>
            </div>
            <div class="space-y-1">
              <span class="text-gray-500 block">Contract Amount</span>
              <span class="text-lg font-bold text-gray-900">${{ selectedContract.contract_amount }}</span>
            </div>
            <div class="space-y-1">
              <span class="text-gray-500 block">Insurance Period</span>
              <span v-if="selectedContract.start_date" class="font-medium">{{ selectedContract.start_date }} &mdash; {{ selectedContract.end_date }}</span>
              <span v-else class="text-gray-400 italic">Not activated yet</span>
            </div>
          </div>
        </section>

        <!-- Client Info -->
        <section>
          <h4 class="text-sm font-semibold text-blue-600 border-b border-blue-100 pb-1 mb-2 uppercase tracking-wider">Client Details</h4>
          <div class="grid grid-cols-2 gap-x-4 gap-y-3 text-sm">
            <div class="col-span-2">
              <span class="text-gray-500 block">Full Name</span>
              <span class="font-medium text-gray-900">{{ selectedContract.client_first_name }} {{ selectedContract.client_last_name }} {{ selectedContract.client_middle_name || '' }}</span>
            </div>
            <div>
              <span class="text-gray-500 block">Phone Number</span>
              <span class="font-medium text-gray-900">{{ selectedContract.client_phone_number }}</span>
            </div>
            <div>
              <span class="text-gray-500 block">Birth Date</span>
              <span class="font-medium text-gray-900">{{ selectedContract.client_birth_date }}</span>
            </div>
            <div class="col-span-2">
              <span class="text-gray-500 block">Address</span>
              <span class="font-medium text-gray-900">
                {{ selectedContract.client_region }}, {{ selectedContract.client_city }}, 
                {{ selectedContract.client_street }}, {{ selectedContract.client_house }}
                <span v-if="selectedContract.client_apartment">, apt. {{ selectedContract.client_apartment }}</span>
              </span>
            </div>
          </div>
        </section>

        <!-- Agent Info -->
        <section>
          <h4 class="text-sm font-semibold text-blue-600 border-b border-blue-100 pb-1 mb-2 uppercase tracking-wider">Agent Details</h4>
          <div class="grid grid-cols-2 gap-x-4 gap-y-3 text-sm">
            <div class="col-span-2">
              <span class="text-gray-500 block">Full Name</span>
              <span class="font-medium text-gray-900">{{ selectedContract.agent_first_name }} {{ selectedContract.agent_last_name }} {{ selectedContract.agent_middle_name || '' }}</span>
            </div>
            <div>
              <span class="text-gray-500 block">Phone Number</span>
              <span class="font-medium text-gray-900">{{ selectedContract.agent_phone_number }}</span>
            </div>
            <div>
              <span class="text-gray-500 block">Birth Date</span>
              <span class="font-medium text-gray-900">{{ selectedContract.agent_birth_date }}</span>
            </div>
            <div class="col-span-2">
              <span class="text-gray-500 block">Address</span>
              <span class="font-medium text-gray-900">
                {{ selectedContract.agent_region }}, {{ selectedContract.agent_city }}, 
                {{ selectedContract.agent_street }}, {{ selectedContract.agent_house }}
                <span v-if="selectedContract.agent_apartment">, apt. {{ selectedContract.agent_apartment }}</span>
              </span>
            </div>
          </div>
        </section>
      </div>
      <template #footer>
        <AppButton variant="secondary" @click="isDetailsModalOpen = false">Close</AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { useContractsStore } from '~/stores/contracts';
import { useClientsStore } from '~/stores/clients';
import { useAgentsStore } from '~/stores/agents';
import { usePaidPlansStore } from '~/stores/plans';
import AppTable from "~/components/AppTable.vue";
import AppModal from "~/components/AppModal.vue";
import type { InsuranceContract } from '~/types/api';

const contractsStore = useContractsStore();
const clientsStore = useClientsStore();
const agentsStore = useAgentsStore();
const plansStore = usePaidPlansStore();

const columns = [
  { key: 'client', label: 'Client' },
  { key: 'agent', label: 'Agent' },
  { key: 'detail', label: 'Amount / Dates' },
  { key: 'status', label: 'Status' },
];

const isModalOpen = ref(false);
const isDetailsModalOpen = ref(false);
const saving = ref(false);
const selectedContract = ref<InsuranceContract | null>(null);

const clientSearchQuery = ref('');
const agentSearchQuery = ref('');

let clientSearchTimeout: any = null;
watch(clientSearchQuery, (newQuery) => {
  clearTimeout(clientSearchTimeout);
  clientSearchTimeout = setTimeout(() => {
    clientsStore.searchClients(newQuery);
  }, 300);
});

let agentSearchTimeout: any = null;
watch(agentSearchQuery, (newQuery) => {
  clearTimeout(agentSearchTimeout);
  agentSearchTimeout = setTimeout(() => {
    agentsStore.searchAgents(newQuery);
  }, 300);
});

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
  clientSearchQuery.value = '';
  agentSearchQuery.value = '';
  isModalOpen.value = true;
  clientsStore.fetchClients();
  agentsStore.fetchAgents();
  plansStore.fetchPlans();
}

function openDetailsModal(contract: InsuranceContract) {
  selectedContract.value = contract;
  isDetailsModalOpen.value = true;
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
    await contractsStore.activateContract(contract.contract_id);
  }
}

async function confirmDelete(contract: InsuranceContract) {
  if (confirm('Delete this contract?')) {
    await contractsStore.deleteContract(contract.contract_id);
  }
}

onMounted(() => {
  contractsStore.fetchContracts();
});
</script>
