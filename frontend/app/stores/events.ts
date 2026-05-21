import { defineStore } from 'pinia';
import type { InsuranceEvent, InsuranceEventCreate } from '~/types/api';

export const useEventsStore = defineStore('events', () => {
  const { fetchApi } = useApi();
  const loading = ref(false);

  async function fetchEventsByContract(contractId: string) {
    loading.value = true;
    try {
      return await fetchApi<InsuranceEvent[]>(`/insurance-events/contract/${contractId}`);
    } finally {
      loading.value = false;
    }
  }

  async function createEvent(contractId: string, data: InsuranceEventCreate) {
    return await fetchApi<InsuranceEvent>(`/insurance-events/contract/${contractId}`, {
      method: 'POST',
      body: data,
    });
  }

  async function updateEventStatus(eventId: string, isInsuranceCase: boolean) {
    return await fetchApi<InsuranceEvent>(`/insurance-events/${eventId}/status`, {
      method: 'PATCH',
      body: { is_insurance_case: isInsuranceCase },
    });
  }

  async function deleteEvent(id: string) {
    await fetchApi(`/insurance-events/${id}`, { method: 'DELETE' });
  }

  return {
    loading,
    fetchEventsByContract,
    createEvent,
    updateEventStatus,
    deleteEvent,
  };
});
