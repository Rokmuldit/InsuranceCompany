import { defineStore } from 'pinia';
import type { InsurancePayment, InsurancePaymentCreate, Page } from '~/types/api';

export const usePaymentsStore = defineStore('payments', () => {
  const { fetchApi } = useApi();
  const payments = ref<InsurancePayment[]>([]);
  const loading = ref(false);

  const total = ref(0);
  const page = ref(1);
  const size = ref(10);
  const pages = ref(0);

  async function fetchPayments(p = 1, s = 10) {
    loading.value = true;
    try {
      const response = await fetchApi<Page<InsurancePayment>>('/insurance-payments/', {
        query: { page: p, size: s }
      });
      payments.value = response.items;
      total.value = response.total;
      page.value = response.page;
      size.value = response.size;
      pages.value = response.pages;
    } finally {
      loading.value = false;
    }
  }

  async function createPayment(data: InsurancePaymentCreate) {
    const newPayment = await fetchApi<InsurancePayment>('/insurance-payments/', {
      method: 'POST',
      body: data,
    });
    await fetchPayments(page.value, size.value);
    return newPayment;
  }

  async function deletePayment(id: string) {
    await fetchApi(`/insurance-payments/${id}`, { method: 'DELETE' });
    await fetchPayments(page.value, size.value);
  }

  return {
    payments,
    loading,
    total,
    page,
    size,
    pages,
    fetchPayments,
    createPayment,
    deletePayment,
  };
});
