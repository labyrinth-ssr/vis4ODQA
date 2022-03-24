<template>
  <div id="app">
    <div id="leftCol">
      <div id="leftUp">
        <que-sankey></que-sankey>
      </div>
      <div id='context-view' class="view">
        <h2>Context View</h2>
      <div id="leftMiddle">
        <que-card ></que-card>
      </div>
      <div id="leftBottom">
        <context-table></context-table>>
      </div>
      </div>
    </div>
    <div id="rightCol">
      <div id="upRow">
            <tree/>
      </div>
      <div id="downRow">
        <!-- <div id="left-instance"> -->
          <instance-view ></instance-view>
        <!-- </div> -->
        <!-- <div id="right-selector"> -->
          <!-- <threshold-instance-view /> -->
        <!-- </div> -->
      </div>
    </div>
  </div>

</template>

<script>
  // import SingleAttrTree from './components/SingleAttrTree.vue'
  // import queThreBox from "./components/queThreBox.vue";
import QueSankey from "./components/QueSankey.vue";
import QueCard from './components/queCard.vue';
import ContextTable from './components/contextTable.vue';
import InstanceView from './components/InstanceView.vue';
// import ThresholdInstanceView from './components/ThresholdInstanceView.vue';
// import AttrTree from './components/AttrTree.vue';
import Tree from './components/Tree.vue';

  export default {
    name: "App",
    components: {
      // queThreBox,
      QueSankey,
      QueCard,
      // SingleAttrTree,
      ContextTable,
      InstanceView,
      // ThresholdInstanceView,
      // AttrTree,
        Tree
    },
    data(){
      return{
        flag: false,
        collapsed:false
      }
    },
    methods:{
      showSingleTree(visible) {
        //visible)
        this.flag = visible;
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
    background: white;
    display: flex;
    height: 100%;
    width: 100%;
    overflow: hidden;

    /* box-sizing: border-box;
    overflow: auto;
    flex-direction: row; */
  }

  #leftCol {
    flex: 0 0 35%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin-bottom: 10px;
  }

  /* #rightCol {
    flex: 0 0
  } */

  #leftUp {
    flex: 0 0 50%;
    overflow: hidden;
    justify-content: space-between;

  }
  /* 62 -40=22 */
  #context-view {
    display: flex;
    overflow: hidden;
    flex-direction: column;

  }

  #leftMiddle {
    overflow: hidden;
    margin: 0 5%;
  }

    #leftBottom {
    /* top: 40%; */
    /* height: 55%; */
    flex: 0 0 45%;
    overflow: hidden;
    margin: 0 5%;
  }

  #rightCol {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    justify-content: space-between;
  }

  #attrTree_container {
    /* position: relative; */
    width: 100%;
    height: 100%;
    display: flex;
    overflow: hidden;
  }

  #upRow {
    flex: 0 0 50%;
    overflow: hidden;
    padding-bottom:0px;
    /* margin-bottom: 10px; */
  }

    #left-tree{
    flex: 0 0 80%;
    overflow: hidden;
    /* width: 800px; */
  }

  #downRow {
    display: flex;
    overflow: hidden;
    flex:0 0 50%;
    margin-top: 0px;
  }

  #left-instance{
    flex: 0 0 80%;
    /* width: 900px; */
    overflow: hidden;

  }

  .view{
    margin: 5px;
    border: 1px solid #ccc!important;
    padding:15px 5px 5px 5px;
    border-radius:16px;
    box-shadow: 2.5px 2.5px 10px rgb(180, 180, 180);
    overflow: hidden;
    height: 95%;
  }

  ::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 0;
}

::-webkit-scrollbar {
  -webkit-appearance: none;
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-thumb {
  cursor: pointer;
  border-radius: 5px;
  background: rgba(0, 0, 0, 0.15);
  transition: color 0.2s ease;
}
h2 {
  font-size: 15px;
}

</style>