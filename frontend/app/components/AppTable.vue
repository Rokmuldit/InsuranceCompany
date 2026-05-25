<template>
  <div class="flex flex-col">
    <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
        <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  v-for="column in columns"
                  :key="column.key"
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ column.label }}
                </th>
                <th v-if="$slots.actions" scope="col" class="relative px-6 py-3">
                  <span class="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in items" :key="index">
                <td
                  v-for="column in columns"
                  :key="column.key"
                  class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                >
                  <slot :name="`cell(${column.key})`" :item="item">
                    {{ item[column.key] }}
                  </slot>
                </td>
                <td v-if="$slots.actions" class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <slot name="actions" :item="item" />
                </td>
              </tr>
              <tr v-if="items.length === 0">
                <td :colspan="columns.length + ($slots.actions ? 1 : 0)" class="px-6 py-10 text-center text-sm text-gray-500">
                  No data available
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="total !== undefined && pages !== undefined" class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-4 rounded-lg shadow">
      <div class="flex-1 flex justify-between sm:hidden">
        <button
          @click="$emit('update:page', page - 1)"
          :disabled="page <= 1"
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          Previous
        </button>
        <button
          @click="$emit('update:page', page + 1)"
          :disabled="page >= pages"
          class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          Next
        </button>
      </div>
      <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700">
            Showing
            <span class="font-medium">{{ (page - 1) * size + 1 }}</span>
            to
            <span class="font-medium">{{ Math.min(page * size, total) }}</span>
            of
            <span class="font-medium">{{ total }}</span>
            results
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <select
            :value="size"
            @change="$emit('update:size', parseInt(($event.target as HTMLSelectElement).value))"
            class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            <option v-for="s in [5, 10, 20, 50]" :key="s" :value="s">{{ s }} per page</option>
          </select>
          <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
            <button
              @click="$emit('update:page', page - 1)"
              :disabled="page <= 1"
              class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
            >
              <span class="sr-only">Previous</span>
              &larr;
            </button>
            <button
              v-for="p in visiblePages"
              :key="p"
              @click="$emit('update:page', p)"
              :class="[
                p === page ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600' : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium'
              ]"
            >
              {{ p }}
            </button>
            <button
              @click="$emit('update:page', page + 1)"
              :disabled="page >= pages"
              class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
            >
              <span class="sr-only">Next</span>
              &rarr;
            </button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Column {
  key: string;
  label: string;
}

const props = defineProps({
  columns: {
    type: Array as () => Column[],
    required: true,
  },
  items: {
    type: Array as () => any[],
    required: true,
  },
  total: Number,
  page: {
    type: Number,
    default: 1
  },
  pages: {
    type: Number,
    default: 0
  },
  size: {
    type: Number,
    default: 10
  }
});

defineEmits(['update:page', 'update:size']);

const visiblePages = computed(() => {
  if (!props.pages) return [];
  const range = [];
  const maxVisible = 5;
  let start = Math.max(1, props.page - Math.floor(maxVisible / 2));
  let end = Math.min(props.pages, start + maxVisible - 1);

  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1);
  }

  for (let i = start; i <= end; i++) {
    range.push(i);
  }
  return range;
});
</script>
