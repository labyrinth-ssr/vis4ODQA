<template>
  <div id="attr-tree"></div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import {
  sankey as d3Sankey,
  sankeyLinkHorizontal as d3SsankeyLinkHorizontal,
  sankeyLeft as d3SankeyLeft,
} from "d3-sankey";
import bus from "./bus";

export default {
  name: "AttrTree",
  watch:{
    model_prop:function(newval){
      if (newval!='single'){
      this.model = newval;
        this.set_para();
      }
    },
    queid_prop:function(newval){
      this.que_id=newval;
      this.top_kth=0;
        this.set_para();
    },
    ctx_prop:function(newval){
      this.top_kth=newval;
      this.set_para();
    }
  },
  created() {

     bus.$on("que_thre", (val) => {
        this.threshold=val
        this.set_para();
      }),
      bus.$on("ctx_thre", (val) => {
        this.threshold=val
        this.set_para();
      }),
      bus.$on("reranker_thre", (val) => {
        this.threshold=val
        this.set_para();
      }),
      bus.$on("reader_thre", (val) => {
        this.threshold=val
        this.set_para();
      })
  },
  props:['ctx_prop','queid_prop','model_prop'],
  data() {
    return {
      data: [],
      // ctx_selected: 1,
      tokens: [],
      nodes: [],
      threshold: 0.5,
      layer: 10,
      valued_nodes: [],
      sentence_span: [],
      model:'reader',
      top_kth:0,
      que_id:1, 
      first_create:true
    };
  },
  methods: {
    update() {
      this.getAll();
    },
    drawAll(sankeyDataList, tokenPool, tree_height) {

      d3.select("#AttrTreeSvg").remove();
      d3.select("#AttrTreeSvg").selectAll("*").remove();
      var margin = { top: 20, right: 100, bottom: 20, left: 10 },
        height = 270;

      const svg_width=970;
      var color = d3.scaleOrdinal(d3.schemePaired);
      const colors=d3.schemeTableau10.concat(['#8adb82'])
const sentence_color = function (i) {
        if (i == 1) {
          return 7;
        } else if (i == 2) {
          return 8;
        } else if (i == 5) {
          return 9;
        }
        if (i==7) {
          return 10;
        }
        return i;
      };

      const textData_index = tokenPool.map((a) => a + "");

      const x = d3
        .scaleBand()
        .domain(textData_index)
        .range([0, height])
        .padding(0);

      var svg = d3
        .select("#attr-tree")
        .append("svg")
        .attr("id", "AttrTreeSvg")
        .attr("width", svg_width)
        .attr("height", height + margin.top + margin.bottom)
        .style("border-radius", "10px");

      const g2 = svg
        .append("g")
        .attr("id", "colourScale")
        .attr(
          "transform",
          "translate(" +(svg_width-margin.right)+ "," + ( margin.top) + ")"
        );

      g2.append("text").attr("x", 0).text("layer").attr("fill", "black").style('font-size','10px');
      for (let i = 0; i < 12; i++) {
        g2.append("rect")
          .attr("width", "10")
          .attr("y", i * 10 + 10)
          .attr("height", "10")
          .attr("fill", d3.interpolateOrRd((i / 11) * 0.7 + 0.1))
          .attr("opacity", "1");

        g2.append("text")
          .text(`${i}`)
          .attr("y", i * 10 + 20)
          .attr("x", 10)
          .attr("font-size", "10px")
          .attr("fill", "black");
      }
      const g3 = svg
        .append("g")
        .attr("id", "colourScale")
        .attr(
          "transform",
          "translate(" + (svg_width-margin.right+30) + "," + ( margin.top) + ")"
        );

      g3.append("text").text("sentence").attr("fill", "black").style('font-size','10px');
      for (let i = 0; i < 8; i++) {
        g3.append("rect")
          .attr("width", "10")
          .attr("y", i * 10 + 10)
          .attr("height", "10")
          .attr("fill", colors[sentence_color(i)])
          .attr("opacity", "1");

        g3.append("text")
          .text(`${i}`)
          .attr("y", i * 10 + 20)
          .attr("x", 20)
          .attr("font-size", "10px")
          .attr("fill", "black");
      }
      // const x_padding=margin.left;

      const tree_padding = 10;

      const sum_tree_height = tree_height.reduce((prev, cur) => prev + cur, 0);
      const layer_width = ((svg_width-margin.right-margin.left)-(11*tree_padding))/sum_tree_height;

      //35*24=700+140=840
      var pos = 0;
      for (let index = 0; index < 12; index++) {
        var width = tree_height[index] * layer_width;
        if (sankeyDataList[index].links.length == 0) {
          continue;
        }
        this.draw(
          sankeyDataList[index],
          x,
          color,
          index,
          height,
          svg,
          margin,
          width,
          pos,
        );
        pos = pos + width + tree_padding;
      }
    },
    draw(sankeydata, x, color, index, height, svg, margin, width, pos) {
      const sentence_color = function (i) {
        if (i == 1) {
          return 7;
        } else if (i == 2) {
          return 8;
        } else if (i == 5) {
          return 9;
        }
        if (i==7) {
          return 10;
        }
        return i;
      };
      // const la
      //sankeydata:node,link
      //calculate the tree height
      const colors=d3.schemeTableau10.concat(['#8adb82'])
      var links_data = sankeydata.links;
      links_data.sort(function (a, b) {
        return a.layer - b.layer;
      });
      
      const sankeyWidth = width,
        snakeyHeight = height;
      var mySvg = svg
        .append("g")
        .attr("id", "g-sankey-scale")
        .attr(
          "transform",
          " translate(" + (margin.left + pos) + "," + margin.top + ") "
        );

      // Set the sankey diagram properties
      var sankey = d3Sankey()
        .nodeWidth(5)
        .nodePadding(0) //最好换成一个函数
        .size([sankeyWidth, snakeyHeight])
        .nodeId(function id(d) {
          return d.node;
        })
        .nodeSort(function (a, b) {
          return a.node - b.node;
        })
        .nodeAlign(d3SankeyLeft)
        .nodes(sankeydata.nodes);

      var graph = sankey(sankeydata);

      graph.nodes.forEach((node) => {
        var newY = x(node.node);
        var yGAp = x.bandwidth();
        node.y0 = newY;
        node.y1 = newY + yGAp;
      });

      sankey.update(graph);
      graph.links.forEach((link) => {
        link.width = x.bandwidth();
        link.y0 = link.source.y0;
        link.y1 = link.target.y0;
      });

      // add in the links
      var link = mySvg
        .append("g")
        .selectAll(".link")
        .data(graph.links)
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("d", d3SsankeyLinkHorizontal())
        .attr("fill", "none")
        .attr("stroke", function (d) {
          return d3.interpolateOrRd((d.layer / 11) * 0.7 + 0.1);
        })
        .style("opacity", 1)
        .style("stroke-width", function (d) {
          return d.value * 20 - 7;
        })
        .on("mouseover", function () {
          d3.select(this).style("opacity", 0.6);
        })
        .on("mouseleave", function () {
          d3.select(this).style("opacity", 1);
        });

      // add the link titles
      link.append("title").text(function (d) {
        return d.source.name + " → " + d.target.name + "\nlayer:" + d.layer;
      });
      const sentence_span = this.sentence_span;
      // add in the graph
      var node = mySvg
        .append("g")
        .selectAll(".node")
        .data(graph.nodes)
        .enter()
        .append("g")
        .attr("class", "node");
      // .attr('id','nodeBox')
      // add the rectangles for the graph
      node
        .append("circle")
        .attr('id',d=>'node'+d.node)
        .attr("class", "nodeRect")
        .attr("cx", function (d) {
          return d.x0 + sankey.nodeWidth() / 2;
        })
        .attr("cy", function (d) {
          return d.y0;
        })
        .attr("r", function (d) {
          return (Math.max(0, d.saliency) * 30 + 5);
        })
        .on("click", function (event, data) {
          bus.$emit("dispatchtokentoshow", data.index);
        })
                .on('mouseover',function(e,d){
          
          d3.selectAll('#node'+d.node)
          .style('stroke','black')
          .style('stroke-width',3)
        })
        .on('mouseleave',function(e,d){
          d3.selectAll('#node'+d.node)
          .style('stroke','none')
        })
        .style("fill", function (d) {
          if (d.targetLinks.length + d.sourceLinks.length === 0) {
            return "none";
          }
          return (d.color =
            colors[sentence_color(sentence_span[d.node])]);
        })
        .style("stroke", "none")
        .style("opacity", 1)
        .append("title")
        .text(function (d) {
          return d.name + "\nsentence:" + sentence_span[d.node];
        });

      node
        .attr("class", "textG")
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
            (d.y0 - (Math.max(0, d.saliency) * 30 + 5)) +
            ") "
          );
        })
        .attr("text-anchor", "middle");

      d3.select("#AttrTreeSvg")
        .style("background-color", "white")
        .style("border-radius", "10px")
        .style("margin", "10px")
        .style("margin-left", "0px");

      var valued_nodes = graph.nodes
        .filter(
          (node) => node.targetLinks.length + node.sourceLinks.length !== 0
        )
        .map((node) => node.index);
      this.valued_nodes = valued_nodes;
    },
    getAll() {
      const path = "http://10.192.9.11:8000/query_attr_tree"
      axios
        .get(path)
        .then((res) => {
          var all_node_link = res.data.all_layer_node_link.map(
            (a) => a.node_link
          );
          this.sentence_span = res.data.sentence_span;
          this.drawAll(all_node_link, res.data.tokenPool, res.data.tree_height);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    set_para() {
      const path = "http://10.192.9.11:8000/query_attr_tree"
      axios
        .post(path, {
          top_kth:this.top_kth,
          que_id:this.que_id,
          threshold: this.threshold,
          layer: this.layer - 1,
          model:this.model
        })
        .then(() => {
          this.getAll();
        });
    },
    init() {
      console.log("tree init");
      console.log('model:',this.model)
      const path =
        "http://10.192.9.11:8000/query_attr_tree"
      axios
        .post(path, {
          top_kth:this.ctx_prop,
          que_id:this.queid_prop,
          threshold: this.threshold,
          layer: this.layer - 1,
          model:this.model_prop
        })
        .then(() => {
          axios
            .get(path)
            .then((res) => {
              var all_node_link = res.data.all_layer_node_link.map(
                (a) => a.node_link
              );
              this.sentence_span = res.data.sentence_span;
              this.drawAll(
                all_node_link,
                res.data.tokenPool,
                res.data.tree_height
              );
            })
            .then(() => {
              bus.$emit("init_tokens", this.valued_nodes);
            })
            .catch((error) => {
              console.error(error);
            });
        });
    },
  },
  beforeMount() {
    this.model = this.model_prop
    console.log('mount',this.model)
    this.init();
  },
};
</script>

<style scoped>
#attr-tree {
  margin: 0px;
  margin-left: 0px;
  height: 100%;
  text-align: center;
  width: 100%;

  /* overflow: auto; */
}
/* #AttrTreeSvg{
 border-radius: 10px;
position: relative;
margin: 10px;
  background-color: white;


} */
</style>

