<template>
  <div id="instance-view" class="view"></div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import bus from "./bus";

export default {
  name: "InstanceView",
  created() {
    var val = [0, 0]
    bus.$emit("inputtoshow", val)
    bus.$on("dispatchqueid", (val) => {
      this.question_selected = val;
      this.init();
    })
    bus.$on("que_sal_thre", (val) => {
      this.que_sal_thre = val;
      this.init();
    })

    // bus.$on("ctx_sal_thre", (val) => {
    //   this.ctx_sal_thre = val;
    //   this.init();
    // })
    // bus.$on("reranker_sal_thre", (val) => {
    //   this.reranker_sal_thre = val;
    //   this.init();
    // })
    // bus.$on("reader_sal_thre", (val) => {
    //   this.reader_sal_thre = val;
    //   this.init();
    // })
    bus.$on("barchart_thre", (val) => {
      this.barchart_thre = val;
      this.init();
    })
  },
  data() {
    return {
      data: [],
      question_selected: 1, 
      q_tokens: [],
      ctx_tokens: [],
      rank_tokens: [],
      span_tokens: [],
      order_result: [],
      que_sal_thre: 0.03,
      ctx_sal_thre: 0.03,
      reranker_sal_thre: 0.03,
      ranker_sal_thre: 0.03,
      barchart_thre:5
    };
  },
  methods: {
    update() {
      this.getAll();
    },
    showSingleTree(){
      this.$emit('showsingletree',true)
    },
    getTokenWidth(tokens, svg, s, fontSize='1em'){
        //先把tokens转成svg中的text元素，用getBBox()计算出最小矩形的尺寸，再把这个text部分删除
        let textTokenWidths = {};
        let textTokenHeight = {};

        let hiddenTextGroup = svg.append('g')
            .attr('class', 'hidden-text')
            .style('opacity', 0);
        
        console.log(fontSize);

        let hiddenTexts = hiddenTextGroup.selectAll('.text-token')
            .data(tokens)
            .join('text')
            .attr('class', 'text-token')
            // .style('font-size', fontSize)
            .style("font-size", function(d){
              // if(d[1]>0.02){
              //   return s(d[1])+"em"
              // }
              // else{
              //   return s(0.02)+"em"
              // }
              return s(Math.abs(d[1]))+"em"
            })
            .text(d => d[0]);

        hiddenTexts.each(function (_, i) {
            let bbox = this.getBBox();
            textTokenWidths[i] = +Number(bbox.width).toFixed(2);
            if (textTokenHeight == null) {
            textTokenHeight = bbox.height;
            }
            else{
              textTokenHeight[i] = +Number(bbox.height).toFixed(2);
            }
        });
        hiddenTextGroup.remove();
        hiddenTexts.remove();
        return { textTokenWidths: textTokenWidths, textTokenHeight: textTokenHeight };
    },
    drawAll() {
      d3.select("#instanceviewsvg").remove();
      d3.select("#instanceviewsvg").selectAll("*").remove();
      var margin = { top: 20, right: 10, bottom: 50, left: 10 },
        whole_width = 1500,
        whole_height = 400,
        bar_chart_height = 50,
        width = 600,
        height = 25;
      // var color = d3.scaleOrdinal(d3.schemePaired);

      var svg = d3.select("#instance-view")
        .append("svg")
        .attr("id", "instanceviewsvg")
        .attr("width", whole_width + margin.left + margin.right)
        .attr("height", whole_height + margin.top + margin.bottom)
      
      const max_saliency = function(tokens){
        var max_array = []
        tokens.forEach(ele => {
          max_array.push(d3.max(ele.map(d => d[1])))
        });
        return Math.max.apply(null, max_array) 
      }
      var q_max_saliency = max_saliency(this.q_tokens)
      var ctx_max_saliency = max_saliency(this.ctx_tokens)
      var rank_max_saliency = max_saliency(this.rank_tokens)
      var span_max_saliency = max_saliency(this.span_tokens) 

      var q_s = d3.scaleLinear()
        .domain([0.01, q_max_saliency])
        .range([0.6, 1.2]);
      var ctx_s = d3.scaleLinear()
        .domain([0.01, ctx_max_saliency])
        .range([0.6, 1.2]);
      var rank_s = d3.scaleLinear()
        .domain([0.01, rank_max_saliency])
        .range([0.6, 1.2]);
      var span_s = d3.scaleLinear()
        .domain([0.01, span_max_saliency])
        .range([0.6, 1.2]);

      let cell_width = width;
      // let cell_height = height;

      // 预先定义图层，使得方框置于底层
      var q_ctx_rect = svg.append('g');
      var rank_rect = svg.append('g');
      var span_rect = svg.append('g');
      
      var q_lineLengthArray = []
      for (let row_idx = 0; row_idx < 10; row_idx++){
        var q_svg = svg.append("g")
        .attr("class","q_svg")
        .attr("transform",
        "translate(" + margin.left  + "," + (margin.top + bar_chart_height + row_idx*height) + ")")
        var q_lineLength = this.drawParagraph(this.q_tokens[row_idx], q_svg, cell_width, q_s)
        q_lineLengthArray.push(q_lineLength)        
      }
      var q_max_length = Math.max.apply(null, q_lineLengthArray)
      var ctx_lineLengthArray = []
      for (let row_idx = 0; row_idx < 10; row_idx++){
        var ctx_svg = svg.append("g")
        .attr("class","ctx_svg")
        .attr("transform",
        "translate(" + (margin.left + q_max_length) + "," + (margin.top + bar_chart_height + row_idx*height) + ")")
        var ctx_lineLength = this.drawParagraph(this.ctx_tokens[row_idx], ctx_svg, cell_width, ctx_s)        
        ctx_lineLengthArray.push(ctx_lineLength)  
      }
      var ctx_max_length = Math.max.apply(null, ctx_lineLengthArray)
      // for (let row_idx = 0; row_idx < 10; row_idx++){
      //   for (let col_idx=0; col_idx < 2; col_idx++){
      //     if(col_idx==0){
      //       var cell_svg = svg.append("g")
      //       .attr("transform",
      //       "translate(" + margin.left + "," + (margin.top + row_idx*height) + ")")
      //       this.drawParagraph(this.q_tokens[row_idx], cell_svg, cell_width, q_s)
      //       console.log(cell_svg.getBBox().width)
      //     }
      //     else{
      //       cell_svg = svg.append("g")
      //       .attr("transform",
      //       "translate(" + (margin.left + col_idx*width/2) + "," + (margin.top + row_idx*height) + ")")
      //       this.drawParagraph(this.ctx_tokens[row_idx], cell_svg, cell_width, ctx_s)
      //     }
      //   }
      // }
      let separator_width = 50;

      var rank_lineLengthArray = []
      for (let row_idx = 0; row_idx < 10; row_idx++){
          var rank_svg = svg.append("g")
          .attr("transform",
          "translate(" + (separator_width + margin.left + q_max_length + ctx_max_length) + "," + (margin.top + bar_chart_height + row_idx*height) + ")")
          var rank_lineLength = this.drawParagraph(this.rank_tokens[this.order_result[row_idx]], rank_svg, cell_width*1.2, rank_s)
          rank_lineLengthArray.push(rank_lineLength)  
        }
      var rank_max_length = Math.max.apply(null, rank_lineLengthArray)

      var span_lineLengthArray = []
      for (let row_idx = 0; row_idx < 10; row_idx++){
          var span_svg = svg.append("g")
          .attr("transform",
          "translate(" + (separator_width*2 + margin.left + q_max_length + ctx_max_length + rank_max_length) + "," + (margin.top + bar_chart_height + row_idx*height) + ")")
          var span_lineLength = this.drawParagraph(this.span_tokens[this.order_result[row_idx]], span_svg, cell_width*1.2, span_s)
          span_lineLengthArray.push(span_lineLength)  
        }
      var span_max_length = Math.max.apply(null, span_lineLengthArray)
      
      for (let row_idx = 0; row_idx < 10; row_idx++){
          if(this.has_answer_list[row_idx]){
            var line_color = "green";
          }
          else{
            line_color = "red";
          }
          if(this.em_result[row_idx]){
            var em_color = "green";
          }
          else{
            em_color = "red";
          }
          q_ctx_rect.append('rect')
          .attr("class", "rect"+row_idx)
          .attr("x", margin.left)   
          .attr("y", margin.top + bar_chart_height + row_idx*height-5) 
          .attr('width', q_max_length + ctx_max_length)
          .attr('height',height)
          .style('fill', "white")
          .style("opacity", 0.1)
          .style('stroke', "black")
          .on("mouseover",function(){
            d3.selectAll(".rect"+row_idx).style('fill', "#333333")
          })
          .on("mouseleave",function(){
            d3.selectAll(".rect"+row_idx).style('fill', "white")
          })
          .on("click", ()=>{
            var val = [row_idx, 0]
            this.showSingleTree()
            bus.$emit("inputtoshow", val)
            bus.$emit("update_ctx", row_idx)
          })

                  var linkGen = d3
        .linkVertical()
        .source(() =>
          [margin.left + q_max_length + ctx_max_length,
          margin.top + bar_chart_height + row_idx * height + 8]
        )
        .target(() =>
          [separator_width + margin.left + q_max_length + ctx_max_length,
           margin.top +
              bar_chart_height +
              this.order_result[row_idx] * height +
              8]
        );

        svg
          .append("path")
          .attr("class", "line" + row_idx)
          .style("stroke", line_color) // colour the line
          .attr("d", linkGen)
          .attr("stroke-width", 1)
        .attr("fill", "none")

          // svg.append("line")
          // .attr("class", "line"+row_idx)  // line的class应该没啥用
          // .style("stroke", line_color)  // colour the line
          // .attr("x1", margin.left + q_max_length + ctx_max_length)   
          // .attr("y1", margin.top + bar_chart_height + row_idx*height+8)     
          // .attr("x2", separator_width + margin.left + q_max_length + ctx_max_length)    
          // .attr("y2", margin.top + bar_chart_height + this.order_result.indexOf(row_idx)*height+8);  

          rank_rect.append('rect')
          .attr("class", "rect"+this.order_result[row_idx])
          .attr("x", separator_width + margin.left + q_max_length + ctx_max_length)   
          .attr("y", margin.top + bar_chart_height + row_idx*height-5) 
          .attr('width', rank_max_length)
          .attr('height',height)
          .style('fill', "white")
          .style("opacity", 0.1)
          .style('stroke', "black")
          .on("mouseover",()=>{
            d3.selectAll(".rect"+this.order_result[row_idx]).style('fill', "#333333")
          })
          .on("mouseleave",()=>{
            d3.selectAll(".rect"+this.order_result[row_idx]).style('fill', "white")
          })
          .on("click", ()=>{
            var val = [this.order_result[row_idx], 1]
            this.showSingleTree()
            bus.$emit("inputtoshow", val)
            bus.$emit("update_ctx", this.order_result[row_idx])
          })

          svg.append("line")
          .attr("class", "line"+this.order_result[row_idx])
          .style("stroke", line_color) 
          .attr("x1", separator_width + margin.left + q_max_length + ctx_max_length + rank_max_length)   
          .attr("y1", margin.top + bar_chart_height + this.order_result.indexOf(row_idx)*height+8)     
          .attr("x2", separator_width*2 + margin.left + q_max_length + ctx_max_length + rank_max_length)    
          .attr("y2", margin.top + bar_chart_height + this.order_result.indexOf(row_idx)*height+8);

          span_rect.append('rect')
          .attr("class", "rect"+this.order_result[row_idx])
          .attr("x", separator_width*2 + margin.left + q_max_length + ctx_max_length + rank_max_length)   
          .attr("y", margin.top + bar_chart_height + row_idx*height-5) 
          .attr('width', span_max_length)
          .attr('height',height)
          .style('fill', "white")
          .style("opacity", 0.1)
          .style('stroke', "black")
          .on("mouseover",()=>{
            d3.selectAll(".rect"+this.order_result[row_idx]).style('fill', "#333333")
          })
          .on("mouseleave",()=>{
            d3.selectAll(".rect"+this.order_result[row_idx]).style('fill', "white")
          })
          .on("click", ()=>{
            var val = [this.order_result[row_idx], 2]
            this.showSingleTree()
            bus.$emit("inputtoshow", val)
            bus.$emit("update_ctx", this.order_result[row_idx])
          })

          svg.append("line")
          .style("stroke", em_color) 
          .attr("x1", separator_width*2 + margin.left + q_max_length + ctx_max_length + rank_max_length + span_max_length)   
          .attr("y1", margin.top + bar_chart_height + row_idx*height+8)     
          .attr("x2", separator_width*3 + margin.left + q_max_length + ctx_max_length + rank_max_length + span_max_length)    
          .attr("y2", margin.top + bar_chart_height + row_idx*height+8);

          svg.append("text")
          .text(this.final_prediction[row_idx])
          .attr('x', separator_width*3 + margin.left + q_max_length + ctx_max_length + rank_max_length + span_max_length+2)
          .attr('y', margin.top + bar_chart_height + row_idx*height+12)
      }
      var retriever_bar_chart = svg.append('g')
      .attr("transform", "translate(" + margin.left  + "," + margin.top + ")")
      var rank_bar_chart = svg.append('g')
      .attr("transform", "translate(" + (separator_width + margin.left + q_max_length + ctx_max_length)  + ","  
      + margin.top + ")")
      var span_bar_chart = svg.append('g')
      .attr("transform", "translate(" + (separator_width*2 + margin.left + q_max_length + ctx_max_length + rank_max_length)  + ","  
      + margin.top + ")")

      const bar_chart_height_no_text = bar_chart_height - 20

      const retriever_x = d3.scaleBand()
      .domain(this.retriever_summary.map(d=>d[0]))
      .range([0, q_max_length + ctx_max_length])
      .padding([0.1])
      retriever_bar_chart.append("g")
        .attr("transform", `translate(0, ${bar_chart_height_no_text})`)
        .call(d3.axisBottom(retriever_x).tickSize(0));
      
      const rank_x = d3.scaleBand()
      .domain(this.rank_summary.map(d=>d[0]))
      .range([0, rank_max_length])
      .padding([0.1])
      rank_bar_chart.append("g")
        .attr("transform", `translate(0, ${bar_chart_height_no_text})`)
        .call(d3.axisBottom(rank_x).tickSize(0));

      const span_x = d3.scaleBand()
      .domain(this.span_summary.map(d=>d[0]))
      .range([0, span_max_length])
      .padding([0.1])
      span_bar_chart.append("g")
        .attr("transform", `translate(0, ${bar_chart_height_no_text})`)
        .call(d3.axisBottom(span_x).tickSize(0));
      
      const retriever_x_subgroup = d3.scaleBand()
      .domain([2,3])
      .range([0, retriever_x.bandwidth()])
      .padding([0.05])
      const rank_x_subgroup = d3.scaleBand()
      .domain([2,3])
      .range([0, rank_x.bandwidth()])
      .padding([0.05])
      const span_x_subgroup = d3.scaleBand()
      .domain([2,3])
      .range([0, span_x.bandwidth()])
      .padding([0.05])
      const color = d3.scaleOrdinal()
      .domain([2,3])
      .range(['#377eb8','#4daf4a'])

      const y = d3.scaleLinear()
      .domain([0, 10])
      .range([bar_chart_height_no_text, 0]);

      const groups = [retriever_x_subgroup, rank_x_subgroup, span_x_subgroup]
      const subgroups = [retriever_x_subgroup.bandwidth(), rank_x_subgroup.bandwidth(),span_x_subgroup.bandwidth()]
      const min_bandwidth = Math.min.apply(null, subgroups)
      const select_group_idx = subgroups.indexOf(min_bandwidth)
      const select_group = groups[select_group_idx]

      retriever_bar_chart.append("g")
      .selectAll("g")
      .data(this.retriever_summary)
      .join("g")
        .attr("transform", d => `translate(${retriever_x(d[0])}, 0)`)
      .selectAll("rect")
      .data(function(d) { return [2,3].map(function(key) { return {key: key, value: d[key], kind: d[1], token:d[0]}; }); })
      .join("rect")
        .attr("x", function(d){
          if(d.kind==0){
            return select_group(d.key) + retriever_x_subgroup.bandwidth() - min_bandwidth + 0.05
          }
          else{
            // kind = 1 q_only
            if(d.kind == 1 ){
              var c = 0.25
            }
            // kind = 2 ctx_only
            else{
              c = -0.25
            }
            return retriever_x_subgroup(d.key) + c * retriever_x.bandwidth() + 0.5*retriever_x_subgroup.bandwidth() - 0.5*min_bandwidth
          }
        })
        .attr("y", d => y(d.value))
        .attr("width", min_bandwidth)
        .attr("height", d => bar_chart_height_no_text - y(d.value))
        .attr("fill", d => color(d.key))
        .on("mouseover",function(_,d){
          d3.selectAll('.node-'+d.token).selectChild('rect').style('stroke', 'black').style('stroke-width', 2)
        })
        .on("mouseleave",function(_,d){
          d3.selectAll('.node-'+d.token).selectChild('rect').style('stroke', 'hsl(180, 1%, 80%)')
        })
      
      rank_bar_chart.append("g")
      .selectAll("g")
      .data(this.rank_summary)
      .join("g")
        .attr("transform", d => `translate(${rank_x(d[0])}, 0)`)
      .selectAll("rect")
      .data(function(d) { return [2,3].map(function(key) { return {key: key, value: d[key], kind: d[1], token:d[0]}; }); })
      .join("rect")
        .attr("x", function(d){
          if(d.kind==0){
            return select_group(d.key) + rank_x_subgroup.bandwidth() - min_bandwidth + 0.05
          }
          else{
            // kind = 1 q_only
            if(d.kind == 1 ){
              var c = 0.25
            }
            // kind = 2 ctx_only
            else{
              c = -0.25
            }
            return rank_x_subgroup(d.key) + c * rank_x.bandwidth() + 0.5*rank_x_subgroup.bandwidth() - 0.5*min_bandwidth
          }
        })
        .attr("y", d => y(d.value))
        .attr("width", min_bandwidth)
        .attr("height", d => bar_chart_height_no_text - y(d.value))
        .attr("fill", d => color(d.key))
        .on("mouseover",function(_,d){
          d3.selectAll('.node-'+d.token).selectChild('rect').style('stroke', 'black').style('stroke-width', 2)
        })
        .on("mouseleave",function(_,d){
          d3.selectAll('.node-'+d.token).selectChild('rect').style('stroke', 'hsl(180, 1%, 80%)')
        })
      
      span_bar_chart.append("g")
      .selectAll("g")
      .data(this.span_summary)
      .join("g")
        .attr("transform", d => `translate(${span_x(d[0])}, 0)`)
      .selectAll("rect")
      .data(function(d) { return [2,3].map(function(key) { return {key: key, value: d[key], kind: d[1], token:d[0]}; }); })
      .join("rect")
                .attr("x", function(d){
          if(d.kind==0){
            return select_group(d.key) + span_x_subgroup.bandwidth() - min_bandwidth + 0.05
          }
          else{
            // kind = 1 q_only
            if(d.kind == 1 ){
              var c = 0.25
            }
            // kind = 2 ctx_only
            else{
              c = -0.25
            }
            return span_x_subgroup(d.key) + c * span_x.bandwidth() + 0.5*span_x_subgroup.bandwidth() - 0.5*min_bandwidth
          }
        })
        .attr("y", d => y(d.value))
        .attr("width", min_bandwidth)
        .attr("height", d => bar_chart_height_no_text - y(d.value))
        .attr("fill", d => color(d.key))
        .on("mouseover",function(_,d){
          d3.selectAll('.node-'+d.token).selectChild('rect').style('stroke', 'black').style('stroke-width', 2)
        })
        .on("mouseleave",function(_,d){
          d3.selectAll('.node-'+d.token).selectChild('rect').style('stroke', 'hsl(180, 1%, 80%)')
        })
      
      svg.append("text")
          .text("Gold Answers:")
          .attr('x', separator_width*3 + margin.left + q_max_length + ctx_max_length + rank_max_length + span_max_length+2)
          .attr('y', margin.top)
      svg.append("text")
          .text(this.gold_answer)
          .attr('x', separator_width*3 + margin.left + q_max_length + ctx_max_length + rank_max_length + span_max_length+2)
          .attr('y', margin.top + 20)

    },
    drawParagraph(tokens, cell_svg, cell_width, s){

            let Cell_SVGWidth = cell_width;
            let textTokenSize = this.getTokenWidth(tokens, cell_svg, s);
            let textTokenWidths = textTokenSize.textTokenWidths;
            let textTokenHeight = textTokenSize.textTokenHeight;
            let containerWidthFactor = 1;
            let containerWidth = Cell_SVGWidth * containerWidthFactor;
            let GPadding={
                left:0,
                top:0
            };
            let textTokenPadding={
                top: 0, bottom:0,
                left:0, right:0,
            };
            const tokenGap = 2;
            const rowGap = textTokenHeight + textTokenPadding.top + textTokenPadding.bottom + 1;

            // Add tokens
            let tokenGroup = cell_svg.append('g')
                .attr('id', 'token-group')
                .attr('transform', `translate(${GPadding.left + Cell_SVGWidth * (1 - containerWidthFactor) / 2},
                ${GPadding.top})`);

            let nodes = tokenGroup.append('g')
                .attr('class', 'node-group')
                .selectAll('g')
                .data(tokens)
                .join('g')
                
//这边统一用token的位置来做id，方便后续和别的视图link时选择token（否则在第一句和第二句甚至同一句中同样的token多次出现，单独处理会比较麻烦）
//似乎没有必要...可以直接nodes.each(function(_,i){})来处理，见208行
                // .attr('id', function(){
                //     count += 1;
                //     return `node-${count}`
                // })
                .attr('class',function(d){
                  // console.log('node-' + d[0])
                  return 'node-' + d[0]
                });

            // Dynamically change the position of each token node
            // Change the positions of tokens based on their width
            let curPos = {x: 0, y: 0};
            // let tokenNum = Object.keys(textTokenWidths).length;  
            let tokenNum = tokens.length;
            let textTokenPositions = {};

            // Change the position of the text token
            let lineLength = 0; 
            nodes.each(function(_, i) {
                d3.select(this)
                .attr('transform', `translate(${curPos.x}, ${curPos.y})`)
                
                // Record the new position
                textTokenPositions[i] = {x: curPos.x, y: curPos.y};

                // Update the next position
                let curLineLength = curPos.x + textTokenWidths[i] + textTokenPadding.left +
                                    textTokenPadding.right + tokenGap;
                if (i + 1 < tokenNum) {
                curLineLength += textTokenWidths[i + 1];
                }
                else{
                  lineLength = curLineLength;
                }

                // Shift to next row if needed
                if (curLineLength > containerWidth) {
                curPos.y += rowGap;
                curPos.x = 0;
                } else {
                curPos.x = curPos.x + textTokenWidths[i] + textTokenPadding.left + textTokenPadding.right + tokenGap;
                }

            });
            const sentence_color = function (i) {
              if (i == 1) {
                return 7;
              } else if (i == 2) {
                return 8;
              } else if (i == 5) {
                return 9;
              }
              return i;
            };
            nodes.append('rect')
                .attr('y',(_, i) => (16-textTokenHeight[i])/2)
                .attr('width', (_, i) => textTokenWidths[i] + textTokenPadding.left + textTokenPadding.right)
                .attr('height',(_, i) =>  textTokenHeight[i] + textTokenPadding.top + textTokenPadding.bottom)
                .attr('rx', 2)
                // .style('fill', "white")
                .style('fill', d => d3.schemeTableau10[sentence_color(d[2])])
                .style("opacity", 0.3)
                .style('stroke', 'hsl(180, 1%, 80%)');

            nodes.append('text')
                .attr('class', 'text-token-arc')
                .attr('x', textTokenPadding.left)
                .attr('y', textTokenPadding.top + 13)
                .style('pointer-events', 'none')
                // .text(d => d.token);
                .text((d)=>{
                  return d[0]
                })
                .style("font-size", function(d){
                  // if(d[1]>0.02){
                  //   return s(d[1])+"em"
                  // }
                  // else{
                  //   return s(0.02)+"em"
                  // }
                  return s(Math.abs(d[1]))+"em"
                });

            d3.select('#tokensvg').attr('height',document.getElementById("token-group").getBBox().height)
            return lineLength;
    },
    init() {
      console.log("instanceview init");
      const path =
        "http://10.192.9.11:5000/query_word_cloud/" + this.question_selected;
          axios
          .post(path, {
                que_sal_thre: this.que_sal_thre,
                barchart_thre:this.barchart_thre
            })
          .then((res) => {
            this.q_tokens = res.data.q_whole_saliency,
            this.ctx_tokens = res.data.ctx_whole_saliency,
            this.rank_tokens = res.data.rank_whole_saliency,
            this.span_tokens = res.data.span_whole_saliency,
            this.order_result = res.data.order_result,
            this.em_result = res.data.em_result,
            this.has_answer_list = res.data.has_answer_list,
            this.final_prediction = res.data.final_prediction,
            this.retriever_summary = res.data.retriever_summary,
            this.rank_summary = res.data.rank_summary,
            this.span_summary = res.data.span_summary,
            this.gold_answer = res.data.gold_answer;
            this.drawAll();
          })
          .catch((error) => {
            console.error(error);
          });
      },
  },
  beforeMount() {
    this.init();
  },
};
</script>

<style scoped>
#instance-view {
  margin: 0px;
  margin-left: 10px;
  height: 100%;
  /* text-align: center; */
  width: 100%;
  /* overflow: auto; */
}
</style>

