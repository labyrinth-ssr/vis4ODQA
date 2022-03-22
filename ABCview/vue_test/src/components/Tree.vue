<template>
    <div id="tree">
        <single-attr-tree v-if="show_single_tree" :queid_prop='que_id'></single-attr-tree>
        <attr-tree v-else :queid_prop='que_id' :model='layer_tree_model'></attr-tree>
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
        bus.$on('showsingletree',(val)=>{
            this.show_single_tree=val;
        })
        bus.$on("layer_tree_model",(model) => {
            this.model = model;
        }),
        bus.$on("update_ctx", (val) => {
        this.ctx_selected = val;
      }),
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
            layer_tree_model:'reader'
        }
    }
}
</script>