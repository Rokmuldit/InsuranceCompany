import { defineStore } from 'pinia';
import type { InsuranceContract, InsuranceContractCreate } from '~/types/api';

export const useContractsStore = defineStore('contracts', () => {
  const { fetchApi } = useApi();
  const contracts = ref<InsuranceContract[]>([]);
  const loading = ref(false);

  async function fetchContracts() {
    loading.value = true;
    try {
      contracts.value = await fetchApi<InsuranceContract[]>('/insurance-contracts/');
    } finally {
      loading.value = false;
    }
  }

  async function createContract(data: InsuranceContractCreate) {
    const newContract = await fetchApi<InsuranceContract>('/insurance-contracts/', {
      method: 'POST',
      body: data,
    });
    contracts.value.push(newContract);
    return newContract;
  }

  async function activateContract(id: string) {
    const updatedContract = await fetchApi<InsuranceContract>(`/insurance-contracts/${id}/activate`, {
      method: 'PATCH',
    });
    const index = contracts.value.findIndex(c => c.id === id);
    if (index !== -1) contracts.value[index] = updatedContract;
    return updatedContract;
  }

  async function deleteContract(id: string) {
    await fetchApi(`/insurance-contracts/${id}`, { method: 'DELETE' });
    contracts.value = contracts.value.filter(c => c.id !== id);
  }

  return {
    contracts,
    loading,
    fetchContracts,
    createContract,
    activateContract,
    deleteContract,
  };
});
