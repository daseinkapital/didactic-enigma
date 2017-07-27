function initMap() {
    //center the map in the US
//    var center = {lat:35.0078 , lng: -97.0929};
//    var zoom = 4;    
    
    //center the map around Sierra Leone  
    var new_center = {lat: 8.612690, lng: -10.95635};
    var new_zoom = 8;
    
    
    //initialize the map with a zoom for Sierra Leone
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: new_zoom,
        center: new_center,
        disableDefaultUI: false,
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
        
//    map.setOptions({
//            draggable: false,
//            scrollwheel: false,
//            disableDoubleClickZoom: true
//            });
    
//    setTimeout(function(){
//            map.panTo(new_center)
//            for (i = zoom; i < new_zoom; i++){
//                setTimeout(function(){map.setZoom(i)},1000);
//                };},1000); 
        
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
            
            url : "/map/init_main/",
            success : function(data) {
                var deathcnfm = [];
                var mark = [];
                var size = [];
                var names = [];

                var count = Object.keys(data).length;
                
                
               
                for (var i = 0; i < count; i++){
                        var name = data[i].name;
                        var lat1 = parseFloat(data[i].lat);
                        var lng1 = parseFloat(data[i].lng);
                        var deaths = parseInt(data[i].deaths); 
                        var mark_size = parseInt(data[i].size);
                        mark.push({lat : lat1, lng : lng1});
                        deathcnfm.push(deaths);
                        size.push(mark_size);
                        names.push(name);
                };
                                  
                for (i = 0; i < mark.length; i++){
                        
                    var link = '/map/region/' + names[i]

                    var iconSize = size[i];
                      
                    var icon = {
        
                        path: "M-20,0a20,20 0 1,0 40,0a20,20 0 1,0 -40,0",
                        fillColor: '#FF0000',
                        fillOpacity: .6,
                        anchor: new google.maps.Point(0,0),
                        strokeWeight: 0,
                        scale: iconSize,
                        
                        
                    }
                
                    var marker = new google.maps.Marker({
                        animation: google.maps.Animation.DROP,
                        position: mark[i],
                        map: map,
                        draggable: false,
                        icon: icon,
                        zIndex : -20,
                        title: link
                    });
                    google.maps.event.addDomListener(marker, 'click', function() {
                        $.ajax({
                              url : "/map/marker/",
                              data : {"lat" : this.getPosition().lat(), "lng" : this.getPosition().lng(), "date" : "2014-09-18"},
                              dataType : 'html',
                              success : function (data) {
                                  $("#mySidenav").empty().append(data);
                              }
                        });
                    });
                    google.maps.event.addDomListener(marker, 'dblclick', function() {
                        window.location.href = this.title;
                    });
                };
            }
    });
}