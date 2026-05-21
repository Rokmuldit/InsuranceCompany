import { defineStore } from 'pinia';
import type { Agent } from '~/types/api';

export const useAgentsStore = defineStore('agents', () => {
  const { fetchApi } = useApi();
  const agents = ref<Agent[]>([]);
  const loading = ref(false);

  async function fetchAgents() {
    loading.value = true;
    try {
      agents.value = await fetchApi<Agent[]>('/agents/');
    } finally {
      loading.value = false;
    }
  }

  async function createAgent(clientId: string) {
    const newAgent = await fetchApi<Agent>('/agents/', {
      method: 'POST',
      body: { client_id: clientId },
    });
    agents.value.push(newAgent);
    return newAgent;
  }

  async function deleteAgent(id: string) {
    await fetchApi(`/agents/${id}`, { method: 'DELETE' });
    agents.value = agents.value.filter(a => a.id !== id);
  }

  return {
    agents,
    loading,
    fetchAgents,
    createAgent,
    deleteAgent,
  };
});
