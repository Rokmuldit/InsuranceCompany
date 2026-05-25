import { defineStore } from 'pinia';
import type { InsuranceContract, InsuranceContractCreate, Page } from '~/types/api';

export const useContractsStore = defineStore('contracts', () => {
  const { fetchApi } = useApi();
  const contracts = ref<InsuranceContract[]>([]);
  const loading = ref(false);

  const total = ref(0);
  const page = ref(1);
  const size = ref(10);
  const pages = ref(0);

  async function fetchContracts(p = 1, s = 10) {
    loading.value = true;
    try {
      const response = await fetchApi<Page<InsuranceContract>>('/insurance-contracts/', {
        query: { page: p, size: s }
      });
      contracts.value = response.items;
      total.value = response.total;
      page.value = response.page;
      size.value = response.size;
      pages.value = response.pages;
    } finally {
      loading.value = false;
    }
  }

  async function createContract(data: InsuranceContractCreate) {
    const newContract = await fetchApi<InsuranceContract>('/insurance-contracts/', {
      method: 'POST',
      body: data,
    });
    await fetchContracts(page.value, size.value);
    return newContract;
  }

  async function activateContract(id: string) {
    const updatedContract = await fetchApi<InsuranceContract>(`/insurance-contracts/${id}/activate`, {
      method: 'PATCH',
    });
    await fetchContracts(page.value, size.value);
    return updatedContract;
  }

  async function deleteContract(id: string) {
    await fetchApi(`/insurance-contracts/${id}`, { method: 'DELETE' });
    await fetchContracts(page.value, size.value);
  }

  async function fetchContractById(id: string) {
    loading.value = true;
    try {
      const contract = await fetchApi<InsuranceContract>(`/insurance-contracts/${id}`);
      return contract;
    } finally {
      loading.value = false;
    }
  }

  return {
    contracts,
    loading,
    total,
    page,
    size,
    pages,
    fetchContracts,
    fetchContractById,
    createContract,
    activateContract,
    deleteContract,
  };
});
