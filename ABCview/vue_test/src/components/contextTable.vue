<template>
    <div id="contexttable"></div> 
</template>

<script>
import * as d3 from 'd3';
import axios from "axios";
import bus from './bus';
export default {
    name:"ContextTable",
    created(){
        bus.$on('highlighttoken',val=>{
            d3.select('#node-'+val).selectChild('rect').style('stroke', 'black').style('stroke-width', 2)

        })
        bus.$on('unhighlighttoken',val=>{
            d3.select('#node-'+val).selectChild('rect').style('stroke', 'hsl(180, 1%, 80%)')
        })
        bus.$on('dispatchtokentoshow',val=>{
            if( d3.select('#node-'+val).attr('stroke')=='#ff6131'){
                        d3.select('#node-'+val).attr("stroke",undefined)
                    }
                    else d3.select('#node-'+val).attr("stroke","#ff6131")
        })
        bus.$on('reset_tokens',()=>{
            d3.selectAll('.node').attr("stroke",undefined)
        })
        bus.$on('init_tokens',valued_nodes_group=>{
            d3.selectAll('.node').attr("stroke",undefined)
        valued_nodes_group.forEach(node_id => {
          d3.select('#node-'+node_id).attr("stroke","#ff6131")
    //       valued_nodes_group.forEach(function(node){
    //     bus.$emit('dispatchtokentoshow',node)
    //   })
          
      });
    })
    },
    data(){
        return{
            SVGPadding:{
                left:0,
                top:5
            },
            textTokenPadding:{
                top:1, bottom:1,
                left:3, right:3,
            },
            width:460,
            height:100,
            select:[],
            tokens: [
            ],
        }
    },
    mounted(){
        // //'do nothing')
        bus.$on("inputtoshow",val =>{
        this.getAll(val[0], val[1])
        d3.select('#tokensvg').remove();   //删除整个SVG
        d3.select('#tokensvg')
            .selectAll('*')
            .remove();                    //清空SVG中的内容
        this.drawParagraph(this.tokens, this.SVGPadding, this.textTokenPadding);
        })
        // this.drawParagraph(this.tokens,this.SVGPadding,this.textTokenPadding);
    },
    methods: {
        getAll(input_idx, stage_idx){
            const path =
        "http://10.192.9.11:8000/query_context_view/";
          axios
            .post(path, {
                ctx_id: input_idx,
                stage_id:stage_idx
            })
            .then((res) => {
                //res.data.select)
                this.tokens = res.data.tokens;
                this.select = res.data.select;
            })
            .catch((error) => {
                console.error(error);
            });
        },
        getTokenWidth(tokens, svg, fontSize){
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
                .text(d => d[0]);

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
            // 为啥点击一次以后页面没有更新？？（明明显示draw触发了的
            //"draw")
            var cls = 0
             for (var i = 0; i < tokens.length-1; i++) {
                if (tokens[i+1][0]=="[CLS]") {
                    cls = i
                }
            }
            // cls>0 表示retriever 分开encode
            var qArray = tokens.slice(0, cls+1)
            var ctxArray = tokens.slice(cls+1, tokens.length) 
            let qMax = d3.max(qArray.map(d => Math.abs(d[1])));
            let ctxMax = d3.max(ctxArray.map(d => Math.abs(d[1])));
            let qColorScale = d3.scaleLinear()
            .domain([0, qMax])
            .range([d3.rgb('#ffffff'), d3.rgb('#1a75ff')]);
            let ctxColorScale = d3.scaleLinear()
            .domain([0, ctxMax])
            .range([d3.rgb('#ffffff'), d3.rgb('#E50035')]);
            // 否则就是ranker/reader
            let largestAbs = d3.max(tokens.map(d => Math.abs(d[1])));

            let tokenColorScale = d3.scaleLinear()
                .domain([0, largestAbs])
                .range([d3.rgb('#ffffff'), d3.rgb('#E50035')]);


            const svg = d3.select("#contexttable")
            .append('svg')
            .attr('id',"tokensvg")
            .attr('width', this.width)
            .attr('height', this.height);

            let SVGWidth = this.width;
            let fontSize = '0.7em'
            let textTokenSize = this.getTokenWidth(tokens, svg, fontSize);
            let textTokenWidths = textTokenSize.textTokenWidths;
            let textTokenHeight = textTokenSize.textTokenHeight;
            let containerWidthFactor = 1;
            let containerWidth = SVGWidth * containerWidthFactor;

            const tokenGap = 1;
            const rowGap = textTokenHeight + textTokenPadding.top + textTokenPadding.bottom + 2;

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

                // Shift to next row if needed (retriever或是宽度不够了)
                if (curLineLength > containerWidth || (cls>0 && i==cls)) {
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
                // .style('fill', "white")
                .style('fill', function(d,i){
                    if(cls>0){
                        if(i<=cls){
                            return qColorScale(d[1])
                        }
                        else{
                            return ctxColorScale(d[1])
                        }
                    }
                    else{
                        return tokenColorScale(d[1])
                    }
                })
                .style('stroke', (_,i)=>{
                    if(this.select.includes(i)){
                        return "black"
                    }
                    else{
                        return 'hsl(180, 1%, 80%)'
                    }
                })
                .style('stroke-width', (_,i)=>{
                    if(this.select.includes(i)){
                        return 1
                    }
                    else{
                        return 0
                    }
                })

            nodes.append('text')
                .attr('class', 'text-token-arc')
                .attr('x', textTokenPadding.left)
                .attr('y', textTokenPadding.top + 10)
                .style('pointer-events', 'none')
                // .text(d => d.token);
                .text(d => d[0])
                .style('font-size', fontSize)
            nodes.each(function(_,i){
                d3.select(this)
                .on("click",function(){
                    // if(d3.select(this).attr("stroke")=="#ff6131"){
                    //     d3.select(this).attr("stroke",undefined)
                    // }
                    // else d3.select(this).attr("stroke","#ff6131")
                    //'token table emit',i)

                    bus.$emit("dispatchtokentoshow",i)
                    //单击事件：传递需要在tsne视图中显示或删除的token的index
                    
                    //"emit")
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
#contexttable{
  overflow: auto;

}

.node-group g:hover {
    fill:grey;
}
</style>