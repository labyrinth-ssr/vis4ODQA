<template>
      <div id="threshold-selected">
        <a-slider :marks="marks_threshold" :max="0.5" :min="0.1" :default-value="0.5" :step="0.01"
          @afterChange="que_thre" :disabled='disables[0]'  class="tree-thre"/>
        <a-slider :marks="marks_threshold" :max="0.5" :min="0.1" :default-value="0.5" :step="0.01"
          @afterChange="ctx_thre" :disabled='disables[1]' class="tree-thre"/>
        <a-slider :marks="marks_reranker_threshold" :max="0.8" :min="0.4" :default-value="0.7" :step="0.01"
          @afterChange="reranker_thre" :disabled='disables[2]' class="tree-thre"/>
        <a-slider :marks="marks_threshold" :max="0.5" :min="0.1" :default-value="0.5" :step="0.01"
          @afterChange="reader_thre" :disabled='disables[3]' class="tree-thre"/>
        <a-select default-value="que" style="width: 100px" @change="onChange" class="tree-selector">
          <a-select-option value="que"> question </a-select-option>
          <a-select-option value="ctx"> context </a-select-option>
          <a-select-option value="reranker"> reranker </a-select-option>
          <a-select-option value="reader"> reader </a-select-option>
          <a-select-option value="single"> model comparison </a-select-option>
        </a-select>
        <!-- <a-radio-group v-model="layer_model" @change="onChange">
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
        </a-radio-group> -->
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
    <!-- <div id="input-container">
      <div id="input-box">
        <a-input v-model="input_value" @pressEnter="input_sentenceId" />
      </div>
    </div> -->

</template>

<script>
import bus from "./bus";

export default {
  name: "ThresholdSelected",
  methods: {

    onChange(val) {
      //`checked = ${e.target.value}`);
      bus.$emit('change_model',eval)
      // console.log(e.target)
      switch (val) {
        case 'que':this.disables=[false,true,true,true];break;
        case 'ctx':this.disables = [true, false,true,true];break;
        case 'reranker':this.disables = [true, true,false,true];break;
        case 'reader':this.disables = [true, true,true,false];break;
        case 'single':this.disables = [false, false,false,false];break;
      }
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
      disables:[false,false,false,false],
      input_value:1,
      layer_model:'single',
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

#title {
  margin: 0px 40px;
}
#sliders-container{
  width:300px
}

.tree-thre .tree-selector{
  flex: 0 0 10%;
}

.ant-slider-mark {
    position: absolute;
    top:-9px;
    left:-15px;
    width: 100%;
    font-size: 10px;
}
.ant-slider-with-marks {
    margin-bottom: 0px;
    width: 80px;
}
</style>