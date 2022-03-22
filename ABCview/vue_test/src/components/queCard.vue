<template>

  <a-table :data-source="data" :scroll="{y: 100 }" :pagination='true' :customRow="customRow">
    <a-table-column key="que" title="question" data-index="que" :width="240" :height="50"/>
    <a-table-column key="k_accu" title="k" data-index="k_accu" :width="30">
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
import axios from 'axios';
import bus from './bus';
import emBarchart from './emBarchart.vue';
const DataUrl = 'http://10.192.9.11:8000/query_que';
export default {
  components: { emBarchart },
    name:'QueCArd',
  data() {
    return {
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
        sorter: true,
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
          click:()=>{
            //record)
            this.showSingleTree()
            bus.$emit('dispatchqueid',record.id)
          }
        }
      }
    },
    showSingleTree(){
      this.$emit('showsingletree',true)
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
</style>

