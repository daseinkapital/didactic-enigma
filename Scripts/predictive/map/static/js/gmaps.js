function initMap() {
    //center the map around Sierra Leone
    var center = {lat: 8.612690, lng: -11.759313};  
    
    //initialize the map with a zoom for Sierra Leone
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: center,
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.SATELLITE
      });

    //load in district regions as polygons
    map.data.loadGeoJson('/map/districts/');
    
    //format district regions
    map.data.setStyle(
            {
                fillColor: "green",
                strokeColor: "purple"
            });
    
    map.data.addListener('mouseover', function(event){
            map.data.revertStyle();
            map.data.overrideStyle(event.feature, {
                    fillColor: "yellow"
                    });
        });
        
    map.data.addListener('mouseout', function(event){
            map.data.revertStyle();
        });
        

    $.ajax({
            url : "/map/init/",
            success : function(data) {
                var mark = [];
                for (var i = 0; i < data.length; i++){
                        var lat1 = parseFloat(data[i].fields.latitude);
                        var lng1 = parseFloat(data[i].fields.longitude);

                        mark.push({lat : lat1, lng : lng1});
                };
                        
                        
                for (i = 0; i < mark.length; i++){
                    var marker = new google.maps.Marker({
                        animation: google.maps.Animation.DROP,
                        position: mark[i],
                        map: map,
                    });
                    google.maps.event.addDomListener(marker, 'click', function() {
                        map.setCenter(this.getPosition());
                        map.setZoom(10); 
                        $.ajax({
                              url : "/map/marker/",
                              data : {"lat" : this.getPosition().lat(), "lng" : this.getPosition().lng(), "date" : "2014-09-18"},
                              dataType : 'html',
                              success : function (data) {
                                  $("#mySidenav").empty().append(data);
                              }
                        });
                    });
                };
            }
    });
}