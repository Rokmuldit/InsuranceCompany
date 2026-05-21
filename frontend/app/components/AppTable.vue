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
  </div>
</template>

<script setup lang="ts">
interface Column {
  key: string;
  label: string;
}

defineProps({
  columns: {
    type: Array as () => Column[],
    required: true,
  },
  items: {
    type: Array as () => any[],
    required: true,
  },
});
</script>
