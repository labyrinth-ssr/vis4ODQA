<template>
    <svg/>
</template>

<script>
import * as d3 from "d3";
export default {
    name:'EmCircle',
    props:['cir_data'],
    mounted(){
        this.draw()
    },
    methods:{
        draw(){
            const data=this.cir_data
            // const svg_width=d3.select(this.$el).style("width")
            // const svg_height=d3.select(this.$el).style("height")
            // const scale=d3.scaleLinear()
            //   .domain([0,1])
            //   .range([0,svg_width]);

            const em_g=d3.select(this.$el)
            .append('g')
            
            em_g.append('circle')
              .attr('cx', 10)
  .attr('cy', 10)
  .attr('r', 5)
  .attr('stroke', '#BBCCDD')
  .attr('fill', data?'#BBCCDD':'none');

        }
    }
}
</script>

<style scoped>
svg{
    height:20px
}
</style>
