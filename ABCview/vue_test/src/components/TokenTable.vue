<template>
    <div id="tokentable"></div> 
</template>

<script>
import * as d3 from 'd3';
import bus from './bus';
export default {
    name:"TokenTable",
    created(){
        bus.$on("dispatchsentencetoshow",val =>{
            this.tokens = val[0];
            d3.select('#tokensvg').remove();   //删除整个SVG
            d3.select('#tokensvg')
                .selectAll('*')
                .remove();                    //清空SVG中的内容
            this.drawParagraph(this.tokens,this.SVGPadding,this.textTokenPadding);
        })
        bus.$on('highlightToken',val=>{
            d3.select('#node-'+val).selectChild('rect').style('fill','Lavender')

        })
        bus.$on('tsne_to_table',val=>{
            d3.select('#node-'+val).selectChild('rect').style('stroke','blue')

            if( d3.select('#node-'+val).style('stroke')=='blue'){

           
                        d3.select('#node-'+val).style("stroke",undefined)
                    }
                    else d3.select('#node-'+val).attr("stroke","#ff6131")


        })
        bus.$on('unhighlight',val=>{
            d3.select('#node-'+val).selectChild('rect').style('fill','white')
        })
        bus.$on('dispatchtokentoshow',val=>{

            if( d3.select('#node-'+val).attr('stroke')=='#ff6131'){

           
                        d3.select('#node-'+val).attr("stroke",undefined)
                    }
                    else d3.select('#node-'+val).attr("stroke","#ff6131")
        }),
        bus.$on('reset_tokens',()=>{
            d3.selectAll('.node').attr("stroke",undefined)

        }),
        bus.$on('init_tokens',valued_nodes_group=>{
            d3.selectAll('.node').attr("stroke",undefined)
        valued_nodes_group.forEach(node_id => {
          d3.select('#node-'+node_id).attr("stroke","#ff6131")
          
      });
    })
    },
    data(){
        return{
            SVGPadding:{
                left:0,
                top:0
            },
            textTokenPadding:{
                top:2, bottom:2,
                left:5, right:5,
            },
            width:800,
            height:400,
            tokens: [
                "[CLS]",
                "The",
                "new",
                "rights",
                "are",
                "nice",
                "enough",
                "[SEP]",
                "Everyone",
                "really",
                "likes",
                "the",
                "newest",
                "benefits",
                "[SEP]"
            ],
        }
    },
    mounted(){
        this.drawParagraph(this.tokens,this.SVGPadding,this.textTokenPadding);
    },
    methods: {
        getTokenWidth(tokens, svg, fontSize='1em'){
            //先把tokens转成svg中的text元素，用getBBox()计算出最小矩形的尺寸，再把这个text部分删除
            let textTokenWidths = {};
            let textTokenHeight = null;

            let hiddenTextGroup = svg.append('g')
                .attr('class', 'hidden-text')
                .style('opacity', 0);

            let hiddenTexts = hiddenTextGroup.selectAll('.text-token')
                .data(tokens)
                .join('text')
                .attr('class', 'text-token')
                .style('font-size', fontSize)
                .text(d => d);

            hiddenTexts.each(function (_, i) {
                let bbox = this.getBBox();
                textTokenWidths[i] = +Number(bbox.width).toFixed(2);
                if (textTokenHeight == null) {
                textTokenHeight = bbox.height;
                }
            });
            hiddenTextGroup.remove();
            hiddenTexts.remove();
            return { textTokenWidths: textTokenWidths, textTokenHeight: textTokenHeight };
        },
        // drawParagraph = (saliencies, svg, SVGWidth,
        //     SVGPadding, textTokenPadding, wordToSubwordMap, tokenNodeMouseover,
        //     tokenNodeMouseleave) => {
        drawParagraph(tokens,SVGPadding, textTokenPadding){
            // Give each saliency token a unique name
            // if (saliencies.tokens[0].id !== undefined) {
            //     let tokenCount = {};
            //     saliencies.tokens.forEach(d => {
            //     let curCount = 0;
            //     if (tokenCount[d.token] === undefined) {
            //         tokenCount[d.token] = curCount + 1;
            //     } else {
            //         curCount = tokenCount[d.token];
            //         tokenCount[d.token] += 1;
            //     }
            //     d.id = `${tokenIDName(d.token)}-${curCount}`;
            //     });
            // }
            // let tokens = saliencies.tokens;
            
            // let key = saliencies.meta['predicted_label'];
            // let largestAbs = d3.max(saliencies.tokens.map(d => Math.abs(d[key])));

            // let tokenColorScale = d3.scaleLinear()
            //     .domain([0, largestAbs])
            //     .range([d3.rgb('#ffffff'), d3.rgb('#E50035')]);

            // Before drawing the texts, pre-render all texts to figure out their widths
            // let textTokenSize = getTokenWidth(tokens.map(d => d.token), svg);

            const svg = d3.select("#tokentable")
            .append('svg')
            .attr('id',"tokensvg")
            .attr('width', this.width)
            .attr('height', this.height);

            let SVGWidth = this.width;
            let textTokenSize = this.getTokenWidth(tokens, svg);
            let textTokenWidths = textTokenSize.textTokenWidths;
            let textTokenHeight = textTokenSize.textTokenHeight;
            let containerWidthFactor = 1;
            let containerWidth = SVGWidth * containerWidthFactor;

            const tokenGap = 5;
            const rowGap = textTokenHeight + textTokenPadding.top + textTokenPadding.bottom + 10;

            // Add tokens
            let tokenGroup = svg.append('g')
                // .attr('class', 'token-group-saliency')
                .attr('id', 'token-group')
                .attr('transform', `translate(${SVGPadding.left + SVGWidth * (1 - containerWidthFactor) / 2},
                ${SVGPadding.top})`);
            let count = -1;
            let nodes = tokenGroup.append('g')
                .attr('class', 'node-group')
                .selectAll('g')
                // .data(tokens, d => d.id)
                .data(tokens)
                .join('g')
                // .attr('class', d => {
                // let cls = `node node-${d.id}`;
                // if (wordToSubwordMap[d.token] !== undefined) {
                //     wordToSubwordMap[d.token].forEach(n => {
                //     cls += ` node-${n}`;
                //     });
                // }
                // return cls;
                // })
                
//这边统一用token的位置来做id，方便后续和别的视图link时选择token（否则在第一句和第二句甚至同一句中同样的token多次出现，单独处理会比较麻烦）
//似乎没有必要...可以直接nodes.each(function(_,i){})来处理，见208行
                .attr('id', function(){
                    count += 1;
                    return `node-${count}`
                })
                .attr('class','node');
                // .on('mouseover', tokenNodeMouseover)
                // .on('mouseleave', tokenNodeMouseleave);

            // Dynamically change the position of each token node
            // Change the positions of tokens based on their width
            let curPos = {x: 0, y: 0};
            // let tokenNum = Object.keys(textTokenWidths).length;  
            let tokenNum = tokens.length;
            let textTokenPositions = {};

            // Change the position of the text token
            nodes.each(function(_, i) {
                d3.select(this)
                .attr('transform', `translate(${curPos.x}, ${curPos.y})`);
                
                // Record the new position
                textTokenPositions[i] = {x: curPos.x, y: curPos.y};

                // Update the next position
                let curLineLength = curPos.x + textTokenWidths[i] + textTokenPadding.left +
                                    textTokenPadding.right + tokenGap;
                if (i + 1 < tokenNum) {
                curLineLength += textTokenWidths[i + 1];
                }

                // Shift to next row if needed
                if (curLineLength > containerWidth) {
                curPos.y += rowGap;
                curPos.x = 0;
                } else {
                curPos.x = curPos.x + textTokenWidths[i] + textTokenPadding.left + textTokenPadding.right + tokenGap;
                }
            });

            nodes.append('rect')
                .attr('width', (_, i) => textTokenWidths[i] + textTokenPadding.left + textTokenPadding.right)
                .attr('height', textTokenHeight + textTokenPadding.top + textTokenPadding.bottom)
                .attr('rx', 5)
                .style('fill', "white")
                // .style('fill', d => tokenColorScale(+d[key]))
                .style('stroke', 'hsl(180, 1%, 80%)');

            nodes.append('text')
                .attr('class', 'text-token-arc')
                .attr('x', textTokenPadding.left)
                .attr('y', textTokenPadding.top + 13)
                .style('pointer-events', 'none')
                // .text(d => d.token);
                .text(d => d);
            nodes.each(function(_,i){
                d3.select(this)
                .on("click",function(){
                    // if(d3.select(this).attr("stroke")=="#ff6131"){
                    //     d3.select(this).attr("stroke",undefined)
                    // }
                    // else d3.select(this).attr("stroke","#ff6131")
                    bus.$emit("dispatchtokentoshow",i)//单击事件：传递需要在tsne视图中显示或删除的token的index
                })
            })

            d3.select('#tokensvg').attr('height',document.getElementById("token-group").getBBox().height)
            // Create legend for the saliency map view
            // let legendGroup = svg.append('g')
            //     .attr('class', 'legend-group')
            //     .attr('transform', `translate(${SVGPadding.left + 10 + SVGWidth * (1/2 * containerWidthFactor + 1/2)},
            //     ${SVGPadding.top + 50})`);

            // let legendPos = {width: 10, height: 150};

            // drawSaliencyLegend(legendGroup, legendPos, largestAbs);

            },

            // const drawSaliencyLegend = (legendGroup, legendPos, largestAbs) => {
            // // Define the gradient
            // let legentGradientDef = legendGroup.append('defs')
            //     .append('linearGradient')
            //     .attr('x1', 0)
            //     .attr('y1', 1)
            //     .attr('x2', 0)
            //     .attr('y2', 0)
            //     .attr('id', 'legend-gradient');

            // legentGradientDef.append('stop')
            //     .attr('stop-color', '#FFFFFF')
            //     .attr('offset', 0);

            // legentGradientDef.append('stop')
            //     .attr('stop-color', '#E50035')
            //     .attr('offset', 1);

            // legendGroup.append('rect')
            //     .attr('x', 0)
            //     .attr('y', 0)
            //     .attr('width', legendPos.width)
            //     .attr('height', legendPos.height)
            //     .style('fill', 'url(#legend-gradient)')
            //     .style('stroke', 'black');

            // // Draw the legend axis
            // let legendScale = d3.scaleLinear()
            //     .domain([0, largestAbs])
            //     .range([legendPos.height, 0])
            //     .nice();

            // legendGroup.append('g')
            //     .attr('transform', `translate(${legendPos.width}, ${0})`)
            //     .call(d3.axisRight(legendScale).ticks(10));

            // legendGroup.append('text')
            //     .attr('x', 5)
            //     .attr('y', -15)
            //     .style('font-size', '12px')
            //     .style('dominant-baseline', 'end')
            //     .style('text-anchor', 'middle')
            //     .text('Saliency Score');
            // }
    }
}
</script>

<style>
#tokentable{
  overflow: auto;

}

.node-group g:hover {
    fill:grey;
}
</style>