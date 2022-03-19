<template>
  <div id="sliders-button-container">
    <div id="sliders-container">
      <div id="threshold-instanceview">
        <a-slider
          :marks="marks_threshold"
          :max="0.05"
          :min="0.01"
          :step="0.01"
          :default-value="0.03"
          @afterChange="que_sal_thre"
        />
        <!-- <a-slider
          :marks="marks_threshold"
          :max="0.05"
          :min="0.01"
          :step="0.01"
          :default-value="0.03"
          @afterChange="ctx_sal_thre"
        />
        <a-slider
          :marks="marks_threshold"
          :max="0.05"
          :min="0.01"
          :step="0.01"
          :default-value="0.03"
          @afterChange="reranker_sal_thre"
        />
        <a-slider
          :marks="marks_threshold"
          :max="0.05"
          :min="0.01"
          :step="0.01"
          :default-value="0.03"
          @afterChange="reader_sal_thre"
        /> -->
        <a-slider
          :marks="marks_barchart_threshold"
          :max="7"
          :min="3"
          :step="1"
          :default-value="5"
          @afterChange="barchart_thre"
        />
      </div>
      <!-- <div id="layer-selected">
        <a-slider
          :marks="marks_layer"
          :max="12"
          :min="1"
          :step="1"
          :default-value="12"
          @afterChange="change_layer"
        />
      </div> -->
    </div>
    <!-- <div id="input-container">
      <div id="input-box">
        <a-input v-model="input_value" @pressEnter="input_sentenceId" />
      </div>
    </div> -->
      
  </div>
</template>

<script>
import bus from "./bus";

export default {
  name: "ThresholdInstanceView",
  methods: {
    que_sal_thre(value) {
      this.threshold = value;
      bus.$emit("que_sal_thre", value);
    },
    // ctx_sal_thre(value) {
    //   bus.$emit("ctx_sal_thre", value);
    // },
    // reranker_sal_thre(value) {
    //   bus.$emit("reranker_sal_thre", value);
    // },
    // reader_sal_thre(value) {
    //   bus.$emit("reader_sal_thre", value);
    // },
    barchart_thre(value) {
      bus.$emit("barchart_thre", value);
    },
  },
  data() {
    return {
      input_value:1,
      marks_threshold: {
        0.01: "0.01",
        0.02: "0.02",
        0.03: "0.03",
        0.04: "0.04",
        0.05: "0.05",
      },
      marks_barchart_threshold: {
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7"
      },
    };
  },
};
</script>

<style>
#sliders-button-container {
  /* display: flex; */
  width: 40;
  height: 100%;
  overflow: visible;
}
#slider2-container{
  overflow: visible;
}
#threshold-instanceview {
  position: relative;
  left: 10%;
  width: 50%;
  height: 50%;
}
#title {
  margin: 0px 40px;
}
#sliders-container{
  width:300px
}
</style>