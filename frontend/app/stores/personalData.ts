import { defineStore } from 'pinia';
import type { PersonalData, PersonalDataCreate } from '~/types/api';

export const usePersonalDataStore = defineStore('personalData', () => {
  const { fetchApi } = useApi();
  const personalDataList = ref<PersonalData[]>([]);
  const loading = ref(false);

  async function fetchAllPersonalData() {
    loading.value = true;
    try {
      personalDataList.value = await fetchApi<PersonalData[]>('/personal-data/');
    } finally {
      loading.value = false;
    }
  }

  async function createPersonalData(data: PersonalDataCreate) {
    const newData = await fetchApi<PersonalData>('/personal-data/', {
      method: 'POST',
      body: data,
    });
    personalDataList.value.push(newData);
    return newData;
  }

  async function updatePersonalData(id: string, data: Partial<PersonalDataCreate>) {
    const updatedData = await fetchApi<PersonalData>(`/personal-data/${id}`, {
      method: 'PATCH',
      body: data,
    });
    const index = personalDataList.value.findIndex(p => p.id === id);
    if (index !== -1) personalDataList.value[index] = updatedData;
    return updatedData;
  }

  async function deletePersonalData(id: string) {
    await fetchApi(`/personal-data/${id}`, { method: 'DELETE' });
    personalDataList.value = personalDataList.value.filter(p => p.id !== id);
  }

  return {
    personalDataList,
    loading,
    fetchAllPersonalData,
    createPersonalData,
    updatePersonalData,
    deletePersonalData,
  };
});
