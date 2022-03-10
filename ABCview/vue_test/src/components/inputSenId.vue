<template>
  <a-input v-model: modelValue="value" placeholder="Basic usage" />
</template>
<script>
import { defineComponent, ref } from 'vue';
export default defineComponent({
  setup() {
    const value = ref('');
    return {
      value,
    };
  },
});
</script>