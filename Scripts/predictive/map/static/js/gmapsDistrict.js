function initMap_district() {
    //center the map around Sierra Leone
    var center = {lat: 8.612690, lng: -11.759313};
    
    var district_name = document.title;
    
    //initialize the map with a zoom for Sierra Leone
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: center,
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.SATELLITE
    });
    
    //load in district regions as polygons
    map.data.loadGeoJson('/map/indDistricts/');
    

    
    //format district regions
    map.data.setStyle(
            {
                fillColor: "green",
                strokeColor: "purple"
            });
               
    map.data.setStyle(function(feature) {
        if (feature.getProperty('ADM2_NAME') !== district_name){
            return{
                visible: false,
                fillColor: "black",
                fillOpacity: 1,
                strokeColor: "black"
            };
        } else {
                return{
                        visible: true,
                        fillColor: "black",
                        fillOpacity: 1
                      };
                //var innercoord = feature.getGeometry().get();
                //alert(innercoord);
                //map.data.add({geometry: new google.maps.Data.Polygon([outercoord, innercoord])})
        };
    });

};