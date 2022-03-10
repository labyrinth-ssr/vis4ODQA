<template>
    <div id="input-container">
      <div id="input-box">
        <a-input v-model="input_value" @pressEnter="input_sentenceId" />
      </div>
    </div>
      
</template>

<script>
import bus from "./bus";

export default {
  name: "queThreBox",
  methods: {
    input_sentenceId(){
      console.log("input"+this.input_value)
      bus.$emit('dispatchQueThre',this.input_value)
    }
  },
  data() {
    return {
      input_value:50
    };
  },
};
</script>

<style>


</style>