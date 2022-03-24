<template>

  <a-table :data-source="data" :scroll="{y: 100 }" :pagination='pagination' :customRow="customRow">
    <a-table-column key="que" title="question" data-index="que" :width="240" :height="50"/>
    <a-table-column key="k_accu" title="k" data-index="k_accu" :width="60">
      <template slot-scope="k_accu">
        <em-barchart :rect_data="k_accu"/>
      </template>
    </a-table-column>
    <a-table-column key="em" title="em" data-index="em" :width="30" :disabled="false">
      <template slot-scope="em">
      <a-radio :default-checked="em" />
      </template>
    </a-table-column>
  </a-table>
</template>
<script>
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css';
import * as d3 from "d3";
import axios from 'axios';
import bus from './bus';
import emBarchart from './emBarchart.vue';
const DataUrl = 'http://10.192.9.11:8000/query_que';
export default {
  components: { emBarchart },
    name:'QueCArd',
  data() {
    return {
      pagination: {
        size:'small',
      },
      data: [],
      loading: false,
      busy: false,
      
      columns:[
        {title:'question',
        dataIndex:'que',
        key:'que',
        width:200
        },
        {
          title: 'k',
          dataIndex: 'k_accu',
          key: 'k_accu',
          sorter: (a,b) => a.k_accu-b.k_accu,
        }
      ],
      senIds:[]
    };
  },
  
  created(){
    bus.$on('dispatchSenIds',(val)=>{
      this.senIds=val
      this.update()
    })
  },
  mounted() {
    this.post_then_get([...(new Array(3610)).keys()])
  },
  methods: {
    post_then_get(post_data){
      axios.post(DataUrl,post_data)
      .then(()=>{
        axios.get(DataUrl)
        .then((res)=>{
        this.data=res.data.results
        //this.data)
        this.data.forEach(element => {
          element.key=element.id
        });
      })
    })
    },
    handleTableChange(/* sorter */) {
      //sorter)
      this.data=this.data.sort((x,y)=>{
        return y.k_accu-x.k_accu
      })
    },
    update(){
      this.post_then_get(this.senIds)
    },
    customRow(record){
      return{
        on:{
          click:(e)=>{
            bus.$emit('dispatchqueid',record.id)
            console.log(e.srcElement)
            d3.selectAll('.ant-table-row-cell-break-word')
            .style('background-color', '#ffffff')
            d3.select(e.srcElement)
            .style('background-color', '#e6f7ff')
          }
        }
      }
    }

  },
};
</script>
<style scope>
.ant-table-thead > tr > th, .ant-table-tbody > tr > td {
    padding: 5px 5px;
    overflow-wrap: break-word;
}
.ant-table {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    color: rgba(0, 0, 0, 0.65);
    font-size: .8em;
    font-variant: tabular-nums;
    line-height: 1.5;
    list-style: none;
    font-feature-settings: 'tnum';
    position: relative;
    clear: both;
}
svg {
    display: block;
    max-width: 100%; 
}
.ant-table-pagination.ant-pagination {
    float: right;
    margin: 0px;
}
</style>

