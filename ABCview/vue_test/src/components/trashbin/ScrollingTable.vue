<template>
    <div id = "scrolling-table">
        <table id = "table"/>
    </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import bus from './bus';
export default {
    name: "ScrollingTable",
    created(){
        this.getAll()

    },
    data(){
        return {
            column_name:['index', 'sentence1','sentence2','golden','pred','prob'],
            columns:['index','prob'],
            allData:[],
            dimensions:{'width':810, 'height':142},
            init_index:4
            // first_init:true
            // delete tokens && change the sequence
        }
    },
    methods:{
        getAll(){
        const path = "http://10.192.9.11:5000/query_all"
        axios.get(path)
            .then((res)=>{
            this.allData = res.data
            })
            .then(() => this.drawTable(this.allData,this.dimensions,this.column_name))
            .then(()=>bus.$emit('dispatchsentencetoshow',[this.allData[this.init_index].tokens, this.init_index]))
            .catch((error)=>{
            console.log(error)
            })
        },

        drawTable(data,  dimensions, columns) {
        var probFunc = function(data) { return data.prob; }
        var indexFunc = function(data) { return data.index; }
        var sortprobAscending = function (a, b) { return probFunc(a) - probFunc(b) }
        var sortprobDescending = function (a, b) { return probFunc(b) - probFunc(a) }
        var sortindexAscending = function (a, b) { return indexFunc(a) - indexFunc(b) }
        var sortindexDescending = function (a, b) { return indexFunc(b) - indexFunc(a)}
        var probAscending = true;
        var indexAscending = true;

        var width = dimensions.width + "px";
        var height = dimensions.height + "px";
        var twidth = (dimensions.width - 25) + "px";
        var divHeight = (dimensions.height -20) + "px";

        var outerTable = d3.select("#table").append("table").attr("width", width);

        outerTable.append("tr").append("td")
            .append("table").attr("class", "headerTable").attr("width", twidth)
            .append("tr").selectAll("th").data(columns).enter()
            .append("th").text(function (column) { return column; })
            .attr("class",d => d)
            .on("click", function () {
                // Choose appropriate sorting function.
                if (this.className === columns[5]) {
                    var sort = probAscending ? sortprobAscending : sortprobDescending;
                    probAscending = !probAscending;
                    tbody.selectAll("tr").sort(sort);
                } else if(this.className === columns[0]) {
                    var sort1 = indexAscending ? sortindexAscending : sortindexDescending
                    indexAscending = !indexAscending;
                    tbody.selectAll("tr").sort(sort1);
                }
            });

        var inner = outerTable.append("tr").append("td")
            .append("div").attr("class", "scroll").attr("width", width).attr("style", "height:" + divHeight + ";")
            .append("table").attr("class", "bodyTable").attr("border", 1).attr("width", twidth).attr("height", height)
            .attr("style", "table-layout:fixed");

        var tbody = inner.append("tbody");
        // Create a row for each object in the data and perform an intial sort.
        var rows = tbody.selectAll("tr").data(data).enter().append("tr").sort(sortindexAscending);

        // Create a cell in each row for each column
        rows.selectAll("td")
            .data(function (d) {
                return columns.map(function (column) {
                    return { column: column, index: indexFunc(d), sentence1:d.sentence1, sentence2:d.sentence2, golden:d.golden,
                             pred:d.pred, prob: probFunc(d), tokens: d.tokens};
                });
            }).enter().append("td")
            .text(function (d) {
                if (d.column === columns[0]) return d.index+1 ;
                else if (d.column === columns[1]) return d.sentence1;
                else if (d.column === columns[2]) return d.sentence2;
                else if (d.column === columns[3]) return d.golden;
                else if (d.column === columns[4]) return d.pred;
                else if (d.column === columns[5]) return d.prob;
            })
            .attr("class",d => d.column)
            .on("dblclick",function(){
                bus.$emit("dispatchsentencetoshow",[this.__data__.tokens, this.__data__.index])//传双参数，sentence的tokens和index
            })


            // if(this.first_init==true){
            //     bus.$emit('dispatchsentencetoshow',)
            // }
        },
    }
}
</script>

<style>
#scrolling-table{
    display: flex;
}
#table {
	width: 500px;
	height: 160px;
}

.bodyTable td {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}

.bodyTable tr {
    height: 40px;
}

.bodyTable tr:hover {
    background-color:grey;
}

.headerTable th:hover {
    background-color:grey;
}

.scroll {
    overflow: auto;
}

.index  {
    width: 10%
}

.sentence1  {
    width: 30%
}

.sentence2  {
    width: 30%
}
.golden  {
    width: 10%
}

.pred {
    width: 10%
}

.prob  {
    width: 10%
}
</style>