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
      </div>
    </div>
    <div id="rightCol">
      <div id="upRow">
        <div id="attrTree_container">
          <ThresholdSelected />
          <div id="bottomRow">
            <single-attr-tree></single-attr-tree>
          </div>
        </div>
      </div>
      <div id="downRow">
        <div id="sunburstCon">
          <div id="queThreCon">
            <que-thre-box></que-thre-box>
          </div>
        </div>
        <div id="att_container" class="container">
          <AttnHead></AttnHead>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AttnHead from "./components/headView.vue";
// import AttrTree from "./components/AttrTree.vue";
import SingleAttrTree from './components/SingleAttrTree.vue'
import ThresholdSelected from "./components/ThresholdSelected.vue";
import queThreBox from "./components/queThreBox.vue";
// import queSunburst from './components/queSunburst.vue'
import QueSankey from "./components/QueSankey.vue";
import QueCard from './components/queCard.vue';

export default {
  name: "App",
  components: {
    AttnHead,
    // AttrTree,
    ThresholdSelected,
    queThreBox,
    // queSunburst,
    QueSankey,
    QueCard,
    SingleAttrTree,
  },
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
#leftCol{
  flex: left;
  width: 450px;
}
#rightCol{
  margin-left: 10px;
}
#leftUp{
  height: 50%;
}
#leftMiddle{
  /* top: 40%; */
  /* height: 55%; */
  padding-left: 25px;
}
#attrTree_container {
  box-sizing: border-box;
  position: relative;
  width: 100%;
  height: 100%;
}
#bottomRow {
  top: 15%;
  height: 85%;
  display: flex;
  flex-direction: row;
}
#upRow {
  top: 0%;
  height: 60%;
}
#downRow {
  display: flex;
}
</style>