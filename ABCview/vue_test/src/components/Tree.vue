<template>
    <div id="tree" class="view">
        <!-- <single-attr-tree v-if="show_single_tree" :queid_prop='que_id' :ctx_prop='ctx_selected'></single-attr-tree>
        <attr-tree v-else :queid_prop='que_id' :model='layer_tree_model'></attr-tree> -->
        <component :is="current_tree" :queid_prop='que_id' :ctx_prop='ctx_selected' :model_prop='model'/>
    </div>
</template>

<script>
  import SingleAttrTree from './SingleAttrTree.vue'
import AttrTree from './AttrTree.vue';
import bus from './bus';

export default {
    name: "Tree",
    components: {
      SingleAttrTree,
      AttrTree,
    },
    created() {
        
      console.log('single attr tree creat')
      const model_comp={'que':'attr-tree','ctx':'attr-tree','reranker':'attr-tree','reader':'attr-tree','single':'single-attr-tree'}

        bus.$on('change_tree',(val)=>{
            console.log('change tree:'+val)
            this.current_tree=model_comp[val]
            this.model=val
        })
        bus.$on("update_ctx", (val) => {
        this.ctx_selected = val;
      })
      bus.$on("dispatchqueid", (val) => {
        this.que_id = val;
        this.ctx_selected=0
      })
    },
    data(){
        return{
            que_id:1,
            ctx_selected:0,
            show_single_tree:false,
            model:'reader',
            current_tree:'attr-tree'
        }
    }
}
</script>