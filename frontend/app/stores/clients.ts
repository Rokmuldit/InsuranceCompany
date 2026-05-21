import { defineStore } from 'pinia';
import type { Client } from '~/types/api';

export const useClientsStore = defineStore('clients', () => {
  const { fetchApi } = useApi();
  const clients = ref<Client[]>([]);
  const loading = ref(false);

  async function fetchClients() {
    loading.value = true;
    try {
      clients.value = await fetchApi<Client[]>('/clients/');
    } finally {
      loading.value = false;
    }
  }

  async function createClient(personalDataId: string) {
    const newClient = await fetchApi<Client>('/clients/', {
      method: 'POST',
      body: { personal_data_id: personalDataId },
    });
    clients.value.push(newClient);
    return newClient;
  }

  async function deleteClient(id: string) {
    await fetchApi(`/clients/${id}`, { method: 'DELETE' });
    clients.value = clients.value.filter(c => c.id !== id);
  }

  return {
    clients,
    loading,
    fetchClients,
    createClient,
    deleteClient,
  };
});
