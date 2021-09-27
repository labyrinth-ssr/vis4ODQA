<template>
<div id='threshold-button-container'>
  <div id="title" class="chart-title">
      <a-button id="resetButton" type="primary" size="small" v-on:click="reset_tokens">Clear tokens></a-button>
    </div>
  <div id="threshold-selected">
    <a-slider :marks='marks' :max=0.5 :min=0.1 :step=0.1 :default-value="0.4" 
      @afterChange="onAfterChange" 
              />
  </div>
</div>
</template>

<script>
import bus from './bus'

export default {
  name: 'ThresholdSelected',
  methods: {
     onAfterChange(value) {
       console.log('after change')
      this.threshold = value;
      bus.$emit("dispatchthreshold",this.threshold);
    },
    
  },
  data(){
    return {
      marks: {
        0.1: '0.1',
        0.2: '0.2',
        0.3: '0.3',
        0.4: '0.4',
        0.5: '0.5',
        },
      threshold:0.4
    }
  }
}
</script>

<style>
#threshold-button-container{
  display: flex;
  width: 100;
  height: 8%;
  overflow: hidden;
}
#threshold-selected{
  position: relative;
  left: 10%;
  width:50%;
  height: 100%;
}
#title{
  margin: 0px 40px;

}
</style>