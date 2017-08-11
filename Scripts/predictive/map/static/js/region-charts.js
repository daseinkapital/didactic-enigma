$.ajax({
    url : "/map/dist_charts/",
    data : { 'name' : document.title },
    success : function(data) {
            $("#chart-div").html(data);
        }
    });