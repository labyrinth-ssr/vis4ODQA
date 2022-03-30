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
  @page{
   size: auto;
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
    flex: 0 0 /* 35% */537.6px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    /* margin-bottom: 10px; */
  }

  /* #rightCol {
    flex: 0 0
  } */

  #leftUp {
    flex: 0 0 /* 50% */360.8px;
    overflow: hidden;
    justify-content: space-between;

  }
  /* 62 -40=22 */
  #context-view {
    display: flex;
    overflow: hidden;
    flex-direction: column;
    flex:0 0 350.8px;
  }

  #leftMiddle {
    overflow: hidden;
    margin: 0 5%;
    flex: 0 0 /* 53% */140.6px;

  }

    #leftBottom {
    /* top: 40%; */
    /* height: 55%; */
    flex: 0 0 /* 53% */220.6px;
    overflow: hidden;
    margin: 0 2%;
  }

  #rightCol {
    display: flex;
    flex: 0 0 998.4px;
    flex-direction: column;
    overflow: hidden;
    /* justify-content: space-between; */
  }

  #attrTree_container {
    /* position: relative; */
    width: 100%;
    height: 100%;
    display: flex;
    overflow: hidden;
  }

  #upRow {
    flex: 0 0 360.8px;
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
    flex:0 0 360.8px;
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
    /* padding:5px 5px 5px 2px; */
    border-radius:6px;
    /* box-shadow: 2.5px 2.5px 10px rgb(180, 180, 180); */
    overflow: hidden;
    height: 98%;
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
  background:#f1f1f1;
  margin-bottom: 0em;
}
#ins-head{
  background-color: #f1f1f1;
}


</style>