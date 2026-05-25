import { defineStore } from 'pinia';
import type { PersonalData, PersonalDataCreate, Page } from '~/types/api';

export const usePersonalDataStore = defineStore('personalData', () => {
  const { fetchApi } = useApi();
  const personalDataList = ref<PersonalData[]>([]);
  const loading = ref(false);

  const total = ref(0);
  const page = ref(1);
  const size = ref(10);
  const pages = ref(0);

  async function fetchAllPersonalData(p = 1, s = 10) {
    loading.value = true;
    try {
      const response = await fetchApi<Page<PersonalData>>('/personal-data/', {
        query: { page: p, size: s }
      });
      personalDataList.value = response.items;
      total.value = response.total;
      page.value = response.page;
      size.value = response.size;
      pages.value = response.pages;
    } finally {
      loading.value = false;
    }
  }

  async function createPersonalData(data: PersonalDataCreate) {
    const newData = await fetchApi<PersonalData>('/personal-data/', {
      method: 'POST',
      body: data,
    });
    await fetchAllPersonalData(page.value, size.value);
    return newData;
  }

  async function updatePersonalData(id: string, data: Partial<PersonalDataCreate>) {
    const updatedData = await fetchApi<PersonalData>(`/personal-data/${id}`, {
      method: 'PATCH',
      body: data,
    });
    await fetchAllPersonalData(page.value, size.value);
    return updatedData;
  }

  async function deletePersonalData(id: string) {
    await fetchApi(`/personal-data/${id}`, { method: 'DELETE' });
    await fetchAllPersonalData(page.value, size.value);
  }

  return {
    personalDataList,
    loading,
    total,
    page,
    size,
    pages,
    fetchAllPersonalData,
    createPersonalData,
    updatePersonalData,
    deletePersonalData,
  };
});
