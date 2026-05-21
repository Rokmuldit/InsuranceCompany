<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-medium text-gray-900">Insurance Plans</h3>
      <AppButton @click="openCreateModal">
        Add New Plan
      </AppButton>
    </div>

    <AppTable :columns="columns" :items="plansStore.plans">
      <template #cell(payment_amount)="{ item }">
        ${{ item.payment_amount }}
      </template>
      <template #actions="{ item }">
        <div class="space-x-2">
          <AppButton variant="ghost" class="text-blue-600 hover:text-blue-900" @click="openEditModal(item)">
            Edit
          </AppButton>
          <AppButton variant="ghost" class="text-red-600 hover:text-red-900" @click="confirmDelete(item)">
            Delete
          </AppButton>
        </div>
      </template>
    </AppTable>

    <!-- Create/Edit Modal -->
    <AppModal v-model="isModalOpen" :title="isEditing ? 'Edit Plan' : 'Create New Plan'">
      <form @submit.prevent="savePlan" class="space-y-4">
        <AppInput v-model="form.name" label="Plan Name" required />
        <AppInput v-model="form.description" label="Description" />
        <AppInput v-model.number="form.payment_amount" label="Payment Amount" type="number" required />
        <AppInput v-model="form.payment_period" label="Payment Period" placeholder="e.g. Monthly, Yearly" required />
      </form>
      <template #footer>
        <AppButton variant="ghost" @click="isModalOpen = false">Cancel</AppButton>
        <AppButton :loading="saving" @click="savePlan">
          {{ isEditing ? 'Update Plan' : 'Create Plan' }}
        </AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { usePaidPlansStore } from '~/stores/plans';
import type { PaidPlan } from '~/types/api';

const plansStore = usePaidPlansStore();

const columns = [
  { key: 'name', label: 'Name' },
  { key: 'payment_amount', label: 'Amount' },
  { key: 'payment_period', label: 'Period' },
  { key: 'description', label: 'Description' },
];

const isModalOpen = ref(false);
const isEditing = ref(false);
const saving = ref(false);
const currentPlanId = ref<string | null>(null);

const form = reactive({
  name: '',
  description: '',
  payment_amount: 0,
  payment_period: '',
});

function openCreateModal() {
  isEditing.value = false;
  currentPlanId.value = null;
  form.name = '';
  form.description = '';
  form.payment_amount = 0;
  form.payment_period = '';
  isModalOpen.value = true;
}

function openEditModal(plan: PaidPlan) {
  isEditing.value = true;
  currentPlanId.value = plan.id;
  form.name = plan.name;
  form.description = plan.description || '';
  form.payment_amount = plan.payment_amount;
  form.payment_period = plan.payment_period;
  isModalOpen.value = true;
}

async function savePlan() {
  saving.value = true;
  try {
    if (isEditing.value && currentPlanId.value) {
      await plansStore.updatePlan(currentPlanId.value, { ...form });
    } else {
      await plansStore.createPlan({ ...form });
    }
    isModalOpen.value = false;
  } finally {
    saving.value = false;
  }
}

async function confirmDelete(plan: PaidPlan) {
  if (confirm(`Are you sure you want to delete plan "${plan.name}"?`)) {
    await plansStore.deletePlan(plan.id);
  }
}

onMounted(() => {
  plansStore.fetchPlans();
});
</script>
