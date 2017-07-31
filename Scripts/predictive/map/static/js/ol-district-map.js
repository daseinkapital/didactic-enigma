
    
     var rome = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([12.5, 41.9]))
      });
       
      var vectorSource = new ol.source.Vector([]);
    var iconStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
          color: '#8959A8',
          crossOrigin: 'anonymous',
          src: 'https://openlayers.org/en/v4.2.0/examples/data/dot.png'
        }))
      });
      rome.setStyle(iconStyle);
      
      
      $.ajax({
            
            url : "/map/addcases/",
            data: {"name" : document.title},
            success : function(data) {
                var deathcnfm = [];
                var mark = [];
                var size = [];
                var names = [];
                var zindex = [];
                var count = Object.keys(data).length;
                

                for (var i = 0; i < count; i++){
                        var name = data[i].hospitalName;
                        var lat1 = parseFloat(data[i].lat);
                        var lng1 = parseFloat(data[i].lng);
                        var deaths = parseInt(data[i].deaths);
                        var zval = parseInt(data[i].zval);
                        mark.push([lng1, lat1]);
                        deathcnfm.push(deaths);
                        names.push(name);
                        zindex.push(zval);
                };
                Object.keys(mark).forEach(function(key) {
                console.log(key, mark[key]);
                });
                
                for (i = 0; i < mark.length; i++){
                        var icon = new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
                              color: '#8959A8',
                              crossOrigin: 'anonymous',
                              src: 'https://openlayers.org/en/v4.2.0/examples/data/dot.png',
                              scale: deathcnfm[i]/100
                            }))  ;
                        var newiconStyle = new ol.style.Style({
                            image: icon,
                            zIndex: zindex[i]
                          });                      
                        
                        var feature = new ol.Feature({
                            geometry: new ol.geom.Point(ol.proj.fromLonLat(mark[i]))                        
                        });
        
                    feature.setStyle(newiconStyle);
                    vectorSource.addFeature(feature);

                };
            }
        });
        
            
    var vectorLayer = new ol.layer.Vector({
        source: vectorSource
      });

      var rasterLayer = new ol.layer.Tile({
         source: new ol.source.XYZ({
          attributions: 'Tiles © <a href="https://services.arcgisonline.com/ArcGIS/' +
              'rest/services/World_Topo_Map/MapServer">ArcGIS</a>',
          url: 'https://server.arcgisonline.com/ArcGIS/rest/services/' +
              'World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
        })
      });
      var districtLayer = new ol.layer.Image({
            source: new ol.source.ImageVector({
              source: new ol.source.Vector({
                url: '/map/districts/',
                format: new ol.format.GeoJSON()
              }),

              style: new ol.style.Style({
                fill: new ol.style.Fill({
                  color: 'rgba(255, 255, 255, 0.6)'
                }),
                stroke: new ol.style.Stroke({
                  color: '#319FD3',
                  width: 1
                }),
            })
        }) 
         });
        
                  

      var distView = new ol.View({
          center:  ol.proj.fromLonLat([parseFloat(document.getElementById('lng').text), parseFloat(document.getElementById('lat').text)]),
          zoom: parseFloat(document.getElementById('zoom').text)
      });
                        
      var map = new ol.Map({
        layers: [rasterLayer, vectorLayer, districtLayer],
        
        target: document.getElementById('map'),
        view: distView
       });

// WE NEED TO FIX THE BOUNDS OF ZOOM AND HOW THE GEOJSON DISPLAYS
//    for (i=0; i < features.length; i++) {
//            alert(features[i]);
//            if (features[i].get('ADM2_NAME') === document.title){
//                          map.setView(new ol.View({
//                              center: map.getView().getCenter(),
//                              boundingExtent: features[i].getGeometry().A,
//                              zoom: map.getView().getZoom(),
//                              minZoom: map.getView().getZoom()
//                            })); 
//                        alert('Found'); 
//                    } else {
//                            alert('Not Found');
//                            features[i].style = { display: 'none' };
//                    }
//            };

              
       map.setView(new ol.View({
          center: map.getView().getCenter(),
          extent: map.getView().calculateExtent(map.getSize()),
          zoom: map.getView().getZoom(),
          minZoom: map.getView().getZoom()
        }));             
                                       
                        
        var featureOverlay = new ol.layer.Vector({
        source: new ol.source.Vector(),
        map: map,
        style: new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: '#f00',
            width: 1
          }),
          fill: new ol.style.Fill({
            color: 'rgba(255,0,0,0.1)'
          })
        })
      });

      var highlight;
      var link; 
      
      var displayLinkInfo = function(pixel) {
          var feature = map.forEachFeatureAtPixel(pixel, function(feature) {
          return feature;
        });
         if (feature) {
          link = '/map/region/' + feature.get('ADM2_NAME');
        } else {
          link = 'none';
        } 
         };               
              
              
              
        
    
      
    var displayFeatureInfo = function(pixel) {

       var feature = map.forEachFeatureAtPixel(pixel, function(feature) {
          return feature;
        });
        
       var info = document.getElementById('info');
        if (feature) {
          info.innerHTML = feature.get('ADM2_NAME');
        } else {
          info.innerHTML = 'none';
        } 
            
       

       

        if (feature !== highlight) {
          if (highlight) {
            featureOverlay.getSource().removeFeature(highlight);
          }
          if (feature) {
            featureOverlay.getSource().addFeature(feature);
          }
          highlight = feature;
        }
          };
          
    
      

      map.on('pointermove', function(evt) {
        if (evt.dragging) {
          return;
        }
        var pixel = map.getEventPixel(evt.originalEvent);
        displayFeatureInfo(pixel);
      });

      map.on('click', function(evt) {
        displayFeatureInfo(evt.pixel);
        if(document.getElementById("info").innerHTML != "none") {
        $.ajax({
                              url : "/map/marker/",
                              data : {"name" : document.getElementById("info").innerHTML, "date" : "2014-09-18"},
                              dataType : 'html',
                              success : function (data) {
                                  $("#mySidenav").empty().append(data);
                              }
                        });        

        }
      });   
          
     map.on('dblclick', function(evt) {
        displayLinkInfo(evt.pixel);
        if(link != "none") {
            window.location.href = link;  

        }
      });   
          
       