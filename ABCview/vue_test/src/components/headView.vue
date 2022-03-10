<template>

<div id="attn-graph">
</div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import bus from './bus';

export default {
  name: "attn_graph",
  created(){
    bus.$on('dispatchQue',val=>{
      this.senIds=val
      this.update();
    })
  },
  data() {
    return {
      // background_color:'steelblue',
      // lineColor:'LightCoral',

      senIds:Array.from(new Array(3610).keys()),
      impo_data:[],
      attn_data:[],
      data: [],
    };
  },
  methods: {
    
    update(){
      
      this.getAll();
    },
    draw(myData) {
      d3.select('#attnSvg').remove()
      d3.select('#attnSvg')
        .selectAll('*')
        .remove();
      // set the dimensions and margins of the graph
      const margin = { top: 90, right: 30, bottom: 15, left: 40 },
        width = 730 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;
      // append the svg object to the body of the page
      const svg = d3
        .select("#attn-graph")
        .append("svg")
        .attr('id','attnSvg')
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

      // Build X scales and axis:
      const axisContent = Array.from(new Array(12).keys())
      const x = d3.scaleBand().range([height, 0]).domain(axisContent).padding(0.05);

      svg
        .append("g")
        .style("font-size", 10)
        .attr("transform", `translate(0, ${height})`)
        .attr("class", "xAxis")
        .call(d3.axisBottom(x).tickSize(0))
        .selectAll(".tick")
        .data(axisContent)
        .select("text")
        .text(function (d) {
          if(d==0){
            return 'head'+1
          }
          return d+1;
        });

      svg
        .append("g")
        .attr('class','yAxis')
        .style("font-size", 10)
        .call(d3.axisLeft(x).tickSize(0))
        .selectAll(".tick")
        .data(axisContent)
        .select("text")
        .text(function (d) {
          if(d==0){
            return 'layer'+1
          }
          return d+1;
        });

      d3.selectAll(".domain").remove();

      var valArr=[]
      myData.forEach(ele => {
        valArr.push(ele.val)
      });

      // Build color scale
      const myColor = d3
        .scaleSequential()
        .interpolator(d3.interpolateGnBu)
        .domain([0, d3.max(valArr)]);

      var mouseover=function(){
        d3.select(this)
        .style('stroke','black')
        .style('opacity',1)
      }

      var mouseleave = function(){
        if(d3.select(this).style('stroke')=='black'){
          d3.select(this)
        .style('stroke','none')
        .style('opacity',0.8)

        }
      }
      svg
        .selectAll('.impo_rect')
        .data(myData)
        .join('rect')
        .attr('class','impo_rect')
          .attr("x", function (d) {
            // console.log('layer '+d.layer+'head '+d.head+'impo '+d.val)
            return x(d.head);
          })
          .attr("y", function (d) {
            return x(d.layer);
          })
          .attr("rx", 4)
          .attr("ry", 4)
          .attr("width", x.bandwidth())
          .attr("height", x.bandwidth())
          .style("fill", function (d) {
            return myColor(d.val);
          })
          .style("stroke-width", 4)
          .style("stroke", "none")
          .style("opacity", 0.8)
        .on('mouseover',mouseover)
        .on('mouseleave',mouseleave)
        .on('click',function(e,d){
            d3.selectAll('.impo_rect').style('stroke','none')
            .style('opacity',0.8)

          d3.select(this)
        .style('stroke','blue')
        .style('opacity',1)

        bus.$emit('emitHeadLayer',{head:d.head,layer:d.layer})

        })
    },

    getAll(){
      const path='http:///10.223.164.171:5000/query_attn_head'
      axios.post(path,{senIds:this.senIds})
      .then(()=>{
        axios.get(path)
        .then((res) => {
          this.impo_data = res.data;
          this.draw(this.impo_data)
        }
        )
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      })
      .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  
  mounted() {
    this.getAll()
  },
};
</script>

<style scoped>
#attn-graph{
  margin-top:10px;
  margin-bottom: 10px;
  border-radius: 10px;
    background: white;
}
</style>
