$.ajax({
    url : "/demo/graph/",
    success : function(data) {
            $("#chart-div").empty();
            $("#chart-div").html(data);
        }
    });