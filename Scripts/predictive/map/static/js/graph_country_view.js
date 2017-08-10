$.ajax({
    url : "/map/country_charts/",
    success : function(data) {
            $("#chart-div").html(data);
        }
    });