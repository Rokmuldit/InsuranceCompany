<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-medium text-gray-900">Insurance Events</h3>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100 mb-6 space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Search Contract by Full ID</label>
        <div class="flex space-x-2">
          <input 
            v-model="searchId" 
            type="text" 
            placeholder="Paste full Contract ID (UUID)..." 
            class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm p-2 border"
          />
          <AppButton @click="searchByContractId" :loading="searching" variant="secondary">Search</AppButton>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Or select from list</label>
        <select v-model="selectedContractId" @change="loadEvents" class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
          <option value="">Select a contract</option>
          <option v-for="c in contractsStore.contracts" :key="c.contract_id" :value="c.contract_id">
            Contract #{{ c.contract_id.slice(0, 8) }}... - {{ c.client_last_name }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="selectedContractId" class="space-y-4">
      <div class="flex justify-between items-center">
        <h4 class="text-md font-medium text-gray-700">Events for selected contract</h4>
        <AppButton @click="isModalOpen = true">Report Event</AppButton>
      </div>

      <AppTable
        :columns="columns"
        :items="eventsStore.events"
        :total="eventsStore.total"
        :page="eventsStore.page"
        :pages="eventsStore.pages"
        :size="eventsStore.size"
        @update:page="eventsStore.fetchEventsByContract(selectedContractId, $event, eventsStore.size)"
        @update:size="eventsStore.fetchEventsByContract(selectedContractId, 1, $event)"
      >
        <template #cell(is_insurance_case)="{ item }">
          <span
            class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
            :class="item.is_insurance_case ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
          >
            {{ item.is_insurance_case ? 'Insurance Case' : 'Pending/Not Case' }}
          </span>
        </template>
        <template #actions="{ item }">
          <div class="space-x-2">
            <AppButton
              v-if="!item.is_insurance_case"
              variant="secondary"
              class="text-xs"
              @click="markAsInsuranceCase(item)"
            >
              Verify as Case
            </AppButton>
            <AppButton variant="ghost" class="text-red-600 hover:text-red-900" @click="deleteEvent(item)">
              Delete
            </AppButton>
          </div>
        </template>
      </AppTable>
    </div>

    <!-- Report Event Modal -->
    <AppModal v-model="isModalOpen" title="Report New Event">
      <form @submit.prevent="saveEvent" class="space-y-4">
        <AppInput v-model="form.event_date" label="Event Date" type="date" required />
        <AppInput v-model="form.description" label="Description" required />
      </form>
      <template #footer>
        <AppButton variant="ghost" @click="isModalOpen = false">Cancel</AppButton>
        <AppButton :loading="saving" @click="saveEvent">Report Event</AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { useEventsStore } from '~/stores/events';
import { useContractsStore } from '~/stores/contracts';
import type { InsuranceEvent } from '~/types/api';

const eventsStore = useEventsStore();
const contractsStore = useContractsStore();

const selectedContractId = ref('');
const searchId = ref('');
const searching = ref(false);

async function searchByContractId() {
  if (!searchId.value) return;
  searching.value = true;
  try {
    const contract = await contractsStore.fetchContractById(searchId.value);
    if (contract) {
      selectedContractId.value = contract.contract_id;
      await loadEvents();
    } else {
      alert('Contract not found');
    }
  } catch (e) {
    alert('Invalid ID or contract not found');
  } finally {
    searching.value = false;
  }
}

const isModalOpen = ref(false);
const saving = ref(false);

const columns = [
  { key: 'event_date', label: 'Date' },
  { key: 'description', label: 'Description' },
  { key: 'is_insurance_case', label: 'Status' },
];

const form = reactive({
  event_date: new Date().toISOString().split('T')[0],
  description: '',
});

async function loadEvents() {
  if (selectedContractId.value) {
    await eventsStore.fetchEventsByContract(selectedContractId.value);
  }
}

async function saveEvent() {
  saving.value = true;
  try {
    await eventsStore.createEvent(selectedContractId.value, { ...form });
    await loadEvents();
    isModalOpen.value = false;
  } finally {
    saving.value = false;
  }
}

async function markAsInsuranceCase(event: InsuranceEvent) {
  if (confirm('Verify this as a valid insurance case?')) {
    await eventsStore.updateEventStatus(event.id, true);
    await loadEvents();
  }
}

async function deleteEvent(event: InsuranceEvent) {
  if (confirm('Delete this event?')) {
    await eventsStore.deleteEvent(event.id);
    await loadEvents();
  }
}

onMounted(() => {
  contractsStore.fetchContracts();
});
</script>
