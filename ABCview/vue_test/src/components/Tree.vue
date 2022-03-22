<template>
    <div id="tree">
        <single-attr-tree v-if="show_single_tree"></single-attr-tree>
        <attr-tree v-else></attr-tree>
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
        this.set_para_update();
      }),
      bus.$on("dispatchqueid", (val) => {
        this.que_id = val;
        this.ctx_selected=0
        this.set_para_update();
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