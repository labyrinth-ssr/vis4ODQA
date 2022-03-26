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

            const em_g=d3.select(this.$el)
            .append('g')

            function roundFun(value, n) {
                return Math.round(value*Math.pow(10,n))/Math.pow(10,n);
            }
            em_g.append('rect')
            .attr('width', scale(data))
            .attr('height',svg_height)
            .attr('fill','#EFE5AE')

            em_g.append('text')
            // .attr('transform','translate('+(-20)+',0)')
            .attr("x",scale(data))
            .attr('y',10)
            .text(roundFun(data*100,2)+'%')
            .style('font-size','10px')
            .style('text-anchor',parseInt(scale(data))<20?'start':'end')
        }
    }
}
</script>

<style scoped>
svg{
    height:20px
}
</style>
