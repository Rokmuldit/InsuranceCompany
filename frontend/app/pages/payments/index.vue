<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-medium text-gray-900">Insurance Payments</h3>
      <AppButton @click="openCreateModal">
        Register Payment
      </AppButton>
    </div>

    <AppTable
      :columns="columns"
      :items="paymentsStore.payments"
      :total="paymentsStore.total"
      :page="paymentsStore.page"
      :pages="paymentsStore.pages"
      :size="paymentsStore.size"
      @update:page="paymentsStore.fetchPayments($event, paymentsStore.size)"
      @update:size="paymentsStore.fetchPayments(1, $event)"
    >
      <template #cell(contract_id)="{ item }">
        #{{ item.contract_id.slice(0, 8) }}
      </template>
      <template #cell(payment_amount)="{ item }">
        ${{ item.payment_amount }}
      </template>
      <template #actions="{ item }">
        <AppButton variant="ghost" class="text-red-600 hover:text-red-900" @click="confirmDelete(item)">
          Delete
        </AppButton>
      </template>
    </AppTable>

    <!-- Register Payment Modal -->
    <AppModal v-model="isModalOpen" title="Register Payment">
      <form @submit.prevent="savePayment" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Contract</label>
          <div class="mt-1 space-y-2">
            <div class="flex space-x-2">
              <input 
                v-model="searchId" 
                type="text" 
                placeholder="Search by full Contract ID..." 
                class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm p-2 border"
              />
              <AppButton @click.prevent="searchByContractId" :loading="searchingContract" variant="secondary" class="text-xs">Find</AppButton>
            </div>
            <select v-model="form.contract_id" class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
              <option disabled value="">Select from list</option>
              <option v-for="c in contractsStore.contracts" :key="c.contract_id" :value="c.contract_id">
                #{{ c.contract_id.slice(0, 8) }}... - {{ c.client_last_name }}
              </option>
            </select>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Insurance Event (Optional)</label>
          <select 
            v-model="form.event_id" 
            :disabled="!form.contract_id || loadingEvents"
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm disabled:bg-gray-50"
          >
            <option value="">No specific event</option>
            <option v-for="e in availableEvents" :key="e.id" :value="e.id">
              {{ e.event_date }} - {{ e.description?.slice(0, 30) }}...
            </option>
          </select>
          <p v-if="loadingEvents" class="text-xs text-gray-500 mt-1 italic">Loading events...</p>
        </div>
        <AppInput v-model.number="form.payment_amount" label="Amount" type="number" required />
        <AppInput v-model="form.payment_date" label="Payment Date" type="date" required />
      </form>
      <template #footer>
        <AppButton variant="ghost" @click="isModalOpen = false">Cancel</AppButton>
        <AppButton :loading="saving" @click="savePayment">Register Payment</AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { usePaymentsStore } from '~/stores/payments';
import { useContractsStore } from '~/stores/contracts';
import { useEventsStore } from '~/stores/events';
import type { InsurancePayment, InsuranceEvent } from '~/types/api';

const paymentsStore = usePaymentsStore();
const contractsStore = useContractsStore();
const eventsStore = useEventsStore();

const columns = [
  { key: 'payment_date', label: 'Date' },
  { key: 'payment_amount', label: 'Amount' },
  { key: 'contract_id', label: 'Contract' },
];

const isModalOpen = ref(false);
const saving = ref(false);
const loadingEvents = ref(false);
const searchingContract = ref(false);
const searchId = ref('');
const availableEvents = ref<InsuranceEvent[]>([]);

const form = reactive({
  contract_id: '',
  event_id: '',
  payment_amount: 0,
  payment_date: new Date().toISOString().split('T')[0],
});

// Watch for contract changes to load corresponding events
watch(() => form.contract_id, async (newContractId) => {
  form.event_id = ''; // Reset event selection
  if (newContractId) {
    loadingEvents.value = true;
    try {
      const response = await eventsStore.fetchEventsByContract(newContractId);
      availableEvents.value = response.items;
    } catch (e) {
      console.error('Failed to load events for contract', e);
      availableEvents.value = [];
    } finally {
      loadingEvents.value = false;
    }
  } else {
    availableEvents.value = [];
  }
});

async function searchByContractId() {
  if (!searchId.value) return;
  searchingContract.value = true;
  try {
    const contract = await contractsStore.fetchContractById(searchId.value);
    if (contract) {
      form.contract_id = contract.contract_id;
    } else {
      alert('Contract not found');
    }
  } catch (e) {
    alert('Invalid ID or contract not found');
  } finally {
    searchingContract.value = false;
  }
}

function openCreateModal() {
  form.contract_id = '';
  form.event_id = '';
  form.payment_amount = 0;
  searchId.value = '';
  isModalOpen.value = true;
  contractsStore.fetchContracts();
}

async function savePayment() {
  saving.value = true;
  try {
    // If event_id is empty string, make it null or handle as needed by backend
    const payload = { ...form };
    if (!payload.event_id) delete (payload as any).event_id;
    
    await paymentsStore.createPayment(payload as any);
    isModalOpen.value = false;
  } finally {
    saving.value = false;
  }
}

async function confirmDelete(payment: InsurancePayment) {
  if (confirm('Delete this payment record?')) {
    await paymentsStore.deletePayment(payment.id);
  }
}

onMounted(() => {
  paymentsStore.fetchPayments();
});
</script>
