<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-medium text-gray-900">Insurance Payments</h3>
      <AppButton @click="openCreateModal">
        Register Payment
      </AppButton>
    </div>

    <AppTable :columns="columns" :items="paymentsStore.payments">
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
          <select v-model="form.contract_id" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            <option disabled value="">Select Contract</option>
            <option v-for="c in contractsStore.contracts" :key="c.id" :value="c.id">
              #{{ c.id.slice(0, 8) }} - {{ c.client?.personal_data?.last_name }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Insurance Event (Optional)</label>
          <select v-model="form.event_id" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            <option value="">No specific event</option>
          </select>
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
import type { InsurancePayment } from '~/types/api';

const paymentsStore = usePaymentsStore();
const contractsStore = useContractsStore();

const columns = [
  { key: 'payment_date', label: 'Date' },
  { key: 'payment_amount', label: 'Amount' },
  { key: 'contract_id', label: 'Contract' },
];

const isModalOpen = ref(false);
const saving = ref(false);

const form = reactive({
  contract_id: '',
  event_id: '',
  payment_amount: 0,
  payment_date: new Date().toISOString().split('T')[0],
});

function openCreateModal() {
  form.contract_id = '';
  form.event_id = '';
  form.payment_amount = 0;
  isModalOpen.value = true;
  contractsStore.fetchContracts();
}

async function savePayment() {
  saving.value = true;
  try {
    await paymentsStore.createPayment({ ...form });
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
