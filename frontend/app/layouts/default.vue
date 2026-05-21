<template>
  <div class="min-h-screen bg-gray-100 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800 text-white flex-shrink-0">
      <div class="p-6">
        <h1 class="text-xl font-bold">Insurance Admin</h1>
      </div>
      <nav class="mt-6">
        <NuxtLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center px-6 py-3 text-gray-300 hover:bg-slate-700 hover:text-white transition-colors"
          active-class="bg-slate-900 text-white"
        >
          <span class="mr-3">{{ item.icon }}</span>
          {{ item.name }}
        </NuxtLink>
      </nav>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <header class="bg-white shadow-sm h-16 flex items-center justify-between px-8">
        <h2 class="text-lg font-medium text-gray-700">{{ currentPageTitle }}</h2>
        <div class="flex items-center space-x-4">
          <span class="text-sm text-gray-500">Admin User</span>
          <div class="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
            A
          </div>
        </div>
      </header>

      <main class="p-8 overflow-y-auto">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute();

const navItems = [
  { name: 'Dashboard', path: '/', icon: '📊' },
  { name: 'Plans', path: '/plans', icon: '📋' },
  { name: 'Clients', path: '/clients', icon: '👥' },
  { name: 'Agents', path: '/agents', icon: '🕵️' },
  { name: 'Contracts', path: '/contracts', icon: '📄' },
  { name: 'Events', path: '/events', icon: '⚠️' },
  { name: 'Payments', path: '/payments', icon: '💰' },
];

const currentPageTitle = computed(() => {
  const current = navItems.find(item => item.path === route.path);
  return current ? current.name : 'Admin Panel';
});
</script>
