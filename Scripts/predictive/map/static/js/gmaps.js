var iconSize = 0.5;
function initMap() {        
    var center = {lat: 8.612690, lng: -11.759313};  
    
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: center,
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.HYBRID
      });
    

    map.data.loadGeoJson('/map/districts/');

    $.ajax({
            
            url : "/map/init/",
            success : function(data) {
                var deathcnfm = [];
                var mark = [];
                var count = Object.keys(data).length;
                
                
               
                for (var i = 0; i < count; i++){
                        var lat1 = parseFloat(data[i].lat);
                        var lng1 = parseFloat(data[i].lng);
                        var deaths = parseInt(data[i].deaths);
                        
                        mark.push({lat : lat1, lng : lng1});
                        deathcnfm.push(deaths);
                };
                                  
                for (i = 0; i < mark.length; i++){
                    var iconSize = deathcnfm[i]/50;
                      
                        
                    var icon = {
        
                        path: "M-20,0a20,20 0 1,0 40,0a20,20 0 1,0 -40,0",
                        fillColor: '#FF0000',
                        fillOpacity: .6,
                        anchor: new google.maps.Point(0,0),
                        strokeWeight: 0,
                        scale: iconSize
                    }
                     
           
                     
                    
                
                    var marker = new google.maps.Marker({
                        animation: google.maps.Animation.DROP,
                        position: mark[i],
                        map: map,
                        draggable: false,
                        icon: icon,
                        zIndex : -20
                    });
                    google.maps.event.addDomListener(marker, 'click', function() {
                        map.setCenter(this.getPosition());
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