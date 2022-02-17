<template>
  <div id="app">
    <div id="leftCol">
      <div id="row1">
        <div id="tableContainer" class="container">
          <ScrollingTable />
          <TokenTable />
        </div>
      </div>
      <div id='row2'>
        <div id="sleftCol">
          <div id="tsneContainer" class="container">
            <LayerSelected />
            <ScatterPlot />
          </div>
        </div>
        <div id="srightCol">
          <div id="att_container" class="container">
            <AttnHead></AttnHead>
          </div>
        </div>
      </div>
    </div>

    <div id="rightCol">
      <div id="attrTree_container" class="container">
        <ThresholdSelected />
        <div id="bottomRow">
          <attnMap></attnMap>
          <AttrTree></AttrTree>
        </div>
      </div>
    </div>

  </div>

</template>

<script>
import ScatterPlot from "./components/ScatterPlot.vue";
import LayerSelected from "./components/LayerSelected.vue";
import ScrollingTable from "./components/ScrollingTable.vue";
import TokenTable from "./components/TokenTable.vue";
import AttnHead from "./components/headView.vue";
import AttrTree from "./components/AttrTree.vue";
import ThresholdSelected from "./components/ThresholdSelected.vue";
import attnMap from './components/attnMap.vue';

export default {
  name: "App",
  components: {
    ScrollingTable,
    ScatterPlot,
    LayerSelected,
    TokenTable,
    AttnHead,
    AttrTree,
    ThresholdSelected,
    attnMap
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
  background: rgba(155, 223, 255, 0.123) ;
  display: flex;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  overflow: auto;
  flex-direction: row;
}
#leftCol {
  width: 0%;
  flex-direction: column;
  overflow: hidden;

}
#rightCol {
  width: 100%;
}

#row1 {
  display: flex;
  box-sizing: border-box;

  height: 40%;
  border: 1px solid darkgrey;

}
#row2 {

  display: flex;
  flex-direction: row;
  height: 60%;

}
#sleftCol {
  width: 48%;
  /* border: 1px solid darkgrey; */
  border-top:none

}
#srightCol {
  width: 52%;
  /* attn-graph与attn-map间的边框 */
  border: 1px solid darkgrey;
  border-top:none;



}
/* .container{
  
} */
#tableContainer{
  box-sizing: border-box;
  display: flex;
  flex-direction: column;

}
#attrTree_container{
  box-sizing: border-box;
  position: relative;
  width: 100%;
  height: 100%;
}
#bottomRow{
  top: 15%;
  height: 85%;
  display: flex;
  flex-direction: row;
}


/* #AttrTree{
  width: 66.67%;
  
} */


/* .ant-row {
  box-sizing: border-box;
  height: 50%;
  width: 100%;
}
/* #row2{
  box-sizing: border-box;
  height: 40%;
  width: 100%;
} */
/* .ant-col {
  box-sizing: border-box;
  height: 100%;
}  */
/* .container {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
  border: 1px solid darkgrey;
  overflow: auto;
} */

/* #sentence {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
.project-title {
  margin: 1rem 0 1rem 0;
} */

</style>
