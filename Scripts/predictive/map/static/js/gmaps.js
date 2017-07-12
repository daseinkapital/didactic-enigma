function initMap() {
    var points = [{lat:10,lng:-13}];
    var center = {lat: 8.612690, lng: -11.759313};
    
    
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: center,
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.HYBRID
      });
        
    var markerDict = [];
    
    for (i = 0; i < points.length; i++){
        var mark = points[i];
        markerDict.push({
            key: i,
            value: mark
        });
        var marker = new google.maps.Marker({
            animation: google.maps.Animation.DROP,
            position: mark,
             icon: {
             path: google.maps.SymbolPath.CIRCLE,
              scale: 10
    },
            map: map,
        });
        google.maps.event.addDomListener(marker, 'click', function() {
            map.setCenter(this.getPosition());
            var date = $('#date').val();
            $.ajax({
                  url : "/map/marker/",
                  data : {"lat" : this.getPosition().lat(), "lng" : this.getPosition().lng(), "date" : date},
                  dataType : 'html',
                  success : function (data) {
                          $("#mySidenav").empty().append(data);}
                  });
          document.getElementById("mySidenav").style.width = "300px";
          });
      };

        
}
