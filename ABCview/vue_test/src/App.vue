<template>

  <div id="app">

    <div id="leftCol">
      <div id="leftUp">
        <que-sankey></que-sankey>
      </div>
      <div id="leftMiddle">
        <que-card></que-card>
      </div>
      <div id="leftBottom">
        <context-table></context-table>>
      </div>
    </div>
    <div id="rightCol">
      <div id="upRow">
        <div id="attrTree_container">
          <!-- <ThresholdSelected /> -->
          <div id="left-tree">
            <single-attr-tree></single-attr-tree>
          </div>
          <div id="right-selector">
            <threshold-selected />
          </div>
        </div>
      </div>
      <div id="downRow">
        <div id="left-instance">
          <instance-view></instance-view>

        </div>
        <div id="right-selector">
          <threshold-instance-view />
        </div>
      </div>
    </div>

  </div>

</template>

<script>
  import SingleAttrTree from './components/SingleAttrTree.vue'
  // import queThreBox from "./components/queThreBox.vue";
  import QueSankey from "./components/QueSankey.vue";
  import QueCard from './components/queCard.vue';
import ThresholdSelected from './components/ThresholdSelected.vue';
import ContextTable from './components/contextTable.vue';
import InstanceView from './components/InstanceView.vue';
import ThresholdInstanceView from './components/ThresholdInstanceView.vue';

  export default {
    name: "App",
    components: {
      // queThreBox,
      QueSankey,
      QueCard,
      SingleAttrTree,
      ThresholdSelected,
      ContextTable,
      InstanceView,
      ThresholdInstanceView
    },
    data(){
      return{
        collapsed:false
      }
    }
  };
</script>

<style>
  html,
  body {
    height: 100%;
    padding: 0;
    margin: 0;
  }

  #app {
    background: rgba(155, 223, 255, 0.123);
    display: flex;
    height: 100%;
    width: 100%;
    box-sizing: border-box;
    overflow: auto;
    flex-direction: row;
  }

  #leftCol {
    flex: left;
    width: 400px;
  }

  #rightCol {
    margin-left: 10px;
  }

  #leftUp {
    height: 40%;
  }

  #leftMiddle {
    /* top: 40%; */
    /* height: 55%; */
    padding-left: 25px;
  }

    #leftBottom {
    /* top: 40%; */
    /* height: 55%; */
    padding-left: 25px;
  }
  #attrTree_container {
    box-sizing: border-box;
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
  }

  #upRow {
    top: 0%;
    height: 50%;
  }

  #downRow {
    display: flex;
  }
  #left-tree{
    width: 800px;
  }
  #left-instance{
    width: 900px;
  }

</style>