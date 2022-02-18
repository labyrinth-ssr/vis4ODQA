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
  sankeyLeft as d3SankeyLeft,
} from "d3-sankey";
import bus from "./bus";

export default {
  name: "AttrTree",
  created() {
    //为什么是在created中监听？
    bus.$on("dispatchsentencetoshow", (val) => {
      this.tokens = val[0];
      var temp = [];
      val[0].forEach(function (token, index) {
        temp.push({ node: `${index}`, name: token });
      });
      this.nodes = temp;
      this.sentence_selected = val[1];

      this.init();
    }),
      bus.$on("dispatchthreshold", (val) => {
        this.threshold = val;

        this.set_para(this.threshold, this.layer);
      }),
      bus.$on("set_layer", (val) => {
        this.layer = val;
        this.set_para(this.threshold, this.layer);
      });
  },
  data() {
    return {
      data: [],
      sentence_selected: 1, //初始时自动选择第5句
      tokens: [],
      nodes: [],
      threshold: 0.4,
      layer: 10,
      valued_nodes: [],
      sentence_span: [],
    };
  },
  methods: {
    update() {
      this.getAll();
    },
    drawAll(sankeyDataList, tokenPool, tree_height) {
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
      d3.select("#AttrTreeSvg").remove();
      d3.select("#AttrTreeSvg").selectAll("*").remove();
      var margin = { top: 20, right: 10, bottom: 50, left: 10 },
        width = 1000,
        height = 400;
      var color = d3.scaleOrdinal(d3.schemePaired);

      const textData_index = tokenPool.map((a) => a + "");
      // Object.keys(textData);
      const layer_width = 35;

      const x = d3
        .scaleBand()
        .domain(textData_index)
        .range([0, height])
        .padding(0);
      var svg = d3
        .select("#attr-tree")
        .append("svg")
        .attr("id", "AttrTreeSvg")
        .attr("width", "1200")
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
      // const layerid_to_color=
      for (let i = 0; i < 12; i++) {
        g2.append("rect")
          .attr("width", "10")
          .attr("x", i * 10 + 60)
          .attr("height", "10")
          .attr("fill", d3.interpolateOrRd((i / 11) * 0.7 + 0.1))
          .attr("opacity", "1");
        //         .on('click',function(d){
        //     console.log('over');
        //     console.log(this.opacity);filter
        // })
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
        //         .on('click',function(d){
        //     console.log('over');
        //     console.log(this.opacity);filter
        // })
        g3.append("text")
          .text(`${i}`)
          .attr("x", i * 10 + 60)
          .attr("y", 20)
          .attr("font-size", "12px")
          .attr("fill", "black");
      }
      // this.draw(sankeyDataList[0],x,color,0,height,svg,margin)
      // this.draw(sankeyDataList[5],x,color,5,height,svg,margin)
      // this.draw(sankeyDataList[11],x,color,11,height,svg,margin)
      var pos = 0;
      for (let index = 0; index < 12; index++) {
        width = tree_height[index] * layer_width;
        this.draw(
          sankeyDataList[index],
          x,
          color,
          index,
          height,
          svg,
          margin,
          width,
          pos
        );
        pos = pos + width + 10;
      }
    },
    draw(sankeydata, x, color, index, height, svg, margin, width, pos) {
      // const la
      //sankeydata:node,link
      console.log(sankeydata);
      //calculate the tree height
      var links_data = sankeydata.links;
      links_data.sort(function (a, b) {
        return a.layer - b.layer;
      });
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
      const sankeyWidth = width,
        snakeyHeight = height;
      // console.log(sankeyWidth)
      // console.log(width)
      // Object.keys(textData);

      // append the svg object to the body of the page
      // var svg = d3
      //   .select("#attr-tree")
      //   .append("svg")
      //   .attr("id", "AttrTreeSvg")
      //   .attr("width", width + margin.left + margin.right)
      //   .attr("height", height + margin.top + margin.bottom)
      //   .style("background-color", "white")
      //   .style("border-radius", "10px")
      // const fixgWidth=50

      var mySvg = svg
        .append("g")
        .attr("id", "g-sankey-scale")
        .attr(
          "transform",
          " translate(" + (margin.left + pos) + "," + margin.top + ") "
        );
      // console.log(mySvg)

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
        link.y0 =
          link.source.y0 +
          (1 / 2) *
            Math.max(1, link.source.targetLinks.length) *
            x.bandwidth() +
          5;
        link.y1 =
          link.target.y0 +
          (1 / 2) *
            Math.max(1, link.target.targetLinks.length) *
            x.bandwidth() +
          5;
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
          console.log(d.layer + "");
          console.log(color(d.layer + ""));
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
        return d.source.name + " → " + d.target.name;
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
      console.log(graph);
      // add the rectangles for the graph
      node
        .append("circle")
        .attr("class", "nodeRect")
        .attr("cx", function (d) {
          return d.x0 + sankey.nodeWidth() / 2;
        })
        .attr("cy", function (d) {
          // console.log((d.y0+d.y1)/2)
          // console.log(d.y0 +
          //     (1 / 2) * Math.max(1, d.targetLinks.length) * x.bandwidth() +
          //     5)
          return (
            d.y0 +
            (1 / 2) * Math.max(1, d.targetLinks.length) * x.bandwidth() +
            5
          );
        })
        .attr("r", function (d) {
          return Math.max(0, d.saliency) * 30 + 5;
        })
        .on("click", function (event, data) {
          bus.$emit("dispatchtokentoshow", data.index);
        })
        .on("mouseover", function (event, data) {
          bus.$emit("highlightToken", data.index);
        })
        .on("mouseleave", function (e, data) {
          bus.$emit("unhighlight", data.index);
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
          return d.name;
        });
      //   d3.selectAll('.nodeRect').append('g')
      // .data(d3.select(this.parentNode).datum())
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
            (d.y0 +
              (1 / 2) * Math.max(1, d.targetLinks.length) * x.bandwidth() +
              5 -
              (Math.max(0, d.saliency) * 30 + 5)) +
            ") "
          );
        })
        .attr("text-anchor", "middle");

      // d3.select("#AttrTreeSvg").attr(
      //   "height",
      //   document.getElementById("g-sankey-scale").getBBox().height + margin.top
      // );
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
    // getAll() {
    //   const path =
    //     "http://10.192.9.11:5000/query_attr_tree/" + this.sentence_selected
    //   axios
    //     .get(path)
    //     .then((res) => {
    //       var nodeLinkData = res.data.node_link;
    //       var tokens = res.data.tokens;
    //       // if (this.tokens.length != 0) {
    //       //   tokens = this.tokens;
    //       // }
    //       var nodesData = nodeLinkData.nodes; //未选过sentence，直接获得？？？
    //       // if (this.nodes.length != 0) {
    //       //   //普通情况：nodes在选sentence时被存了
    //       //   nodesData = this.nodes;
    //       // }
    //       this.draw(nodeLinkData, tokens, nodesData);
    //     })
    //     .catch((error) => {
    //       // eslint-disable-next-line
    //       console.error(error);
    //     });
    // },
    set_para(threshold, layer) {
      const path =
        "http://10.192.9.11:5000/query_attr_tree/" + this.sentence_selected;
      axios
        .post(path, {
          sts_id: this.sentence_selected,
          threshold: threshold,
          layer: layer - 1,
        })
        .then(() => {
          this.getAll();
        });
    },
    init() {
      console.log("tree init");
      const path =
        "http://10.222.144.246:5000/query_attr_tree/" + this.sentence_selected;
      axios
        .post(path, {
          sts_id: this.sentence_selected,
          threshold: this.threshold,
          layer: this.layer - 1,
        })
        .then(() => {
          axios
            .get(path)
            .then((res) => {
              console.log(res.data);
              // var nodeLinkData = res.data.node_link;
              // var tokens = res.data.tokens;
              // // if (this.tokens.length != 0) {
              // //   tokens = this.tokens;
              // // }
              // var nodesData = nodeLinkData.nodes; //未选过sentence，直接获得？？？
              // // if (this.nodes.length != 0) {
              // //   //普通情况：nodes在选sentence时被存了
              // //   nodesData = this.nodes;
              // // }
              // tokens=[],nodesData=[]
              // res.data.valued_nodes.forEach((ele)=>{
              //   tokens.push(res.data.tokens[ele])
              //   nodesData.push(nodeLinkData.nodes[ele])
              // })
              // // nodeLinkData.nodes=nodesData
              // // nodesData=res.data.node_link.nodes
              var all_node_link = res.data.all_layer_node_link.map(
                (a) => a.node_link
              );
              this.sentence_span = res.data.sentence_span;
              this.drawAll(
                all_node_link,
                res.data.tokenPool,
                res.data.tree_height
              );
              // this.draw({'links':res.data.node_link.links,'nodes':nodesData}, tokens, nodeLinkData.nodes);
            })
            .then(() => {
              bus.$emit("init_tokens", this.valued_nodes);
              console.log("init tokens");
              console.log(this.valued_nodes);
            })
            .catch((error) => {
              // eslint-disable-next-line
              console.error(error);
            });
        });
    },
  },
  beforeMounted() {
    this.init();
    // console.log("tree init");
    // this.set_para(this.threshold,this.layer)

    // this.getAll()
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

