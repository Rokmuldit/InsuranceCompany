import { defineStore } from 'pinia';
import type { Agent, Page } from '~/types/api';

export const useAgentsStore = defineStore('agents', () => {
  const { fetchApi } = useApi();
  const agents = ref<Agent[]>([]);
  const loading = ref(false);

  const total = ref(0);
  const page = ref(1);
  const size = ref(10);
  const pages = ref(0);

  async function fetchAgents(p = 1, s = 10) {
    loading.value = true;
    try {
      const response = await fetchApi<Page<Agent>>('/agents/', {
        query: { page: p, size: s }
      });
      agents.value = response.items;
      total.value = response.total;
      page.value = response.page;
      size.value = response.size;
      pages.value = response.pages;
    } finally {
      loading.value = false;
    }
  }

  async function createAgent(clientId: string) {
    const newAgent = await fetchApi<Agent>('/agents/', {
      method: 'POST',
      body: { client_id: clientId },
    });
    await fetchAgents(page.value, size.value);
    return newAgent;
  }

  async function deleteAgent(id: string) {
    await fetchApi(`/agents/${id}`, { method: 'DELETE' });
    await fetchAgents(page.value, size.value);
  }

  async function searchAgents(query: string) {
    if (!query) return fetchAgents(1, size.value);
    loading.value = true;
    try {
      const results = await fetchApi<Agent[]>('/agents/search', {
        method: 'POST',
        body: {
          last_name: query,
          phone_number: query
        }
      });
      agents.value = results;
      total.value = results.length;
      page.value = 1;
      pages.value = 1;
    } finally {
      loading.value = false;
    }
  }

  return {
    agents,
    loading,
    total,
    page,
    size,
    pages,
    fetchAgents,
    searchAgents,
    createAgent,
    deleteAgent,
  };
});
