<template>
      <div id="ins-thre">
        <h5 class='thre-title' id="salthre_title">sal_th</h5>
        <a-slider id="sal_thre" :marks="marks_threshold" :max="0.05" :min="0.01" :step="0.01" :default-value="0.03"
          @afterChange="que_sal_thre" />
        <h5 class='thre-title' id="octhre_title">occur_th</h5>
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
        0.01: {
          style:{
            transform: 'translateX(-140%)',
            left: '0%'
          },
          label: '0.01'
        },
        // 0.02: "0.02",
        // 0.03: "0.03",
        // 0.04: "0.04",
        0.05: {
          style:{
            transform: 'translateX(65%)',
            left: '100%'
          },
          label: '0.05'
        }
      },
      marks_barchart_threshold: {
        3: {
          style:{
            transform:     'translateX(-254%)',
            left: '0%'
          },
          label: '3'
        },
        // 4: "4",
        // 5: "5",
        // 6: "6",
        7: {
          style:{
            transform: 'translateX(148%)',
            left: '100%'
          },
          label: '7'
        }
      },
    };
  },
};
</script>

<style>
#ins-thre {
  display:flex;
  justify-content: flex-start;;
  padding: 0 10% 0 0;
  flex:0 0 70%;
}
#sal_thre{
  flex: 0 0 30%;
}
#bar_thre{
  flex: 0 0 30%;
}
#salthre_title{
    margin-right: 30px;  
}
#octhre_title{
  margin-left:40px;
    margin-right: 15px;  


}

</style>