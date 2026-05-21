import { defineStore } from 'pinia';
import type { PaidPlan, PaidPlanCreate } from '~/types/api';

export const usePaidPlansStore = defineStore('paidPlans', () => {
  const { fetchApi } = useApi();
  const plans = ref<PaidPlan[]>([]);
  const loading = ref(false);

  async function fetchPlans() {
    loading.value = true;
    try {
      plans.value = await fetchApi<PaidPlan[]>('/paid-plans/');
    } finally {
      loading.value = false;
    }
  }

  async function createPlan(data: PaidPlanCreate) {
    const newPlan = await fetchApi<PaidPlan>('/paid-plans/', {
      method: 'POST',
      body: data,
    });
    plans.value.push(newPlan);
    return newPlan;
  }

  async function updatePlan(id: string, data: PaidPlanCreate) {
    const updatedPlan = await fetchApi<PaidPlan>(`/paid-plans/${id}`, {
      method: 'PUT',
      body: data,
    });
    const index = plans.value.findIndex(p => p.id === id);
    if (index !== -1) plans.value[index] = updatedPlan;
    return updatedPlan;
  }

  async function deletePlan(id: string) {
    await fetchApi(`/paid-plans/${id}`, { method: 'DELETE' });
    plans.value = plans.value.filter(p => p.id !== id);
  }

  return {
    plans,
    loading,
    fetchPlans,
    createPlan,
    updatePlan,
    deletePlan,
  };
});
