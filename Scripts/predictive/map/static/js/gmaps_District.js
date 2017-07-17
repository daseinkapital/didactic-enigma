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
    
    $.ajax({
    url : '/map/init_dist/',
    data : {'name' : document.title},
    success : function(data) {
        map.setZoom(data.zoom);
        map.setCenter({lat : parseFloat(data.lat), lng : (parseFloat(data.lng) - 0.5)})
        }
    });
    
    //load in district regions as polygons
    map.data.loadGeoJson('/map/indDistricts/');
    

    map.data.setStyle(function(feature) {
        if (feature.getProperty('ADM2_NAME') !== district_name){
            return{
                visible: false,
            };
        } else {
                return{
                        visible: true,
                        fillColor: "gray",
                        fillOpacity: 0.7,
                        strokeColor: "gray",
                        strokeWeight: 0
                      };
        };
    });
    

};