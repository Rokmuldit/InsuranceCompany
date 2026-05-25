import { defineStore } from 'pinia';
import type { PaidPlan, PaidPlanCreate, Page } from '~/types/api';

export const usePaidPlansStore = defineStore('paidPlans', () => {
  const { fetchApi } = useApi();
  const plans = ref<PaidPlan[]>([]);
  const loading = ref(false);

  const total = ref(0);
  const page = ref(1);
  const size = ref(10);
  const pages = ref(0);

  async function fetchPlans(p = 1, s = 10) {
    loading.value = true;
    try {
      const response = await fetchApi<Page<PaidPlan>>('/paid-plans/', {
        query: { page: p, size: s }
      });
      plans.value = response.items;
      total.value = response.total;
      page.value = response.page;
      size.value = response.size;
      pages.value = response.pages;
    } finally {
      loading.value = false;
    }
  }

  async function createPlan(data: PaidPlanCreate) {
    const newPlan = await fetchApi<PaidPlan>('/paid-plans/', {
      method: 'POST',
      body: data,
    });
    await fetchPlans(page.value, size.value);
    return newPlan;
  }

  async function updatePlan(id: string, data: PaidPlanCreate) {
    const updatedPlan = await fetchApi<PaidPlan>(`/paid-plans/${id}`, {
      method: 'PUT',
      body: data,
    });
    await fetchPlans(page.value, size.value);
    return updatedPlan;
  }

  async function deletePlan(id: string) {
    await fetchApi(`/paid-plans/${id}`, { method: 'DELETE' });
    await fetchPlans(page.value, size.value);
  }

  return {
    plans,
    loading,
    total,
    page,
    size,
    pages,
    fetchPlans,
    createPlan,
    updatePlan,
    deletePlan,
  };
});
