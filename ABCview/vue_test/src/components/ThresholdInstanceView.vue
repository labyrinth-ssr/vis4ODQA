<template>
      <div id="ins-thre">
        <a-slider id="sal_thre" :marks="marks_threshold" :max="0.05" :min="0.01" :step="0.01" :default-value="0.03"
          @afterChange="que_sal_thre" />
        <a-slider id="bar_thre" :marks="marks_barchart_threshold" :max="7" :min="3" :step="1" :default-value="5"
          @afterChange="barchart_thre" />
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
#ins-thre {
  display:flex;
  justify-content: space-evenly;
  padding: 0 10%;
  flex:0 0 70%;
}
#sal_thre{
  flex: 0 0 30%;
}
#bar_thre{
  flex: 0 0 30%;
}

</style>