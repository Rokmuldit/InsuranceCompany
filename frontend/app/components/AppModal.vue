<template>
  <div
    v-if="modelValue"
    class="fixed z-10 inset-0 overflow-y-auto"
    aria-labelledby="modal-title"
    role="dialog"
    aria-modal="true"
  >
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        aria-hidden="true"
        @click="$emit('update:modelValue', false)"
      ></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <div>
          <h3 v-if="title" class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
            {{ title }}
          </h3>
          <div class="mt-4">
            <slot />
          </div>
        </div>
        <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
          <slot name="footer">
            <AppButton variant="ghost" class="sm:col-start-1" @click="$emit('update:modelValue', false)">
              Cancel
            </AppButton>
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  modelValue: Boolean,
  title: String,
});

defineEmits(['update:modelValue']);
</script>
