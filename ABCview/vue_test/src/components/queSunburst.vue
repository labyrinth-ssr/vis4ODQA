<template>
  <div id="que-sunburst"></div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import bus from "./bus";

export default {
  name: "queSunburst",
  created() {
      bus.$on("dispatchQueThre", (val) => {
        this.threshold = val;
        this.set_para(this.threshold,this.head,this.layer);
      })
      bus.$on("emitHeadLayer", (val) => {
        this.head=val.head
        this.layer=val.layer
        this.set_para(this.threshold,this.head,this.layer);
      })
  },
  data() {
    return {
      data: [],
      threshold: 50,
      head:0,
      layer:0
    };
  },
  methods: {
    update() {
      this.getAll();
    },
    drawAll(data) {
        d3.select("#sunburstSvg").remove();
        d3.select("#sunburstSvg").selectAll("*").remove();
        var nodeData = { 'name': 'root', 'children': data }
        var margin = { top: 60, right: 10, bottom: 20, left: 10 }

        // var threshold=50
        var width = 400;  // <-- 1
        var height = 400;
        var radius = Math.min(width, height) / 2;  // < -- 2
        // var color = d3.scaleOrdinal(d3.schemePaired);   // <-- 3
// var nodeData = {
//     "name": "TOPICS", "children": [{
//         "name": "Topic A",
//         "children": [{"name": "Sub A1", "size": 4}, {"name": "Sub A2", "size": 4}]
//     }, {
//         "name": "Topic B",
//         "children": [{"name": "Sub B1", "size": 3}, {"name": "Sub B2", "size": 3}, {
//             "name": "Sub B3", "size": 3}]
//     }, {
//         "name": "Topic C",
//         "children": [{"name": "Sub A1", "size": 4}, {"name": "Sub A2", "size": 4}]
//     }]
// };
        

        var svg = d3
        .select("#que-sunburst")
        .append("svg")
        .attr("id", "sunburstSvg")
        .attr('width', width)  // <-- 2
            .attr('height', height+margin.top+margin.bottom)

        const g = svg  // <-- 1
            
            .append('g')  // <-- 3
            .attr('transform', 'translate(' + width / 2 + ',' +( height / 2+margin.top) + ')');  // <-- 4

        var partition = d3.partition()  // <-- 1
            .size([2 * Math.PI, radius]);  // <-- 2

            // var nodeData = { 'name': 'root', 'children': data }

            var root = d3.hierarchy(nodeData)
                .sum(function (d) {
                    return d.size
                });

            partition(root);
            var arc = d3.arc()
                .startAngle(function (d) { return d.x0 })
                .endAngle(function (d) { return d.x1 })
                .innerRadius(function (d) { return d.y0 })
                .outerRadius(function (d) { return d.y1 });

            g.selectAll('g')  // <-- 1
                .data(root.descendants())
                .enter().append('g').attr("class", "node")  // <-- 2
                .append('path')  // <-- 2
                .attr("display", function (d) { 
                  // console.log(d)
                return d.depth ? null : "none"; })
                .attr("d", arc)
                .on('click',function (e,d) {
                    bus.$emit('dispatchQue',d.data.senId)
                })
                .style('stroke', '#fff')
                .style("fill", function (d) { 
                  return d3.interpolateBuPu(d.data.val)
                  // return color((d.children ? d : d.parent).data.name); 
                  });

            g.selectAll(".node")  // <-- 1
                .append("text")  // <-- 2
                .attr("transform", function (d) {
                    return "translate(" + arc.centroid(d) + ")rotate(" + computeTextRotation(d) + ")";
                }) // <-- 3
                .attr("dx", "-20")  // <-- 4
                // " + computeTextRotation(d) + "
                .attr("dy", ".2em")  // <-- 5
                .attr('font-size',10 )
                .text(function (d) { return d.parent ? d.data.name : "" });  // <-- 6

            function computeTextRotation(d) {
                var angle = (d.x0 + d.x1) / Math.PI * 90;  // <-- 1

                // Avoid upside-down labels
                return (angle < 180) ? angle-90 : angle + 90;  // <--2 "labels aligned with slices"

                // Alternate label formatting
                //return (angle < 180) ? angle - 90 : angle + 90;  // <-- 3 "labels as spokes"
            }

        // });
    },
    getAll() {
      const path =
        "http:///10.219.186.190:5000/query_que_sunburst";
      axios
        .get(path) 
        .then((res) => {
              this.drawAll(
                res.data
              );

        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    set_para(threshold,head,layer) {
        this.threshold=threshold
        this.head=head
        this.layer=layer
      const path =
        "http:///10.219.186.190:5000/query_que_sunburst";
      axios
        .post(path, {
          threshold:this.threshold,
          head:this.head,
          layer:this.layer
        })
        .then(() => {
          this.getAll();
        });
    },
    init() {
      const path =
        "http:///10.219.186.190:5000/query_que_sunburst";
      axios
        .post(path, {
          threshold: this.threshold,
          head:this.head,
          layer:this.layer
        })
        .then(() => {
          axios
            .get(path)
            .then((res) => {
              this.drawAll(res.data)
              
            })
            .catch((error) => {
              console.error(error);
            })}
            )
        .catch((error) => {
              console.error(error);
            })
        // });
    }}
  ,
  beforeMount() {
    this.init();
  }
}
</script>

<style scoped>


</style>

