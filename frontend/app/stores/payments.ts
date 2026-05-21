import { defineStore } from 'pinia';
import type { InsurancePayment, InsurancePaymentCreate } from '~/types/api';

export const usePaymentsStore = defineStore('payments', () => {
  const { fetchApi } = useApi();
  const payments = ref<InsurancePayment[]>([]);
  const loading = ref(false);

  async function fetchPayments() {
    loading.value = true;
    try {
      payments.value = await fetchApi<InsurancePayment[]>('/insurance-payments/');
    } finally {
      loading.value = false;
    }
  }

  async function createPayment(data: InsurancePaymentCreate) {
    const newPayment = await fetchApi<InsurancePayment>('/insurance-payments/', {
      method: 'POST',
      body: data,
    });
    payments.value.push(newPayment);
    return newPayment;
  }

  async function deletePayment(id: string) {
    await fetchApi(`/insurance-payments/${id}`, { method: 'DELETE' });
    payments.value = payments.value.filter(p => p.id !== id);
  }

  return {
    payments,
    loading,
    fetchPayments,
    createPayment,
    deletePayment,
  };
});
