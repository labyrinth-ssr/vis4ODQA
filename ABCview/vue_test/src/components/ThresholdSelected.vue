<template>
  <div id="sliders-button-container">
    <div id="sliders-container">
      <div id="threshold-selected">
        <a-slider :marks="marks_threshold" :max="0.5" :min="0.1" :default-value="0.5" :step="0.01"
          @afterChange="que_thre" />
        <a-slider :marks="marks_threshold" :max="0.5" :min="0.1" :default-value="0.5" :step="0.01"
          @afterChange="ctx_thre" />
        <a-slider :marks="marks_reranker_threshold" :max="0.8" :min="0.4" :default-value="0.7" :step="0.01"
          @afterChange="reranker_thre" />
        <a-slider :marks="marks_threshold" :max="0.5" :min="0.1" :default-value="0.5" :step="0.01"
          @afterChange="reader_thre" />
        <a-radio-group v-model="layer_model" @change="onChange">
          <a-radio-button value="que">
            question
          </a-radio-button>
          <a-radio-button value="ctx">
            context
          </a-radio-button>
          <a-radio-button value="reranker">
            reranker
          </a-radio-button>
          <a-radio-button value="reader">
            reader
          </a-radio-button>
          <a-radio-button value="single">
            model-comparison
          </a-radio-button>
        </a-radio-group>
        <!-- <a-button @click="showSingleTree(true)">model-comparison</a-button> -->
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
  name: "ThresholdSelected",
  methods: {
    onChange(e) {
      //`checked = ${e.target.value}`);
      bus.$emit('change_tree',e.target.value)
      // if(e.target.value=='single'){
      // bus.$emit('showsingletree',true)
      // }
      // else{
      // bus.$emit('layer_tree_model',e.target.value)
      // }
      // this.$emit('showsingletree',false)
    },
    que_thre(value) {
      this.threshold = value;
      bus.$emit("que_thre", value);
    },
    ctx_thre(value) {
      bus.$emit("ctx_thre", value);
    },
    reranker_thre(value) {
      bus.$emit("reranker_thre", value);
    },
    reader_thre(value) {
      bus.$emit("reader_thre", value);
    },
    change_layer(val){
      this.layer=val;
      bus.$emit('set_layer',this.layer);
    },
    // input_sentenceId(){
    //   //"input"+this.input_value)
    //   bus.$emit('dispatchsentencetoshow',this.input_value)
    // },
    showSingleTree(val){
      //val)
      bus.$emit('showsingletree',val)
    }
  },
  data() {
    return {
      input_value:1,
      layer_model:'reader',
      marks_threshold: {
        0.1: "0.1",
        // 0.2: "0.2",
        // 0.3: "0.3",
        // 0.4: "0.4",
        0.5: "0.5",
      },
      marks_reranker_threshold: {
        0.4: "0.4",
        // 0.5: "0.5",
        // 0.6: "0.6",
        // 0.7: "0.7",
        0.8: "0.8"
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
  /* display: flex; */
  width: 40;
  height: 100%;
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
#sliders-container{
  width:300px
}
</style>