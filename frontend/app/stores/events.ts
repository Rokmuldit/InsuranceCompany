import { defineStore } from 'pinia';
import type { InsuranceEvent, InsuranceEventCreate, Page } from '~/types/api';

export const useEventsStore = defineStore('events', () => {
  const { fetchApi } = useApi();
  const events = ref<InsuranceEvent[]>([]);
  const loading = ref(false);

  const total = ref(0);
  const page = ref(1);
  const size = ref(10);
  const pages = ref(0);

  async function fetchEventsByContract(contractId: string, p = 1, s = 10) {
    loading.value = true;
    try {
      const response = await fetchApi<Page<InsuranceEvent>>(`/insurance-events/contract/${contractId}`, {
        query: { page: p, size: s }
      });
      events.value = response.items;
      total.value = response.total;
      page.value = response.page;
      size.value = response.size;
      pages.value = response.pages;
      return response;
    } finally {
      loading.value = false;
    }
  }

  async function createEvent(contractId: string, data: InsuranceEventCreate) {
    const newEvent = await fetchApi<InsuranceEvent>(`/insurance-events/contract/${contractId}`, {
      method: 'POST',
      body: data,
    });
    await fetchEventsByContract(contractId, page.value, size.value);
    return newEvent;
  }

  async function updateEventStatus(eventId: string, isInsuranceCase: boolean) {
    const updatedEvent = await fetchApi<InsuranceEvent>(`/insurance-events/${eventId}/status`, {
      method: 'PATCH',
      body: { is_insurance_case: isInsuranceCase },
    });
    // We don't have contractId here easily, but usually updateEventStatus might be called from a view that knows it.
    // If we want to be safe and we have the event in our current list, we could update it locally or refetch if we knew contractId.
    // For now, let's just return it as before, or if it's in our list, update it.
    const index = events.value.findIndex(e => e.id === eventId);
    if (index !== -1) events.value[index] = updatedEvent;
    return updatedEvent;
  }

  async function deleteEvent(id: string, contractId?: string) {
    await fetchApi(`/insurance-events/${id}`, { method: 'DELETE' });
    if (contractId) {
      await fetchEventsByContract(contractId, page.value, size.value);
    } else {
      events.value = events.value.filter(e => e.id !== id);
    }
  }

  return {
    events,
    loading,
    total,
    page,
    size,
    pages,
    fetchEventsByContract,
    createEvent,
    updateEventStatus,
    deleteEvent,
  };
});
