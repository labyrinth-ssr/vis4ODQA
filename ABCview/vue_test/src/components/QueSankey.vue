<template>
  <div id="que_sankey" class="view">
    <h2>Summary View</h2>
    <svg id="queSankeySvg"/>
    <a-select default-value="que" style="width: 120px" @change="handleChange">
      <a-select-option value="que"> question </a-select-option>
      <a-select-option value="ctx"> context </a-select-option>
      <a-select-option value="reranker"> reranker </a-select-option>
      <a-select-option value="reader"> reader </a-select-option>
    </a-select>
  </div>
</template>

<script>
const sankey_path = "http://10.192.9.11:8000/query_que_sunburst";
const sum_path = "http://10.192.9.11:8000/query_attn_head";
const bar_path = "http://10.192.9.11:8000/query_em_accu";
import * as d3 from "d3";
import axios from "axios";
import {
  sankey as d3Sankey,
  sankeyLinkHorizontal as d3SankeyLinkHorizontal,
  sankeyLeft as d3SankeyLeft,
} from "d3-sankey";
import bus from "./bus";

export default {
  name: "QueSankey",
  created() {
    // bus.$on('change_model',(val)=>{
    //   this.model = val;
    //   this.init();
    // })
  },
  data() {
    return {
      node_link: {},
      threshold: 100,
      head: 0,
      layer: 0,
      attn: {},
      accu_em: {},
      model: "single",
    };
  },
  methods: {
    handleChange(value) {
      this.model = value;
      this.update_head();
    },
    // update() {

    // },
    draw() {
      d3.select("#queSankeySvg").selectAll("*").remove();
      var sankeydata = this.node_link;
      //sankeydata)
      var attndata = this.attn;
      var accu_em_data = this.accu_em.accu_em;
      const em_avg = this.accu_em.em_avg;
      const accu_avg = this.accu_em.k_accu_avg;
      //accu_em_data)
      const margin = { top: 10, right: 15, bottom: 10, left: 15 };
      const svg_size = { width: 450, height: 275 };
      const sankey_size = {
        width: 80,
        height: 450 - margin.left - margin.right,
      };
      // const attn_size = { width: 15, height: 15 };

      var svg = d3
        .select("#queSankeySvg")
        // .append("svg")
        // .attr("id", "queSankeySvg")
        .attr("width", svg_size.width)
        .attr("height", svg_size.height)
        .append("g")
        .attr(
          "transform",
          "translate(" +
            (margin.left + sankey_size.height) +
            "," +
            margin.top +
            ")rotate(90)"
        );

      const sankey_nodewidth = 10;
      const node_color = [
        "#8F6FAE",
        "#F38E1A",
        "#DF5E4C",
        "#46A7E4",
        "#F9B700",
      ];
      const link_color = [
        "#DBCCE9",
        "#F8CB9D",
        "#F1D0D0",
        "#8ECEE9",
        "#F3D790",
      ];
      const color = node_color.map((val, key) => [val, link_color[key]]);
      const color_scl = d3.scaleOrdinal(color);
      var sankey = d3Sankey()
        .nodeWidth(sankey_nodewidth)
        .nodePadding(6)
        .size([sankey_size.width, sankey_size.height])
        .nodeId(function id(d) {
          return d.node;
        })
        .nodeAlign(d3SankeyLeft)
        .nodeSort(null);
      var graph = sankey(sankeydata);
      // //graph);
      /* var link =  */ svg
        .append("g")
        .selectAll(".link")
        .data(graph.links)
        .enter()
        .append("path")
        .attr("id", (d) => "link" + d.index)
        .attr("class", "link")
        .attr("d", d3SankeyLinkHorizontal())
        .attr("fill", "none")
        .attr("stroke", function (d) {
          return (d.color = color_scl(d.source.name)[1]);
        })
        .style("opacity", 0.5)
        .style("stroke-width", (d) => d.width)
        .on("mouseover", function () {
          d3.select(this).style("opacity", 1);
        })
        .on("mouseleave", function () {
          d3.select(this).style("opacity", 0.5);
        })
        .on("click", (e, d) => {
          bus.$emit("dispatchSenIds", d.senIds);
          //d)
        })
        .append("title")
        .text(function (d) {
          return d.source.name + "->" + d.target.name+'\n'+d.value;
        });
      //link);

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
          return (d.color = color_scl(d.name)[0]);
        })
        .style("stroke", "none")
        .style("opacity", 1)
        .append("title")
        .text((d) => {
          return d.name;
        });

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

      // svg.attr("transform", "translate(400,10)rotate(90)");

      const sankey_matrix_gap = 30;

      const attn_color = d3
        .scaleSequential()
        .interpolator(d3.interpolateGnBu)
        .domain([0, 2.54]);
      var links_data = sankeydata.links;
      sankeydata.links.sort((a, b) => {
        return a.y1 - b.y1;
      });
      const rect_padding = 5;
      const rect_height = 6;
      const rect_width = sankey_size.height / links_data.length - rect_padding;
      links_data.forEach((ele, index) => {
        ele.index = index;
      });
      console.log(links_data);
      const barchart_padding = 15;

      var attn_g = d3
        .select("#queSankeySvg")
        .append("g")
        .attr("id", "attn_g")
        .attr(
          "transform",
          "translate(" +
            /* margin.left */ 0 +
            "," +
            (margin.top +
              sankey_size.width +
              rect_padding +
              sankey_matrix_gap +
              barchart_padding) +
            ")"
        );

      // 确定col的横坐标：绑定所有attndata数据后，将根据每条attn，选出匹配link的index
      //取出所有的y1排序后将index存入links
      var attn = attn_g
        .append("g")
        .selectAll(".attn_col")
        .data(attndata)
        .enter()
        .append("g")
        .attr("transform", (d) => {
          const link_data = sankeydata.links;
          const link_index = link_data.filter(
            (link) =>
              link.source.name == d.source && link.target.name == d.target
          )[0].index;
          d.link_index = link_index;
          return (
            "translate(" +
            (sankey_size.height - link_index * (rect_width + rect_padding)) +
            ",0)"
          );
        })
        .attr("class", "attn_col");
      //attndata)
      attndata.sort((a, b) => {
        return a.link_index - b.link_index;
      });
      // 对应的数据，已经列出，需要匹配，按照senid匹配？，按照source和target匹配。

      attn
        .append("g")
        .selectAll(".layer_attn")
        .data((d) => {
          const link_data = sankeydata.links;
          const width = link_data.filter(
            (link) =>
              link.source.name == d.source && link.target.name == d.target
          )[0].width;
          d.layer_impo.forEach((ele) => {
            ele["width"] = width;
          });
          return d.layer_impo;
        })
        .enter()
        .append("g")
        .attr("class", "layer_attn");

      d3.selectAll(".layer_attn")
        .append("rect")
        .attr("y", (d) => {
          return d.layer * (rect_height + rect_padding);
        })
        .attr("width", rect_width)
        .attr("height", rect_height)
        .attr("fill", (d) => attn_color(d.val))
        .append("title")
        .text((d) => 'layer attr:\n'+d.val.toFixed(3));
      // var queSankeySvg=

      d3.select("#queSankeySvg")
        .append("defs")
        .append("pattern")
        .attr("id", "diagonalHatch")
        .attr("patternUnits", "userSpaceOnUse")
        .attr("width", 4)
        .attr("height", 4)
        .append("path")
        .attr("d", "M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2")
        .attr("stroke", "#EFE5AE")
        .attr("stroke-width", 1);

      d3.select("#queSankeySvg")
        .append("defs")
        .append("pattern")
        .attr("id", "diagonalHatch2")
        .attr("patternUnits", "userSpaceOnUse")
        .attr("width", 4)
        .attr("height", 4)
        .append("path")
        .attr("d", "M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2")
        .attr("stroke", "#BBCCDD")
        .attr("stroke-width", 1);

      // 首先将每个g移动到对应的横坐标，然后根据值开始画
      // 横坐标的值来自link的y1，具体
      // [0,1]=>[0,30]
      //使用最大值作为
      //使用同一个轴
      const max_em = d3.max(accu_em_data.map((ele) => ele.em));

      const max_accu = d3.max(accu_em_data.map((ele) => ele.accu));
      // const scale_max=d3.max([max_em,max_accu])
      const a_scale = d3
        .scaleLinear()
        .domain([0, max_accu])
        .range([0, sankey_matrix_gap]);
      const e_scale = d3
        .scaleLinear()
        .domain([0, max_em])
        .range([0, sankey_matrix_gap]);
      const bar_width = 8;
      var accu_em_g = d3
        .select("#queSankeySvg")
        .append("g")
        .attr("id", "ae_g")
        .attr(
          "transform",
          "translate(" +
            /* margin.left-bias */ 0 +
            "," +
            (margin.top + sankey_size.width + barchart_padding) +
            ")"
        );
      //sankeydata)
      console.log(accu_em_data);
      /* var accu_em= */ accu_em_g
        .append("g")
        .selectAll(".que_ae")
        .data(accu_em_data)
        .enter()
        .append("g")
        .attr("transform", (d) => {
          const link_data = sankeydata.links;

          d.id= link_data.filter(
            (link) =>
              link.source.node == d.source && link.target.node == d.target
          )[0].index;
          return (
            "translate(" +
            (sankey_size.height - d.id * (rect_width + rect_padding)) +
            ",0)"
          );
        })
        .attr("class", "que_ae")
        .classed("over_avg", (d) => (d.accu > accu_avg ? true : false))
        .classed("over_e_avg", (d) => (d.em > em_avg ? true : false));

      //accu_em)

      //有没有办法合成一块写,我希望，将他们作为一个整体，但是
      //重构：作为同一个rec的情况，第一个长方形高度是avg与自长更小的高度，填充颜色，第二个长方形高度是avg与自长更高的高度，若未前者则无填充，若为后者则
      //给出index时，需要变化的主要是填充物
      var accu_avg_rec = d3
        .selectAll(".que_ae")
        .append("rect")
        .attr("width", bar_width)
        .attr("height", a_scale(accu_avg))
        .attr("fill", (d) => {
          return d.accu < accu_avg ? "none" : "#EFE5AE";
        })
        .attr("stroke", "#EFE5AE")
        .attr("id", (d) => (d.accu < accu_avg ? "" : "rect" + d.id));

      accu_avg_rec
        .append("title")
        .text((d) => 'topk accu:\n'+d.accu.toFixed(3))
        .append("g");

      accu_avg_rec
        .on("mouseover", function (e, d) {
          if (d.accu >= accu_avg) {
            d3.select(this).style("fill-opacity", 0.8);
          }
          d3.select("#link" + d.id).style("opacity", 0.8);
        })
        .on("mouseleave", function (e, d) {
          if (d.accu >= accu_avg) {
            d3.select(this).style("fill-opacity", 1);
          }
          d3.select("#link" + d.id).style("opacity", 0.5);
        });

      var accu_rec = d3
        .selectAll(".que_ae")
        .append("rect")
        .attr("width", bar_width)
        .attr("height", (d) => a_scale(d.accu))
        .attr("fill", (d) => {
          return d.accu < accu_avg ? "#EFE5AE" : "url(#diagonalHatch)";
        })
        .attr("stroke", (d) => {
          return d.accu < accu_avg ? "#EFE5AE" : "none";
        });

      accu_rec.append("title").text((d) => 'topk accu:\n'+d.accu.toFixed(3));

      accu_rec
        .on("mouseover", function (e, d) {
          if (d.accu < accu_avg) {
            d3.select(this).style("fill-opacity", 0.8);
          }
          d3.select("#link" + d.id).style("opacity", 0.8);
        })
        .on("mouseleave", function (e, d) {
          if (d.accu < accu_avg) {
            d3.select(this).style("fill-opacity", 1);
          }
          d3.select("#link" + d.id).style("opacity", 0.5);
        });

      d3.selectAll(".que_ae")
        .append("rect")
        .attr("x", bar_width)
        .attr("width", bar_width)
        .attr("height", e_scale(em_avg))
        .attr("fill", (d) => {
          return d.em < em_avg ? "none" : "#BBCCDD";
        })
        .attr("stroke", "#BBCCDD")
        .on("mouseover", function (e, d) {
          if (d.em >= em_avg) {
            d3.select(this).style("fill-opacity", 0.8);
          }
          d3.select("#link" + d.id).style("opacity", 0.8);
        })
        .on("mouseleave", function (e, d) {
          if (d.em >= em_avg) {
            d3.select(this).style("fill-opacity", 1);
          }
          d3.select("#link" + d.id).style("opacity", 0.5);
        })
        .append("title")
        .text((d) => 'em:\n'+d.em.toFixed(3))
        .append("g");

      d3.selectAll(".que_ae")
        .append("rect")
        .attr("x", bar_width)
        .attr("width", bar_width)
        .attr("height", (d) => e_scale(d.em))
        .attr("fill", (d) => {
          return d.em < em_avg ? "#BBCCDD" : "url(#diagonalHatch2)";
        })
        .attr("stroke", (d) => {
          return d.em < em_avg ? "#BBCCDD" : "none";
        })
        .on("mouseover", function (e, d) {
          if (d.em < em_avg) {
            d3.select(this).style("fill-opacity", 0.8);
          }
          d3.select("#link" + d.id).style("opacity", 0.8);
        })
        .on("mouseleave", function (e, d) {
          if (d.em < em_avg) {
            d3.select(this).style("fill-opacity", 1);
          }
          d3.select("#link" + d.id).style("opacity", 0.5);
        })
        .append("title")
        .text((d) => 'em:\n'+d.em.toFixed(3));

      //Link generator used for both examples
      var linkGen = d3
        .linkVertical()
        .source((d) =>
          saneky_revert_scale(
            sankey_size.width + sankey_nodewidth * 0.5,
            d.y1 /* +0.5*d.width */
          )
        )
        .target((d) =>
          matrix_revert_scale(
            sankey_size.height - d.index * (rect_width + rect_padding),
            0
          )
        );

      const saneky_revert_scale = (x, y) => {
        return [sankey_size.height - y-margin.left+3, x+6];
      };
      const matrix_revert_scale = (x, y) => {
        return [
          x - 0.5 * rect_width-margin.left+6,
          margin.top + sankey_size.width + barchart_padding + y,
        ];
      };
      d3.select("#queSankeySvg")
        .append("g")
        .attr("transform", "translate(" + (margin.left + 12) + ",0)")
        .selectAll(".sim_link")
        .data(sankeydata.links)
        .join("path")
        .attr("d", linkGen)
        .attr("stroke", "#D3D3D3")
        .attr("stroke-width", 1)
        .attr("fill", "none")
        .classed("sim_link", true);
      // draw_attn(){
    },
    init() {

      const requestOne = axios.get(sankey_path);
      const requestTwo = axios.get(sum_path);
      const requestThree = axios.get(bar_path);
      axios
        .all([
          axios
            .post(sankey_path, {
              threshold: this.threshold,
              head: this.head,
              layer: this.layer,
            })
            .then(console.log('sankey posted')),
          axios
            .post(sum_path, {
              model: this.model,
            })
            .then(console.log('head posted')),
        ])
        .then(() => {
          console.log('all posted')
          

          axios.all([requestOne, requestTwo, requestThree]).then(


            axios.spread((sankey,sum,barchart) => {
              console.log('get all')
              console.log({sankey,sum,barchart})
              this.node_link = sankey.data;
              this.attn = sum.data;
              this.accu_em = barchart.data;
              console.log(this.node_link)
              console.log(this.attn)
              this.draw();
            })
          );
          // .catch((error) => {
          //   console.error(error);
          // });
        });
      // .catch((error) => {
      //   console.error(error);
      // });
    },
    update_head(){
      axios.post(sum_path,{
        model: this.model,
      })
      .then(() => {
        console.log('model change,sum posted')
        axios.get(sum_path)
        .then((resp)=>{
          this.attn=resp.data
          this.draw()
        })
      })
    }
  },
  mounted() {
    this.init();
  },
};
</script>

<style >
.over_avg {
  /* height: 10px; */
  background: linear-gradient(
    45deg,
    rgba(0, 153, 68, 0.5) 0,
    rgba(0, 153, 68, 0.5) 25%,
    transparent 25%,
    transparent 50%,
    rgba(0, 153, 68, 0.5) 50%,
    rgba(0, 153, 68, 0.5) 75%,
    transparent 75%,
    transparent
  );
  background-size: 5px 5px;
}

.ant-pagination.mini .ant-pagination-jump-prev, .ant-pagination.mini .ant-pagination-jump-next {
    height: 10px;
    }
    .ant-pagination.mini .ant-pagination-item {
    min-width: 5px;
    height: 5px;
    margin: 0;
    line-height: 5px;
}
.ant-pagination.mini .ant-pagination-prev, .ant-pagination.mini .ant-pagination-next {
    min-width: 5px;
    height: 5px;
    margin: 0;
    line-height: 5px;
}
</style>

