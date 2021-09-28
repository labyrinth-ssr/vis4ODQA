<template>
  <div id="attr-tree"></div>
</template>

<script>
//增加控件的话，其实最好是搞个默认..
import * as d3 from "d3";
import axios from "axios";
import {
  sankey as d3Sankey,
  sankeyLinkHorizontal as d3SsankeyLinkHorizontal,
  sankeyLeft as d3SankeyLeft
} from "d3-sankey"; 
import bus from './bus';

export default {
  name: "AttrTree",
  created(){//为什么是在created中监听？
    bus.$on('dispatchsentencetoshow',val=>{
      this.tokens=val[0]
      var temp=[]
      val[0].forEach(function(token,index){
          temp.push({'node': `${index}`, 'name': token})
      })
      this.nodes=temp
      this.sentence_selected = val[1];

      this.set_para(this.threshold,this.layer)
    }),
    bus.$on('dispatchthreshold',val=>{
      this.threshold=val;
      console.log('on val:'+val)
      
      this.set_para(this.threshold,this.layer)
    }),
    bus.$on('set_layer',val=>{
      this.layer=val;
      this.set_para(this.threshold,this.layer)

    })
  },
  data() {
    return {
      data: [],
      sentence_selected:5, //初始时自动选择第6句
      tokens:[],
      nodes:[],
      threshold:0.4,
      layer:12
      
    };
  },
  methods: {
update(){
      
      this.getAll();
    },
    draw(sankeydata,textData,nodesData) {//sankeydata:node,link
    console.log(nodesData);
d3.select('#AttrTreeSvg').remove()
      d3.select('#AttrTreeSvg')
        .selectAll('*')
        .remove();
      var margin = { top: 10, right: 10, bottom: 30, left: 1 },
        width = document.getElementById('attr-tree').clientWidth - margin.left - margin.right,
        height = document.getElementById('attr-tree').clientHeight - margin.top - margin.bottom;
      const sankeyWidth=width,snakeyHeight=height;

      var  color = d3.scaleOrdinal(d3.schemePaired);
      
      const textData_index=Object.keys(textData)

        const x = d3.scaleBand().domain(textData_index).range([0,height]).padding(0);

      // append the svg object to the body of the page
      var svg = d3
        .select("#attr-tree")
        .append("svg")
        .attr('id','AttrTreeSvg')
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style('background-color','white')
        .style("border-radius",'10px')
        .append("g")
        .attr('id','g-sankey-scale')
        .attr("transform", " translate(" + (margin.left) + "," +( margin.top )+ ") ")

      // Set the sankey diagram properties
      var sankey = d3Sankey()
        .nodeWidth(36)
        .nodePadding(0)//最好换成一个函数
        .size([sankeyWidth,snakeyHeight])
        .nodeId(function id(d) {
          return d.node;
        })
        .nodeSort(function(a,b){
          return a.node-b.node
        })
        .nodeAlign(d3SankeyLeft)
        .nodes(nodesData)


      var graph = sankey(sankeydata);

      graph.nodes.forEach(node => {
          var newY=x(node.node)
          var yGAp=x.bandwidth()
          node.y0=newY
          node.y1=newY+yGAp
        });
        // console.log(graph.nodes);

        graph.links.forEach(link => {
          link.width=x.bandwidth()
        });

        sankey.update(graph)

      // add in the links
      var link = svg
        .append("g")
        .selectAll(".link")
        .data(graph.links)
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("d", d3SsankeyLinkHorizontal())
        .attr('fill','none')
        .attr('stroke',function(d){
          return color(d.source.name.replace(/ .*/, ""))
        })
        .style('opacity',0.3)
        .style("stroke-width", function (d) {
          return d.width;
        })
        .on('mouseover',function(){
          d3.select(this).style('opacity',0.6)
        })
        .on('mouseleave',function(){
          d3.select(this).style('opacity',0.3)
        })

      // add the link titles
      link.append("title").text(function (d) {
        return d.source.name + " → " + d.target.name ;
      });

      // add in the graph
      var node = svg
        .append("g")
        .selectAll(".node")
        .data(graph.nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        // .attr('id','nodeBox')
        

      

      // add the rectangles for the graph
      node
        .append("rect")
        .attr('class','nodeRect')
        .attr("x", function (d) {
          return d.x0;
        })
        .attr("y", function (d) {
          return d.y0;
        })
        .attr("height", function (d) {
          // return d.y1-d.y0;

          return Math.max(1,d.targetLinks.length)*x.bandwidth() ;
        })
        .attr("width", sankey.nodeWidth())
        .on('click',function(event,data){
          bus.$emit("dispatchtokentoshow",data.index)
        })
        .on('mouseover',function(event,data){
          bus.$emit('highlightToken',data.index)
        })
        .on('mouseleave',function(e,data){
          bus.$emit('unhighlight',data.index)
        })
        .style("fill", function (d) {

          if((d.targetLinks.length+d.sourceLinks.length)=== 0){
            return 'none';
          }
          return (d.color = color(d.name.replace(/ .*/, "")));
        })
        .style("stroke",'none')
        .style("opacity",0.5)
        .append("title")
        .text(function (d) {
          return d.name ;
        })
      //   d3.selectAll('.nodeRect').append('g') 
      // .data(d3.select(this.parentNode).datum())
      node.attr('class','textG')
      .append('text')
      .attr('font-size',10)
      .text(function(d){
        return d.name
      })
      .attr('transform',function(d){
        return 'translate('+d.x0+','+(d.y0+1/2*Math.max(1,d.targetLinks.length)*x.bandwidth()+5) +') '
      })
      .attr('text-anchor','start')

      d3.select('#AttrTreeSvg').attr('height',document.getElementById('g-sankey-scale').getBBox().height+margin.top)
      d3.select('#AttrTreeSvg').style('background-color','white')
        .style("border-radius",'10px')
        .style("margin",'10px')
        .style('margin-left','0px')
      
      var valued_nodes=graph.nodes.filter(node=>node.targetLinks.length+node.sourceLinks.length!==0).map(node=>node.index);
      if(this.threshold===0.4){
        console.log(valued_nodes)
      bus.$emit('init_tokens',valued_nodes);


      }



    },
    getAll(){
      const path='http://10.192.9.11:5000/query_attr_tree/'+this.sentence_selected
      axios.get(path)
        .then((res) => {
          var nodeLinkData = res.data.node_link;
        var tokens=res.data.tokens
        if(this.tokens.length!=0){
            tokens=this.tokens
          }
        var nodesData=nodeLinkData.nodes//未选过sentence，直接获得？？？
        if(this.nodes.length!=0){//普通情况：nodes在选sentence时被存了
          nodesData=this.nodes
        }
        this.draw(nodeLinkData,tokens,nodesData);
        }
        )
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    set_para(threshold,layer){
      const path='http://10.192.9.11:5000/query_attr_tree/'+this.sentence_selected
      axios.post(path,{'sts_id':this.sentence_selected,'threshold':threshold,'layer':layer-1})
      .then(()=>{
        this.getAll()
        
      }
      )
    }
  },
  mounted() {
    this.set_para(this.threshold,this.layer)
    // this.getAll()
  },
};
</script>

<style scoped>



#attr-tree{
  margin: 10px;
  margin-left: 0px;
  height: 100%;
  text-align: center;
  width:66.67%;
  overflow: auto;
}
/* #AttrTreeSvg{
 border-radius: 10px;
position: relative;
margin: 10px;
  background-color: white;


} */

</style>

