<template>
    <svg/>
</template>

<script>
import * as d3 from "d3";
export default {
    name:'EmBarchart',
    props:['rect_data'],
    mounted(){
        this.draw()
    },
    methods:{
        draw(){
            const data=this.rect_data
            const svg_width=d3.select(this.$el).style("width")
            const svg_height=d3.select(this.$el).style("height")
            const scale=d3.scaleLinear()
              .domain([0,1])
              .range([0,svg_width]);
            d3.select(this.$el)
            .append('g')
            .append('rect')
            .attr('width', scale(data))
            .attr('height',svg_height)
            .attr('fill','steelblue')
        }
    }
}
</script>

<style scoped>
svg{
    height:20px
}
</style>
