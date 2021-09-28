<template>
  <div id="sliders-button-container">
    <div id="title" class="chart-title">
      <a-button
        id="resetButton"
        type="primary"
        size="small"
        v-on:click="reset_tokens"
        >Clear tokens></a-button
      >
    </div>
    <div id="sliders-container">
      <div id="threshold-selected">
        <a-slider
          :marks="marks_threshold"
          :max="0.5"
          :min="0.1"
          :step="0.1"
          :default-value="0.4"
          @afterChange="onAfterChange"
        />
      </div>
      <div id="layer-selected">
        <a-slider
          :marks="marks_layer"
          :max="12"
          :min="1"
          :step="1"
          :default-value="12"
          @afterChange="change_layer"
        />
      </div>
    </div>
  </div>
</template>

<script>
import bus from "./bus";

export default {
  name: "ThresholdSelected",
  methods: {
    onAfterChange(value) {
      this.threshold = value;
      bus.$emit("dispatchthreshold", this.threshold);
    },
    change_layer(val){
      this.layer=val;
      bus.$emit('set_layer',this.layer);
    },
    reset_tokens(){
      bus.$emit('reset_tokens');

    }
  },
  data() {
    return {
      marks_threshold: {
        0.1: "0.1",
        0.2: "0.2",
        0.3: "0.3",
        0.4: "0.4",
        0.5: "0.5",
      },
      marks_layer:{
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
      threshold: 0.4,
      layer:12,
    };
  },
};
</script>

<style>
#sliders-button-container {
  display: flex;
  width: 100;
  height: 8%;
  overflow: visible;
}
#slider2-container{
  overflow: visible;
}
#threshold-selected {
  position: relative;
  left: 10%;
  width: 50%;
  height: 50%;
}
#title {
  margin: 0px 40px;
}
</style>