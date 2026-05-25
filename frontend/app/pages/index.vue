<template>
  <div class="space-y-6">
    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="stat in stats" :key="stat.name" class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <p class="text-sm font-medium text-gray-500 truncate">{{ stat.name }}</p>
        <div class="mt-2 text-3xl font-semibold text-gray-900">
          <!-- Показываем скелетон или текст загрузки, пока данные грузятся -->
          <span v-if="loadingStats" class="animate-pulse text-gray-300">...</span>
          <span v-else>{{ stat.value }}</span>
        </div>
      </div>
    </div>

    <!-- Health Check -->
    <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
      <h3 class="text-lg font-medium text-gray-900 mb-4">System Status</h3>
      <div v-if="health" class="flex items-center space-x-2">
        <span
          class="h-3 w-3 rounded-full"
          :class="health.status === 'ok' ? 'bg-green-500' : 'bg-red-500'"
        ></span>
        <span class="text-sm font-medium" :class="health.status === 'ok' ? 'text-green-700' : 'text-red-700'">
          API Status: {{ health.status.toUpperCase() }}
        </span>
        <span class="text-sm text-gray-500 ml-4">
          Database: {{ health.database }}
        </span>
      </div>
      <div v-else-if="loadingHealth" class="text-sm text-gray-500">
        Checking system health...
      </div>
      <div v-else class="text-sm text-red-500 font-medium">
        Could not connect to API. Please check if the backend is running.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const { fetchApi } = useApi();

const health = ref<{ status: string; database: string } | null>(null);
const loadingHealth = ref(true);
const loadingStats = ref(true);

// Делаем массив реактивным, чтобы интерфейс обновился после ответа API
const stats = ref([
  { name: 'Active Contracts', value: '0' },
  { name: 'Pending Payments', value: '$0' },
  { name: 'New Clients (MTD)', value: '0' },
  { name: 'Open Events', value: '0' },
]);

const loadStats = async () => {
  try {
    loadingStats.value = true;

    // Используем Promise.allSettled, чтобы если один запрос упадет (например, нет данных),
    // остальные все равно отобразились, а страница не сломалась.
    const [contractsRes, paymentsRes, clientsRes, eventsRes] = await Promise.allSettled([
      fetchApi('/insurance-contracts/quantity/active'),
      fetchApi('/insurance-payments/sum/all'),
      fetchApi('/clients/sum/all'),
      fetchApi('/insurance-events/sum/all_open_events')
    ]);

    // Обновляем значения в массиве, проверяя статус каждого промиса
    stats.value = [
      {
        name: 'Active Contracts',
        value: contractsRes.status === 'fulfilled' ? contractsRes.value.toString() : 'Error'
      },
      {
        name: 'Pending Payments',
        value: paymentsRes.status === 'fulfilled' ? `$${paymentsRes.value}` : 'Error'
      },
      {
        name: 'New Clients (MTD)',
        value: clientsRes.status === 'fulfilled' ? clientsRes.value.toString() : 'Error'
      },
      {
        name: 'Open Events',
        value: eventsRes.status === 'fulfilled' ? eventsRes.value.toString() : 'Error'
      },
    ];
  } catch (error) {
    console.error('Failed to load dashboard stats', error);
  } finally {
    loadingStats.value = false;
  }
};

onMounted(async () => {
  const healthPromise = fetchApi('/health')
    .then(res => { health.value = res; })
    .catch(e => console.error('Health check failed', e))
    .finally(() => { loadingHealth.value = false; });

  await Promise.all([healthPromise, loadStats()]);
});
</script>