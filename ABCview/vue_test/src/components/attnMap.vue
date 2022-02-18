<template>
  <div id="attnMap"></div>
</template>
<script>
//实现一键取消
import * as d3 from "d3";
import axios from "axios";
import bus from "./bus";

export default {
  name: "attnMap",
  created() {
    bus.$on("dispatchtokentoshow", (val) => {//监听到选择时,,,
    // console.log(this.token_selected)
      if (this.token_selected.indexOf(val) >= 0) {//
        this.token_selected.splice(this.token_selected.indexOf(val), 1);
      }
      else {this.token_selected.push(val);}
      this.draw(this,this.singleAttn, this.tokens);
    });
    
    bus.$on("dispatchsentencetoshow", (val) => {
      // this.tokens = val[0];
      this.sentence_selected = val[1];
      this.token_selected=[];
      this.getAll(this);//后台读取
    });
    bus.$on("dispatchheadtoshow", (val) => {
      this.layer = val[0];
      this.head = val[1];
      var temp = this.all_attn.filter(
        (ele) => ele.layer === this.layer && ele.head === this.head
      );
      this.singleAttn = temp[0].attn;
      this.draw(this,this.singleAttn, this.tokens);
    });
    
    bus.$on('reset_tokens',()=>{
      this.token_selected=[];
      this.draw(this,this.singleAttn, this.tokens);
    })
    // ,
    bus.$on('init_tokens',valued_nodes_group=>{
      // console.log('attn map get tkens init',valued_nodes_group)
      valued_nodes_group.forEach((node)=>{
        if (this.token_selected.indexOf(node) >= 0) {//
        this.token_selected.splice(this.token_selected.indexOf(node), 1);
      }
      else {this.token_selected.push(node);}
      })
      this.getAll(this)
      // console.log(this.token_selected)
      
      // console.log('init tokens in attnmap',this.token_selected,this.singleAttn,this.tokens)
      // this.draw(this.singleAttn, this.tokens);
      // console.log('after draw',this.token_selected)
    })
    
  },
  data() {
    return {
      all_attn: [],
      sentence_selected: 4, //初始时自动选择第5句
      layer: 0,
      head: 0,
      token_selected: [], //被选中的token的index，用于过滤（注意是index（int)而不是token(str)，以防多个词反复出现时选取错误）
      tokens: [],
      singleAttn: [],
    };
  },
  // watch:{
  //   token_selected(val){
  //     this.getAll(this);

  //   }

  // },
  methods: {
    draw(obj,req_data, tokens) {
      var tokenId=obj.token_selected;
      const max = d3.max(req_data,ele=>ele.val)
      const attrScale=d3
      .scaleLinear()
      .domain([0,max]) 
      .range([0, 1]) 
      
      const background_color = "steelblue";
      const lineColor = "red";

      d3.select("#attnMapSvg").remove();
      d3.select("#attnMapSvg").selectAll("*").remove();
      // set the dimensions and margins of the graph

      const margin = { top: 10, right: 0, bottom: 30, left: 50 },
        width =
          document.getElementById("attnMap").clientWidth -
          margin.left -
          margin.right,
        height =
          document.getElementById("attnMap").clientHeight -
          margin.top -
          margin.bottom;

      const svg=d3.select('#attnMap').append('svg')
      .attr('id','attnMapSvg')
      .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
         .style('background-color','white')
        .style("border-radius",'10px')
        .style("margin",'10px')
        .style('margin-right','0px')
        .append("g")
        .attr('id','svg-g')
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

      var line_data = req_data;

      const detailDomain = Object.keys(tokens);
      const detailScale = d3
        .scaleBand()
        .range([0, height])
        .domain(detailDomain)
        .padding(0);


      if (d3.select("#leftAxis")._groups[0][0] === null) {
        const tickData = Object.entries(tokens);

        svg
          .append("g")
          .style("font-size", 10)
          .attr("id", "leftAxis")
          .call(d3.axisLeft(detailScale).tickSize(0))
          .selectAll(".tick")
          .attr("class", "leftTick")
          .data(tickData)
          .select("text")
          .attr("class", "leftText")
          .text(function (d) {
            return d[1];
          })
          .style("opacity", 1);

        d3.select("#leftAxis")
          .selectAll(".tokenContainer")
          .data(tickData)
          .join("rect")
          .attr("class", "tokenContainer")
          .attr('id',function(d){
            return 'tokenContainer'+d[0]
          })
          .attr("x", -30)
          .attr("y", function (d) {
            return detailScale(d[0]);
          })
          .attr("width", 30)
          .attr("height", detailScale.bandwidth())
          .attr("fill", "blue")
          .style("opacity", 0.0)
          .on("mouseover", function (d, data) {
            d3.selectAll('.attn').style('opacity',0)
            stephighlight(data[0]);
          })
          .on("mouseleave", function () {
            unhighlightSelection();
          });

        svg
          .append("g")
          .style("font-size", 10)
          .attr("transform", "translate(" + (width - margin.right) + ",0)")
          .attr("id", "rightAxis")
          .call(d3.axisRight(detailScale).tickSize(0))
          .selectAll(".tick")
          .attr("class", "rightTick")
          .data(tickData)
          .select("text")
          .attr("class", "rightText")
          .attr("id", function (d) {
            return "rightText" + d[0];
          })
          .text(function (d) {
            return d[1];
          })
          .style("opacity", 0);

        d3.selectAll(".domain").remove();
      }

      svg
        .selectAll(".attn")
        .data(line_data)
        .join("line")
        .attr("class", function(d){
          return 'attn'+d.source+' attn';
        })
        .attr("x1", 5)
        .attr("y1", function (d) {
          return detailScale(`${d.source}`) + detailScale.bandwidth() / 2;
        })
        .attr("x2", width - margin.right)
        .attr("y2", function (d) {
          return detailScale(`${d.target}`) + detailScale.bandwidth() / 2;
        })
        .attr("stroke-width", 2.2)
        .attr("stroke", lineColor)
        .attr("stroke-opacity", function (d) {
          return attrScale(+d.val)
        });

      function stephighlight(index){//根据index高亮
        d3.select('#tokenContainer'+index)
        .attr("fill", background_color)
          .style("opacity", 0.3);

        d3.selectAll('.attn'+index).style('opacity',1)

      }

      if(obj.token_selected.length!==0){
      d3.selectAll('.attn').style('opacity',0)
      obj.token_selected.forEach(function (token) {
          stephighlight(token);
        });

          }
      

      function unhighlightSelection() {
             d3.selectAll(".tokenContainer").style("opacity", 0.0);
        if(tokenId.length!==0){
      d3.selectAll('.attn').style('opacity',0)
      tokenId.forEach(function (token) {
          stephighlight(token);
        });

          }
          else{
        d3.selectAll(".attn").style("opacity", 1);
          }
      }
    },

    getAll(obj) {
      let urls = [
         'http://10.192.9.11:5000/query_all',
        //  'http://10.192.9.11:5000/query_attr_tree/'+obj.sentence_selected,
         'http://10.192.9.11:5000/query_attn_map/'+ obj.sentence_selected
       ]
       let axiosList = []
       urls.forEach(url => {
         axiosList.push(axios.get(url))
       })
       axios.all(axiosList).then((res)=> {
            obj.tokens = res[0].data[obj.sentence_selected].tokens;
            // obj.token_selected= res[1].data.valued_nodes;
            obj.all_attn = res[1].data.detail;
            obj.singleAttn = obj.all_attn[obj.layer*12+obj.head].attn;
            // console.log('before map draw,valued',obj.token_selected)
          obj.draw(obj,obj.singleAttn, obj.tokens);
       })
       .catch((error) => {
          console.error(error);
        });
    }
  },
  
};
</script>

<style scoped>
#attnMap {
  margin: 10px;
  margin-right: 5px;
  position: relative;
  width: 0%;
  height: 100%;
}

</style>