import { defineStore } from 'pinia';
import type { Client, Page } from '~/types/api';

export const useClientsStore = defineStore('clients', () => {
  const { fetchApi } = useApi();
  const clients = ref<Client[]>([]);
  const loading = ref(false);
  
  const total = ref(0);
  const page = ref(1);
  const size = ref(10);
  const pages = ref(0);

  async function fetchClients(p = 1, s = 10) {
    loading.value = true;
    try {
      const response = await fetchApi<Page<Client>>('/clients/', {
        query: { page: p, size: s }
      });
      clients.value = response.items;
      total.value = response.total;
      page.value = response.page;
      size.value = response.size;
      pages.value = response.pages;
    } finally {
      loading.value = false;
    }
  }

  async function createClient(personalDataId: string) {
    const newClient = await fetchApi<Client>('/clients/', {
      method: 'POST',
      body: { personal_data_id: personalDataId },
    });
    await fetchClients(page.value, size.value);
    return newClient;
  }

  async function deleteClient(id: string) {
    await fetchApi(`/clients/${id}`, { method: 'DELETE' });
    await fetchClients(page.value, size.value);
  }

  async function searchClients(query: string) {
    if (!query) return fetchClients(1, size.value);
    loading.value = true;
    try {
      const results = await fetchApi<Client[]>('/clients/search', {
        method: 'POST',
        body: {
          last_name: query,
          phone_number: query
        }
      });
      clients.value = results;
      total.value = results.length;
      page.value = 1;
      pages.value = 1;
    } finally {
      loading.value = false;
    }
  }

  return {
    clients,
    loading,
    total,
    page,
    size,
    pages,
    fetchClients,
    searchClients,
    createClient,
    deleteClient,
  };
});
