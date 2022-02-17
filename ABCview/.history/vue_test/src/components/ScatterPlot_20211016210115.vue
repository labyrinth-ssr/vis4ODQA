<template>
  <div class="container-scatter-plot">
    <div id="title" class="chart-title">
      <a-button id="startLine" type="primary" size="small">Motion trajectory></a-button>
      <a-button id="changetype" type="primary" size="small" v-on:click="changetype">{{this.showtype}}></a-button>
    </div>
    <div  id="scatter-plot" class="scatter-plot">
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios'
import bus from './bus'

export default {
  name: 'ScatterPlot',

  created(){
    bus.$on("dispatchlayerspan",val =>{
      var layer_selected=[];
      for(var i= val[0];i<=val[1];i++){
        layer_selected.push(i-1);
      }
      this.layer_selected = layer_selected;
      this.getAll();
    })
    bus.$on("dispatchsentencetoshow",val =>{
      this.sentence_selected = val[1];
      this.selected_token=[];
      // this.getAll();
    })
    bus.$on("dispatchtokentoshow",val =>{
      // console.log("scatter token dispatch")
      var a=this.selected_token;
    // console.log(a);
      if(a.indexOf(val)>=0){
        a.splice(a.indexOf(val),1)
      }
      else a.push(val)
      this.selected_token=a;
    //   var b=this.selected_token;
    // console.log(b);
      this.getAll();
    })
    bus.$on('reset_tokens',()=>{
      this.selected_token=[];
      this.getAll();
    })
    // ,
    bus.$on('init_tokens',valued_nodes_group=>{
      // console.log("scatter init")
      valued_nodes_group.forEach((node)=>{
        if (this.selected_token.indexOf(node) >= 0) {//
        this.selected_token.splice(this.selected_token.indexOf(node), 1);
      }
      else {this.selected_token.push(node);}
      })
      this.getAll();
      
    })
  },
  data(){
    return {
      // api provided by freeCodeCamp
      showtype: "sentence",
      tsnedata: [], //所有的data
      sentence_selected:4, //初始时自动选择第5句
      layer_selected: [0,1,2,3,4,5,6,7,8,9,10,11], //被选中的layer，用于过滤
      selected_token: [], //被选中的token的index，用于过滤（注意是index（int)而不是token(str)，以防多个词反复出现时选取错误）
      data_to_show: [],
      widthChart: 350, // width of #scatter-plot svg
      heightChart: 350, // height of #scatter-plot svg
      padding: 50, // padding of chart
      // array of objects for the graph legend text
      legendData: [//仅仅是给句子tsne用的
        {
          Text: 'Sentence1',
          Sentence1: 'Yes',
        },
        {
          Text: 'Sentence2',
          Sentence1: '',
        },
      ],
      tokenlegendData:[], //用于token tsne legend的Data
      color: [
        "#c25ec3", 
        "#73A373", 
        "#52f3a9", 
        "#EA7E53", 
        "#EEDD78", 
        "#759AA0", 
        "#1e9d95", 
        "#7289AB", 
        "#E69D87", 
        "#47c0d4", 
        "#d54873", 
        "#ff1c12", 
        "#ff8603", 
        "#4B8E6F", 
        "#ff6131", 
        "#ffde1d", 
        "#386F38", 
        "#388589",
        "#385177",
        "#50964A",
        "#C16B0D",
        "#FF190F",
        "#45BFD3",
        "#FF5F2F",
        "#50F3A8",
        "#FF4800",
        "#FFDE1A",
        "#41D541",
        "#32E7EF",
        "#3B7CDE",
        "#58FD4A",
        "#FF8500"
      ]
    }
  },

  mounted() {
    this.getAll()
  },
  
  methods: {
    changetype(){
      if(this.showtype=="sentence"){
        this.showtype="token";
      }
      else {this.showtype="sentence";}
      this.getAll();
    },
    update(){
      d3.select('#scattersvg').remove();   //删除整个SVG
      d3.select('#scattersvg')
        .selectAll('*')
        .remove()
      this.tokenlegendData=[]
    },
    getAll(){
      var path;
      if(this.showtype=="sentence"){
        path = "http://10.192.9.11:5000/query_sentence_tsne";
      }
      else {path = "http://10.192.9.11:5000/query_tsne";}
      axios.get(path)
        .then((res)=>{
          if(this.showtype=="token") {this.tsnedata = res.data[this.sentence_selected];}
          else{
            this.tsnedata=res.data;
          }
        })
        .then(() => this.update())
        .then(() => this.datainit())
        .then(() => this.graphinit())
        .catch((error) => console.log(error));
    },
    datainit(){
      if(this.showtype=="token"){
        this.data_to_show = this.tsnedata.filter(datum =>{
          return (this.selected_token.indexOf(datum.index)>=0
                &&this.layer_selected.indexOf(datum.layer)>=0)
        })
        for (var i = 0; i < this.selected_token.length; i++) {
          this.tokenlegendData.push(this.data_to_show.find((item) => {
            if(item.index === this.selected_token[i]){
              return item
            }
          }))
          this.tokenlegendData[i].color=this.color[i]
        }
        // this.tsnedata.forEach(element => {
        //   element.color = "#6B7377"
        // });
        this.data_to_show.forEach(element => {
          var index = this.selected_token.indexOf(element.index)
          element.color = this.color[index]
        });
      }else {
        this.data_to_show = this.tsnedata.filter(datum =>{
          return ((datum.index==this.sentence_selected)
                &&this.layer_selected.indexOf(datum.layer)>=0)
        })
      }
    },
    graphinit(){
      // choose element to draw our svg
      const svg = d3.select('#scatter-plot')
        .append('svg')
        .attr('id',"scattersvg")
        .attr('width', this.widthChart)
        .attr('height', this.heightChart);

      // setup x-axis (year)
      const xScale = d3.scaleLinear()
        // minus and plus one year to give padding for the data
        .domain([
          d3.min(this.data_to_show, (d) => d['tsne'][0]-5),
          d3.max(this.data_to_show, (d) => d['tsne'][0]+5)
        ])
        .range([
          this.padding,
          this.widthChart - this.padding,
        ]);

      // setup y-axis
      const yScale = d3.scaleTime()
        .domain([
          d3.min(this.data_to_show, (d) => d['tsne'][1]-5),
          d3.max(this.data_to_show, (d) => d['tsne'][1]+5)
        ])
        .range([
          this.heightChart - this.padding,
          this.padding,
        ]);

      // functional declaration for drawing x-axis with no comma in the labels
      const xAxis = d3.axisBottom(xScale)
        .tickFormat(d3.format('d'));

      // functional declaration for drawing y-axis with label in minutes:seconds format
      const yAxis = d3.axisLeft(yScale)
        .tickFormat(d3.format('d'));

      // group legend elements together
      const legendG = svg.append('g')
        .attr('id', 'legend') // project requirement
        .attr('transform', `translate(${this.widthChart - this.padding - 200},
          ${this.padding-40} )`);

      // function declaration for tooltip div element
      const divTool = d3.select('#scatter-plot')
        .append('div')
        .attr('id', 'tooltip') // project requirement
        .style('opacity', 0);

      // draw x-axis
      svg.append('g')
        .attr('transform', `translate(0, ${this.heightChart - this.padding})`)
        .attr('id', 'x-axis') // project requirement
        .call(xAxis);

      // draw y-axis
      svg.append('g')
        .attr('transform', `translate(${this.padding}, 0)`)
        .attr('id', 'y-axis') // project requirement
        .call(yAxis);
      // draw data points as dots with tooltip pop-up on mouseover
      svg.selectAll('circle')
        .data(this.data_to_show)
        .enter()
        .append('circle')
        .attr('cx', (d) => xScale(d['tsne'][0]))
        .attr('cy', (d) => yScale(d['tsne'][1])) 
        .attr('r', 4)
        // change circle color based on whether sentence1 or not; coordinate with legend
        .attr('class', function(d){
          return d.label+" "+d.layer
        })
        // hover to show value with tooltip as defined in divTool above
        .on('mouseover', (event, d) => {
          divTool
            .attr('class', 'tooltip')
            .style('opacity', '1')
            .style('display', 'flex') // to align items centrally
            // funky offsets here because of setting .scatter-plot to display: relative;
            .style('top', `${event.pageY }px`)
            .style('left', `${event.pageX + 10}px`);
          if(this.showtype=="sentence"){
            divTool.html(`<p>
              <span class="name">index: ${d.index+1}</span>, layer: ${d.layer+1}<br/>
              x: ${d.tsne[0]},<br/>
              y: ${d.tsne[1]}<br/>
            </p>`)
          }
          else{
            divTool.html(`<p>
              <span class="name">${d.tokens}</span>, layer: ${d.layer+1}<br/>
              x: ${d.tsne[0]},<br/>
              y: ${d.tsne[1]}<br/>
            </p>`)
          }
        })
        .on('mouseout', () => {
          divTool
            .style('opacity', 0)
            .style('display', 'none');
        })
        //和tokentable
        .on('click',(event,d)=>{
          bus.$emit('tsne_to_table',d.index);

        })

      // one dot for each label in the legend
      if(this.showtype=="sentence"){
        legendG.selectAll('rect')
          .data(this.legendData)
          .enter()
          .append('rect')
          .attr('x', 240) // color squares are to the left of text
          .attr('y', (d, i) => i * 22) // multiple to set each dot lower than prev
          .attr('height', 12)
          .attr('width', 8)
          .attr('class', (d) => (d.Sentence1 ? 'sentence1' : 'sentence2'));
              // text labels for legend
        legendG.selectAll('text')
          .data(this.legendData)
          .enter()
          .append('text')
          .attr('x', 160)
          .attr('y', (d, i) => 10 + (i * 22))
          .text((d) => d.Text)
          .attr('class', 'legend-text');
      }
      else{
          svg.selectAll('circle')
          .attr('class', function(d){
            return d.layer
          })
          .attr('fill',function(d){
            return d.color
          })
          legendG.selectAll('rect')
          .data(this.tokenlegendData)
          .enter()
          .append('rect')
          .attr('x', 240) 
          .attr('y', (d, i) => i * 22) // multiple to set each dot lower than prev
          .attr('height', 12)
          .attr('width', 8)
          // .attr('class', (d) => (d.Sentence1 ? 'sentence1' : 'sentence2'));
          .attr('fill',function(d){
            return d.color
          })
          // 获取最长token的length 以保证sentence能够对齐
          var tokenmaxlen=d3.max(this.tokenlegendData,function(d){
            return d.tokens.length
            })
          legendG.selectAll('text')
          .data(this.tokenlegendData)
          .enter()
          .append('text')
          .attr('x', 80)
          .attr('y', (d, i) => 10 + (i * 22))
          .text(function(d){
            var space = " "
            for(var i=0;i<(tokenmaxlen-d.tokens.length);i++){
              space +='\u00A0'
            }
            var text = d.tokens+space+d.label
            return (text)
          })
          .attr('class', 'legend-text')
          .attr('style', 'white-space:pre');
      }


      const line_generator = function(data,i,color){
          const line = d3.line()
          .x(d => {return xScale(d['tsne'][0])})
          .y(d => {return yScale(d['tsne'][1])})
          //.curve(d3.curveBasis)
          .curve(d3.curveCardinal.tension(0.5))
          
          var currentid = "Path"+i;
          // var Gradientid = "svgGradient"+i;
          // var defs = svg.append("defs");

          // var gradient = defs.append("linearGradient")
          // .attr("id", Gradientid)
          // .attr("x1", "0%")
          // .attr("x2", "100%")
          // .attr("y1", "0%")
          // .attr("y2", "100%");

          // gradient.append("stop")
          // .attr('class', 'start')
          // .attr("offset", "0%")
          // .attr("stop-color",color)
          // .attr("stop-opacity", 0);

          // gradient.append("stop")
          // .attr('class', 'end')
          // .attr("offset", "100%")
          // .attr("stop-color",color)
          // .attr("stop-opacity", 1);

          d3.select("#"+currentid).datum(data)
          .attr('class', 'datacurve')
          .attr("fill", "none")
          .attr("stroke-width", 2.5)
          .attr("d", line)
          .attr("stroke",color)
          // .attr("stroke", `url(#${Gradientid})`)
          
          d3.select("#startLine").on("click", function(){
          d3.selectAll('.datacurve')
          .attr("stroke-dasharray", function() {
            var totalLength = this.getTotalLength();
            return totalLength + " " + totalLength;
          })
          .attr("stroke-dashoffset", function() {
            var totalLength = this.getTotalLength();
            return totalLength;
          })
          .transition()
          .duration(3000)
          .attr("stroke-dashoffset", 0);
          })
        }
      var data = [];
      if(this.showtype=="token"){
        for(var i=0;i<this.selected_token.length;i++){
          data = this.data_to_show.filter(datum => {return datum['index']==this.selected_token[i]});
          var currentid = "Path"+i;
          svg.append('path').attr('id', currentid);
          line_generator(data,i,this.color[i]);
        }
      }
      else{
        data = this.data_to_show.filter(datum =>{return datum['label']=="sentence1"});
        currentid = "Path0";
        svg.append('path').attr('id', currentid);
        line_generator(data,0,this.color[0]);

        data = this.data_to_show.filter(datum =>{return datum['label']=="sentence2"});
        currentid = "Path1";
        svg.append('path').attr('id', currentid);
        line_generator(data,1,this.color[1]);
      }
    },
  },
};
</script>

