function initMap_district() {
    //center the map around Sierra Leone
    var center = {lat: 8.612690, lng: -11.759313};
    
    //initialize the map with a zoom for Sierra Leone
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: center,
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.SATELLITE
    });
};