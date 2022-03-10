<template>
  <div class="container-scatter-plot">
    <h2 id="title" class="chart-title">
      <a-button id="startLine" type="primary">Motion trajectory></a-button>
    </h2>
    <div id="scatter-plot" class="scatter-plot">
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
    }),
    bus.$on("dispatchsentencetoshow",val =>{
      this.sentence_selected = val[1];
      this.token_selected=[];
      this.getAll();
    })
    bus.$on("dispatchtokentoshow",val =>{
      if(this.token_selected.indexOf(val)>=0){
        this.token_selected.splice(this.token_selected.indexOf(val),1)
      }
      else this.token_selected.push(val)
      this.getAll();
    })
  },
  data(){
    return {
      // api provided by freeCodeCamp
      tsnedata: [], //所有的data
      sentence_selected:0, //初始时自动选择第一句
      layer_selected: [1,2,3,4,5,6,7,8,9,10,11,12], //被选中的layer，用于过滤
      token_selected: [], //被选中的token的index，用于过滤（注意是index（int)而不是token(str)，以防多个词反复出现时选取错误）
      data_to_show: [],
      widthChart: 600, // width of #scatter-plot svg
      heightChart: 300, // height of #scatter-plot svg
      padding: 60, // padding of chart
      // array of objects for the graph legend text
      legendData: [
        {
          Text: 'Sentence 1',
          Sentence1: 'Yes',
        },
        {
          Text: 'Sentence 2',
          Sentence1: '',
        },
      ],
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
    update(){
      d3.select('#scattersvg').remove();   //删除整个SVG
      d3.select('#scattersvg')
        .selectAll('*')
        .remove()
    },
    getAll(){
      const path = "http://10.192.9.11:5000/query_tsne"
      axios.get(path)
        .then((res)=>{
          this.tsnedata = res.data[this.sentence_selected];
        })
        .then(() => this.update())
        .then(() => this.datainit())
        .then(() => this.graphinit())
        .catch((error) => console.log(error));
    },
    datainit(){
      this.data_to_show = this.tsnedata.filter(datum =>{
          return (this.token_selected.indexOf(datum.index)>=0
                 &&this.layer_selected.indexOf(datum.layer)>=0)
        }
      )
    },
    graphinit() {
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
          ${this.padding - 30} )`);

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
        .attr('r', 6)
        // change circle color based on whether sentence1 or not; coordinate with legend
        .attr('class', function(d){
          return d.label+" "+d.layer+" "+d.tokens
        })
        // hover to show value with tooltip as defined in divTool above
        .on('mouseover', (event, d) => {
          
          divTool
            .attr('class', 'tooltip')
            .html(`<p>
              <span class="name">${d.tokens}</span>, layer: ${d.layer+1}<br/>
              x: ${d.tsne[0]},<br/>
              y: ${d.tsne[1]}<br/>
            </p>`)
            .style('opacity', '1')
            .style('display', 'flex') // to align items centrally
            // funky offsets here because of setting .scatter-plot to display: relative;
             .style('top', `${event.layerY }px`)
            .style('left', `${event.layerX + 10}px`);
        })

       
        .on('mouseout', () => {
          divTool
            .style('opacity', 0)
            .style('display', 'none');
        });

      // one dot for each label in the legend
      legendG.selectAll('rect')
        .data(this.legendData)
        .enter()
        .append('rect')
        .attr('x', 180) // color squares are to the left of text
        .attr('y', (d, i) => i * 21) // multiple to set each dot lower than prev
        .attr('height', 12)
        .attr('width', 12)
        .attr('class', (d) => (d.Sentence1 ? 'sentence1' : 'sentence2'));

      // text labels for legend
      legendG.selectAll('text')
        .data(this.legendData)
        .enter()
        .append('text')
        .attr('x', 80)
        .attr('y', (d, i) => 10 + (i * 22))
        .text((d) => d.Text)
        .attr('class', 'legend-text');
      
      const line_generator = function(data,i,color){
          const line = d3.line()
          .x(d => {return xScale(d['tsne'][0])})
          .y(d => {return yScale(d['tsne'][1])})
          //.curve(d3.curveBasis)
          .curve(d3.curveCardinal.tension(0.5))
          
          var currentid = "Path"+i;

          d3.select("#"+currentid).datum(data)
          .attr('class', 'datacurve')
          .attr("fill", "none")
          .attr("stroke", color)
          .attr("stroke-width", 2.5)
          .attr("d", line);

          
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
      var data = []
      for(var i=0;i<this.token_selected.length;i++){
        data = this.data_to_show.filter(datum => {return datum['index']==this.token_selected[i]});
        var currentid = "Path"+i;
        svg.append('path').attr('id', currentid);
        line_generator(data,i,this.color[i]);
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

// .container-scatter-plot {
//   background-color: $chart-background;
//   border-radius: 15px;
//   box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
//   height: 550px;
//   margin: auto;
//   margin-bottom: 2rem;
//   width: 1050px;
// }

.chart-title {
  color: $text-gray;
  font-family: "Roboto", Helvetica, Arial, sans-serif;
  margin-bottom: 0;
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
  fill: $guilty-red;
  opacity: 0.9;
}

// dynamically assigned class for dots to show tokens in sentence2
.sentence2 {
  fill: $clean-green;
  opacity: 0.9;
}

.legend-text {
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
</style>