<style lang="scss">
/*
 * NB: Do not scope this component's style! D3 won't be able to see it!!!
 */
@import "../assets/colors.scss";


.chart-title {
  color: $text-gray;
  font-family: "Roboto", Helvetica, Arial, sans-serif;
  margin: 0px 68px;
  padding-top: 1rem;
}

// axis markers
.tick {
  color: $text-gray;
  font-family: "Open Sans", Arial, Helvetica, sans-serif;
}

.axis-label {
  font-size: 0.8rem;
  font-style: italic;
}

// dynamically assigned class for dots to show tokens in sentence1
.sentence1 {
  fill:#c25ec3;
  opacity: 0.9;
}

// dynamically assigned class for dots to show tokens in sentence2
.sentence2 {
  fill:#73A373;
  opacity: 0.9;
}

.legend-text {
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9rem;
}

.tooltip {
  align-items: center;
  background: $mouseover;
  border-radius: 15px;
  border-style: none;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  color: $mouseover-text;
  font-family: Roboto, Helvetica, Arial, sans-serif;
  font-size: 13px;
  padding: 0.6rem;
  position: absolute;
  text-align: left;

  & .name {
    font-weight: bold;
  }

  & .doping-text {
    font-style: italic;
  }
}

.container-scatter-plot{
  height: 100%;
  // overflow: hidden;
}
#scatter-plot{
  height: 90%;
  // overflow: hidden;
}
#title{
  height: 10%;
}
#scattersvg{
   border-radius: 10px;
    background-color: white;
}

</style>