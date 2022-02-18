<template>
  <div id="layer-selected">
    <a-slider range :marks="marks" :max=12 :min=1 :step=1 :default-value="[1, 12]" 
              @afterChange = "afterChange"
              />
  </div>
</template>

<script>
import bus from './bus'

export default {
  name: 'LayerSelected',
  methods: {
     afterChange(value) {
      this.layerspan = value;
      bus.$emit("dispatchlayerspan",this.layerspan);
    }
  },
  data(){
    return {
      marks: {
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: '11',
        12: '12'
        },
      layerspan:[1,12]
    }
  }
}
</script>

<style>
#layer-selected{
  width:300px;
  height:5px;
  margin: auto;
}
</style>


