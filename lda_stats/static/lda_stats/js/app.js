$(document).ready(function() {

    // Load General Stats
    $.getJSON( "/lda_stats/general_stats", function( data ) {
        $.each( data, function( key, val ) {
            $("#stats_"+key).html(val);
        });
    });

    // Hot Topics
    $("#hot_topics_interval,#hot_topics_alg").change(function(){
        load_hot_topics();
    });

    //Loads hot topics
    function load_hot_topics(){
        $("#hot_topics_div").html("Lading ...");
        var params = {
                algorithm: $("#hot_topics_alg").val(),
                period: $("#hot_topics_interval").val(),
        }
        $.getJSON( "/lda_stats/hot_topics", params, function( data ) {
            var s = data.join("<BR />\n");
            $("#hot_topics_div").html(s);
        });        
    }

    //Load hot tpoics for the first time with default values
    load_hot_topics();

    //Loads Infulential Items and show them in table
    $.getJSON( "/lda_stats/influential_items", function( data ) {
        var table_data = "";
        counter = 1;
        $.each( data, function( key, val ) {
            tr = "<tr><td>"+counter+"</td><td>"+val["title"]+"</td><td>"+val.count+"<td></tr>";
            table_data = table_data+tr;
            counter += 1;
        });
        $("#influential_items").html(table_data);
    });

    //Influential Words
    $.getJSON( "/lda_stats/influential_words", function( data ) {
        var words = [];
        $.each( data, function(key, item) {
            words.push(item.word+" -- "+item.score);
        });
        $("#influential_words").html(words.join("<BR />\n"));
    });

});
