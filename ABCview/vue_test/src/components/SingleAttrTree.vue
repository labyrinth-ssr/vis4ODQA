<template>
  <div id="single-attr-tree"></div>
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
  name: "SingleAttrTree",
  created() {
      bus.$on("que_thre", (val) => {
        this.threshold.que=val
        this.set_para_update();
      }),
      bus.$on("ctx_thre", (val) => {
        this.threshold.ctx=val
        this.set_para_update();
      }),
      bus.$on("reranker_thre", (val) => {
        this.threshold.reranker=val
        this.set_para_update();
      }),
      bus.$on("reader_thre", (val) => {
        this.threshold.reader=val
        this.set_para_update();
      }),
      bus.$on("set_layer", (val) => {
        this.layer = val;
        this.set_para_update();
      });
      bus.$on("update_ctx", (val) => {
        this.ctx_selected = val;
        this.set_para_update();
      });
      bus.$on("dispatchqueid", (val) => {
        this.question_id = val;
        this.ctx_selected=0
        this.set_para_update();
      });
  },
  data() {
    return {
    //   data: [],
      ctx_selected: 0,
    //   tokens: [],
    //   nodes: [],
      threshold:{
        que:0.5,
        ctx:0.5,
        reranker:0.7,
        reader:0.5
      },
      layer: 12,
      q_node_link:{},
      ctx_node_link:{},
      reranker_node_link:{},
      reader_node_link:{},
      tokenPool:[],
      sentence_span: [],
      tree_height:{},
      question_id:1
    };
  },
  methods: {
    drawAll(/* sankeyDataList, tokenPool, tree_height */) {
      const sentence_span = this.sentence_span;
            d3.select("#AttrTreeSvg").remove();
      d3.select("#AttrTreeSvg").selectAll("*").remove();

      const sentence_color = function (i) {
        if (i == 1) {
          return 7;
        } else if (i == 2) {
          return 8;
        } else if (i == 5) {
          return 9;
        }
        return i;
      };
    //   d3.select("#AttrTreeSvg").remove();
    //   d3.select("#AttrTreeSvg").selectAll("*").remove();
      const margin = { top: 50, right: 10, bottom: 50, left: 50 },
        // width = 1000,
        height = 240;
      // var color = d3.scaleOrdinal(d3.schemePaired);

      const textData_index = this.tokenPool.map((a) => a + "");
      // Object.keys(textData);

      const x = d3
        .scaleBand()
        .domain(textData_index)
        .range([0, height])
        .padding(0);
      const svg_width=700;
      var svg = d3
        .select("#single-attr-tree")
        .append("svg")
        .attr("id", "AttrTreeSvg")
        .attr("width", "700")
        .attr("height", height + margin.top + margin.bottom)
        .style("background-color", "white")
        .style("border-radius", "10px");

      const g2 = svg
        .append("g")
        .attr("id", "colourScale")
        .attr(
          "transform",
          "translate(" + margin.left + "," + (height + margin.top) + ")"
        );
      g2.append("text").attr("y", 10).text("layer").attr("fill", "black");
      for (let i = 0; i < 12; i++) {
        g2.append("rect")
          .attr("width", "10")
          .attr("x", i * 10 + 60)
          .attr("height", "10")
          .attr("fill", d3.interpolateOrRd((i / 11) * 0.7 + 0.1))
          .attr("opacity", "1");
        g2.append("text")
          .text(`${i}`)
          .attr("x", i * 10 + 60)
          .attr("y", 20)
          .attr("font-size", "12px")
          .attr("fill", "black");
      }
      const g3 = svg
        .append("g")
        .attr("id", "colourScale")
        .attr(
          "transform",
          "translate(" + margin.left + "," + (height + margin.top + 30) + ")"
        );
      g3.append("text").attr("y", 10).text("sentence").attr("fill", "black");
      for (let i = 0; i < 7; i++) {
        g3.append("rect")
          .attr("width", "10")
          .attr("x", i * 10 + 60)
          .attr("height", "10")
          .attr("fill", d3.schemeTableau10[sentence_color(i)])
          .attr("opacity", "1");
        g3.append("text")
          .text(`${i}`)
          .attr("x", i * 10 + 60)
          .attr("y", 20)
          .attr("font-size", "12px")
          .attr("fill", "black");
      }

        function draw(sankeydata,start_x,width) {
          console.log(sankeydata)
                  // var links_data = sankeydata.links;
      // links_data.sort(function (a, b) {
      //   return a.layer - b.layer;
      // });
      var mySvg = svg
        .append("g")
        .attr("id", "g-sankey-scale")
        .attr(
          "transform",
          " translate(" + (margin.left + start_x) + "," + margin.top + ") "
        );

      // Set the sankey diagram properties
      var sankey = d3Sankey()
        .nodeWidth(5)
        .nodePadding(0) //最好换成一个函数
        .size([width, height])
        .nodeId(function id(d) {
          return d.node;
        })
        // .nodeSort(function (a, b) {
        //   return a.node - b.node;
        // })
        .nodeAlign(d3SankeyLeft)
        // .nodes(sankeydata.nodes);

      var graph = sankey(sankeydata);
      console.log(graph)

      graph.nodes.forEach((node) => {
        var newY = x(node.node);
        var yGAp = x.bandwidth();
        node.y0 = newY;
        node.y1 = newY + yGAp;
      });

      // sankey.update(graph);
      graph.links.forEach((link) => {
        link.width = x.bandwidth();
        link.y0 =
          link.source.y0 
        link.y1 =
          link.target.y0 
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
        .style("opacity", 0.8)
        .style("stroke-width", function (d) {
          return d.value * 20 - 7;
        })
        .on("mouseover", function () {
          d3.select(this).style("opacity", 1);
        })
        .on("mouseleave", function () {
          d3.select(this).style("opacity", 0.8);
        });

      // add the link titles
      link.append("title").text(function (d) {
        return d.source.name + " → " + d.target.name+'\nlayer:'+d.layer;
      });
      // add in the graph
      var node = mySvg
        .append("g")
        .selectAll(".node")
        .data(graph.nodes)
        .enter()
        .append("g")
        .attr("class", "node");

      node
        .append("circle")
        .attr("class", "nodeRect")
        .attr("cx", function (d) {
          return d.x0 + sankey.nodeWidth() / 2;
        })
        .attr("cy", function (d) {
          return (
            d.y0 
          );
        })
        .attr("r", function (d) {
          return Math.max(0, d.saliency) * 30 + 5;
        })
        .style("fill", function (d) {
          if (d.targetLinks.length + d.sourceLinks.length === 0) {
            return "none";
          }
          return (d.color =
            d3.schemeTableau10[sentence_color(sentence_span[d.node])]);
        })
        .style("stroke", "none")
        .style("opacity", 1)
        .append("title")
        .text(function (d) {
          return d.name+'\nsentence:'+sentence_span[d.node];
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
            (d.y0 
              -
              (Math.max(0, d.saliency) * 30 + 5)) +
            ") "
          );
        })
        .attr("text-anchor", "middle");

      d3.select("#AttrTreeSvg")
        .style("background-color", "white")
        .style("border-radius", "10px")
        .style("margin", "10px")
        .style("margin-left", "0px");

        }
    const tree_padding=40;
      // const layer_width = 60;
      const tree_height_sum=this.tree_height.q+this.tree_height.ctx+d3.max([this.tree_height.q,this.tree_height.ctx])+d3.max([this.tree_height.q,this.tree_height.ctx]);
      const layer_width = (( svg_width-margin.right-margin.right)+tree_padding-(2*tree_padding))/tree_height_sum;


        draw(this.q_node_link,0,this.tree_height.q*layer_width)
        draw(this.ctx_node_link,0,this.tree_height.ctx*layer_width)
        draw(this.reranker_node_link,layer_width*d3.max([this.tree_height.q,this.tree_height.ctx])+tree_padding,
        this.tree_height.reranker*layer_width)
        draw(this.reader_node_link,layer_width*d3.max([this.tree_height.q,this.tree_height.ctx])+tree_padding*2+layer_width*this.tree_height.reranker,
        this.tree_height.reader*layer_width)
    },

    getAll() {
      const path =
        "http://10.192.9.11:8000/query_single_attr_tree/" + this.ctx_selected
      axios
        .get(path)
        .then((res) => {
              this.set_data(res)
              this.drawAll();

        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    set_para_update() {
      const path =
        "http://10.192.9.11:8000/query_single_attr_tree/" + this.ctx_selected;
      axios
        .post(path, {
          threshold: this.threshold,
          layer: this.layer - 1,
          queId:this.question_id
        })
        .then(() => {
          this.getAll();
        });
    },
    set_data(res){
              this.q_node_link=res.data.q_node_link
              this.ctx_node_link=res.data.ctx_node_link
              this.reranker_node_link=res.data.reranker_node_link
              this.reader_node_link=res.data.reader_node_link
              this.tree_height=res.data.tree_height
              this.sentence_span = res.data.sentence_span;
              this.tokenPool=res.data.token_pool
    },
    init() {
      console.log("tree init");
      const path =
        "http://10.192.9.11:8000/query_single_attr_tree/" + this.ctx_selected;
      axios
        .post(path, {
          threshold: this.threshold,
          layer: this.layer - 1,
          queId:this.question_id
        })
        .then(() => {
          axios
            .get(path)
            .then((res) => {
              this.set_data(res)
              this.drawAll(
              );
            })
            .catch((error) => {
              console.error(error);
            });
        });
    },
  },
  beforeMount() {
    this.init();
  },
};
</script>

<style scoped>
#single-attr-tree {
  margin: 0px;
  margin-left: 0px;
  height: 100%;
  text-align: center;
  width: 100%;
}

</style>

