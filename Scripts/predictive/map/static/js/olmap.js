
  
  
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
                        mark.push([lat1, lng1]);
                        deathcnfm.push(deaths);
                        size.push(mark_size);
                        names.push(name);
                };

                
                for (i = 0; i < mark.length; i++){
                        var link = '/map/region/' + names[i];
                    
                        var feature = new ol.Feature({
                        geometry: new ol.geom.Point(mark[i]),

                        
                    });
                    
                    feature.setStyle(iconStyle);
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
              'World_Imagery/MapServer/tile/{z}/{y}/{x}'
        })
      });
      var feature = vectorSource.getFeatures();
      
      var districtLayer = new ol.layer.Image({
            source: new ol.source.ImageVector({
              source: new ol.source.Vector({
                url: '/map/districts/',
                format: new ol.format.GeoJSON()
              }),

              style: function(feature, res){

                      return  feature.get('ADM2_NAME') == "Kambia" || feature.get('ADM2_NAME')== "Koinadugu" || feature.get('ADM2_NAME')== "Western Area Rural" || feature.get('ADM2_NAME')== "Kono" || feature.get('ADM2_NAME')== "Bonthe" || feature.get('ADM2_NAME')== "Kalihun"? 

                              new ol.style.Style({
                                  stroke: new ol.style.Stroke({
                                  color: '#319FD3',
                                  width: 1
                                }),
                                  fill: new ol.style.Fill({

                                    color: 'rgba(255,255,0, 0.7)'
                                })
                              }) :
                      
                              feature.get('ADM2_NAME') == "Pujehun" || feature.get('ADM2_NAME')== "Tonkolli" || feature.get('ADM2_NAME')== "Kenema" || feature.get('ADM2_NAME')== "Bo" ? 

                              new ol.style.Style({
                                  stroke: new ol.style.Stroke({
                                  color: '#319FD3',
                                  width: 1
                                }),
                                  fill: new ol.style.Fill({

                                    color: 'rgba(255,0,0,0.7)'
                                })
                              }) :
                              new ol.style.Style({
                                  stroke: new ol.style.Stroke({
                                  color: '#319FD3',
                                  width: 1
                                }),
                                  fill: new ol.style.Fill({
                                    color: 'rgba(255, 153, 0, 0.7)'
                                })
                              });
          
        }}) 
         });
                        
       var sierraView = new ol.View({
          center:  [-1354603.7697028217, 950826.8771984349],
          zoom: 8.206381747585729
        });
        
                        
    var circlesource = new ol.source.Vector({wrapX: false});

     var Circlevector = new ol.layer.Vector({
        source: circlesource
      });   
                        
                        
      var map = new ol.Map({
        layers: [rasterLayer, vectorLayer, districtLayer, Circlevector],
        
        target: document.getElementById('mapol'),
        view: sierraView
      
       });

                        
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
                document.getElementById("name").innerHTML = document.getElementById("info").innerHTML;
                if(document.getElementById("active").innerHTML != false){
        $.ajax({
                              url : "/map/reports/",
                    
                              data : {"name" : document.getElementById("name").innerHTML, "date" : "2017-07-27"},
                              dataType: "html",
                              success : function (data) {
                                  side1Width =$('#slide-1').css("transform");
                                 
                                  if (side1Width === "matrix(1, 0, 0, 1, 0, 0)"){

                                  
                                  $("#slide-1").empty().append(data);
                                  }
                                  else
                                  {
                            
                                   $("#slide-2").empty().append(data);
                                          }
                              }
                        }); 
          
        };
        };
      });   
          
     map.on('dblclick', function(evt) {
        displayLinkInfo(evt.pixel);
        if(link != "none") {
            window.location.href = link;  

        }
      });  
          
    
        
    var typeSelect = document.getElementById('type');

     var draw; // global so we can remove it later
      function addInteraction() {
        var value = typeSelect.innerHTML;
        if (value == 'Circle') {
          draw = new ol.interaction.Draw({
            source: circlesource,
            type: "Circle"
          });
          map.addInteraction(draw);
        
          
        }
      }
    
              
   $('#type').change(function(){
        map.removeInteraction(draw);
        addInteraction();
        circlesource.clear();
       
      
});

      addInteraction();
          
     
          
       