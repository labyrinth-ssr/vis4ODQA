<template>

<div id="attn-graph">
</div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import bus from './bus';
// import func from 'vue-editor-bridge';

// import visData from '../../../data/attn_head.json'
//need:token,importance data

export default {
  name: "attn_graph",
  created(){
    bus.$on('dispatchsentencetoshow',val=>{
      this.tokens=val[0]
      this.sentence_selected = val[1];
      this.update();
    })
    
  },
  data() {
    return {
      // background_color:'steelblue',
      // lineColor:'LightCoral',

      impo_data:[],
      attn_data:[],
      data: [],
      sentence_selected:5, //初始时自动选择第一句
      tokens:[]
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

      
      const margin = { top: 10, right: 30, bottom: 15, left: 30 },
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

      // svg.append('g')
      //   .attr('id','detail')
      //   .attr('transform','translate('+(height+margin.right) +',0)')

      // var click=function(d,data,){//todo:
      // const req_data=detail_attn.filter(ele=>ele.layer===data.layer&&ele.head===data.head)//迷之..是个数组
      // var line_data=req_data[0].attn

      // const detailDomain=Object.keys(tokens)
      // const detailScale= d3.scaleBand().range([0,height]).domain(detailDomain).padding(0);
      // if(d3.select('#leftAxis')._groups[0][0]===null){

      //   const tickData=Object.entries(tokens)
      
      // d3.select('#detail').append('g').style("font-size",10)
      //   .attr("id", "leftAxis")
      //   .call(d3.axisLeft(detailScale).tickSize(0))
      //   .selectAll(".tick")
      //   .attr('class','leftTick')
      //   .data(tickData)
      //   .select("text")
      //   .attr('class','leftText')
      //   .text(function (d) {
      //     return d[1];
      //   })
      //   .style('opacity',0)

      //   d3.select('#leftAxis')
      //   .selectAll('.tokenContainer')
      //   .data(tickData)
      //   .join('rect')
      //   .attr('class','tokenContainer')
      //   .attr('x',-margin.right)
      //   .attr('y',function(d){
      //     return detailScale(d[0])
      //   })
      //   .attr('width',margin.right)
      //   .attr('height',detailScale.bandwidth())
      //   .attr('fill','blue')
      //   .style('opacity',0.0)
      //   .on('mouseover',function(d,data){
      //     highlightSelection(data[0])
      //   })
      //   .on('mouseleave',function(){
      //     unhighlightSelection()
      //   })

      //   token_selected.forEach(function(token){
      //   highlightSelection(token);
      // })

      // d3.select('#detail').append("g")
      //   .style("font-size", 10)
      //   .attr('transform','translate('+(detailWidth-margin.right)+',0)')
      //   .attr('id','rightAxis')
      //   .call(d3.axisRight(detailScale).tickSize(0))
      //   .selectAll(".tick")
      //   .attr('class','rightTick')
      //   .data(tickData)
      //   .select("text")
      //   .attr('class','rightText')
      //   .attr('id',function(d){
      //     return 'rightText'+d[0];
      //   })
      //   .text(function (d) {
      //     return d[1];
      //   })
      //   .style('opacity',1)

      // d3.selectAll(".domain").remove();

      // }
      
      // d3.select('#detail').selectAll('.attn')
      //   .data(line_data)
      //   .join('line')
      //   .attr('class','attn')
      //   .attr('x1',5)
      //   .attr('y1',function(d){
      //       return (detailScale(`${d.source}`)+(detailScale.bandwidth())/2)
      //   })
      //   .attr('x2',detailWidth-margin.right)
      //   .attr('y2',function(d){
      //       return detailScale(`${d.target}`)+detailScale.bandwidth()/2
      //   })
      //   .attr('stroke-width',2.2)
      //   .attr('stroke',lineColor)
      //   .attr('stroke-opacity',function(d){
      //       return +d.val
      //   })

      // }

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
        .on('click',function(event,data){
            d3.selectAll('.impo_rect').style('stroke','none')
        .style('opacity',0.8)


          d3.select(this)
        .style('stroke','blue')
        .style('opacity',1)
          bus.$emit('dispatchheadtoshow',[data.layer,data.head])
        })

      //    function highlightSelection(index) {
      //     //  var targets=[]
      //   d3
      //     .selectAll(".tokenContainer")
      //     .attr("fill", background_color)
      //     .style("opacity", function (d) {
      //       return d[0] == index ? 0.3: 0.0;
      //     });
      //   d3
      //     .selectAll(".attn")
      //     .style("opacity", function (d) {
      //       // if(d.source==+index){
      //       //   console.log(d.target)
      //       //   d3.select('#rightText'+d.target).style("opacity",1)

      //       // }
      //       // console.log(targets)
      //       return d.source == (+index) ? 1.0 : 0.0;
      //     });

      //     d3.selectAll('.leftText')
      //     .style('opacity',function(d){
      //       return d[0] == (+index)? 1:0;
      //     })

      // }

      // function unhighlightSelection() {
      //   d3
      //     .selectAll(".tokenContainer")
      //     .style("opacity", 0.0);
      //   d3.selectAll(".attn").style("opacity", 1);
      // }

    },

    getAll(){
      const path='http://10.192.9.11:5000/query_attn_head/'+this.sentence_selected
      axios.get(path)
        .then((res) => {
          this.impo_data = res.data.importance;
          var tokens =res.data.tokens
          this.attn_data=res.data.detail

          if(this.tokens.length!=0){
            tokens=this.tokens
          }
          
          // console.log()
          this.draw(this.impo_data,tokens,this.attn_data)
        }
        )
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
