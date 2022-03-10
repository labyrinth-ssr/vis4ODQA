<template>
  <div id="que_sankey"></div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import {
  sankey as d3Sankey,
  sankeyLinkHorizontal as d3SankeyLinkHorizontal,
  sankeyLeft as d3SankeyLeft,
} from "d3-sankey";
// import bus from "./bus";

export default {
  name: "QueSankey",
  created() {
    // bus.$on("", (val) => {
    // })
  },
  data() {
    return {
      node_link: {},
      threshold: 100,
      head: 0,
      layer: 0,
      attn: {},
    };
  },
  methods: {
    update() {},
    draw() {
      var sankeydata = this.node_link;
      var attndata = this.attn;
      const margin = { top: 10, right: 10, bottom: 10, left: 10 };
      const svg_size = { width: 400, height: 800 };
      const sankey_size = {
        width: 150,
        height: 380,
      };
      // const attn_size = { width: 15, height: 15 };

      var svg = d3
        .select("#que_sankey")
        .append("svg")
        .attr("width", svg_size.width)
        .attr("height", svg_size.height)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      const color = d3.scaleOrdinal(d3.schemePaired);
      var sankey = d3Sankey()
        .nodeWidth(15)
        .nodePadding(0)
        .size([sankey_size.width, sankey_size.height])
        .nodeId(function id(d) {
          return d.node;
        })
        .nodeAlign(d3SankeyLeft);
      var graph = sankey(sankeydata);
      console.log(graph);
      var link = svg
        .append("g")
        .selectAll(".link")
        .data(graph.links)
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("d", d3SankeyLinkHorizontal())
        .attr("fill", "none")
        .attr("stroke", function (d) {
          return (d.color = color(d.source.name.replace(/ .*/, "")));
        })
        .style("opacity", 0.5)
        .style("stroke-width", d=>d.width)
        .on("mouseover", function () {
          d3.select(this).style("opacity", 0.8);
        })
        .on("mouseleave", function () {
          d3.select(this).style("opacity", 0.5);
        });
      console.log(link);

      var node = svg
        .append("g")
        .selectAll(".node")
        .data(graph.nodes)
        .enter()
        .append("g")
        .attr("class", "node");

      node
        .append("rect")
        .attr("x", (d) => {
          return d.x0;
        })
        .attr("y", (d) => {
          return d.y0;
        })
        .attr("height", function (d) {
          return d.y1 - d.y0;
        })
        .attr("width", sankey.nodeWidth())
        .style("fill", function (d) {
          return (d.color = color(d.name.replace(/ .*/, "")));
        })
        .style("stroke", "none")
        .style("opacity", 1);
      node
        .append("text")
        .attr("font-size", 10)
        .text(function (d) {
          return d.name;
        })
        .attr("transform", function (d) {
          return (
            "translate(" +
            d.x0 +
            "," +
            (d.y0 + 0.5 * (d.y1 - d.y0)) +
            ") rotate(-90)"
          );
        })
        .attr("text-anchor", "middle");
      svg.attr("transform", "translate(400,10)rotate(90)");

      const bias=8

      const attn_color = d3
        .scaleSequential()
        .interpolator(d3.interpolateGnBu)
        .domain([0, 2.54]);
        var links_data=sankeydata.links
      links_data.sort((a,b)=>{
        return a.y1-b.y1
      })
      const rect_padding=5
      const rect_height=10
      const rect_width=(sankey_size.height/ links_data.length)-rect_padding
      links_data.forEach((ele,index)=>{
        ele.index=index
      })

      var attn_g = d3.select("svg").append("g").attr("id", "attn_g")
      .attr('transform','translate('+(margin.left-bias)+','+(margin.top+sankey_size.width+rect_padding)+')');

      
      //取出所有的y1排序后将index存入links
      var attn = attn_g
        .append("g")
        .selectAll(".attn_col")
        .data(attndata)
        .enter()
        .append("g")
        .attr('transform',(d)=>{
          const link_data=sankeydata.links
          
          console.log(d.source,d.target)
          console.log(link_data.filter(link=>
            link.source.name==d.source&&link.target.name==d.target
          )[0])
          const link_index=link_data.filter(link=>
            link.source.name==d.source&&link.target.name==d.target
          )[0].index
            return 'translate('+(sankey_size.height-(link_index*(rect_width+rect_padding)))+',0)'
        }
          )
        .attr("class", "attn_col");

      // 对应的数据，已经列出，需要匹配，按照senid匹配？，按照source和target匹配。
      
      attn
        .append("g")
        .selectAll(".layer_attn")
        .data((d)=>{
          const link_data=sankeydata.links
          const width=link_data.filter(link=>
            link.source.name==d.source&&link.target.name==d.target
          )[0].width
          d.layer_impo.forEach(ele => {
            ele['width']=width
          });
          return d.layer_impo
        })
        .enter()
        .append("g")
        .attr('class','layer_attn')

      d3.selectAll('.layer_attn').append('rect')
        .attr("y",(d)=>{
          return d.layer*(rect_height+rect_padding)
        })
        .attr("width", rect_width)
        .attr("height", rect_height)
        .attr('fill',d=>attn_color(d.val)
        )
    },
    //有两种方法：是否使用两个url？
    
    // draw_attn(){
    // },
    init() {
      const path = "http://localhost:5000/query_que_sunburst";
      const path2 = "http://localhost:5000/query_attn_head";
      const requestOne = axios.get(path);
      const requestTwo = axios.get(path2);
      axios
        .post(path, {
          threshold: this.threshold,
          head: this.head,
          layer: this.layer,
        })
        .then(() => {
          axios
            .all([requestOne, requestTwo])
            .then(
              axios.spread((...responses) => {
                const responseOne = responses[0];
                const responseTwo = responses[1];
                this.node_link = responseOne.data;
                this.attn = responseTwo.data;
                this.draw();
              })
            )
            .catch((error) => {
              console.error(error);
            });
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  beforeMount() {
    this.init();
  },
};
</script>

<style scoped>
</style>

