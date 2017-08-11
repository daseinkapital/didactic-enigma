 		var FIRST_TOGGLE = true;

      var report_status = document.getElementById('active');
        

      var ACTIVE = true;
				$(document).ready(function(){
                        
					$('#sideNavButton1').sideNav({
                  edge: 'left', 
                  closeOnClick: false
                  });
                $('#sideNavButton2').sideNav({
                  edge: 'left', 
                  closeOnClick: false
                  });


            
             	$(".nav-toggler").click(function(){
                         if (FIRST_TOGGLE){
                            $('#sideNavButton1').sideNav('show');
                            FIRST_TOGGLE = false;
                            ACTIVE = false;
                        } else {
                            if (ACTIVE) {
                           $('#sideNavButton1').sideNav('show');
                           $('#sideNavButton1').sideNav('hide');
                          $('#sideNavButton2').sideNav('hide');
                          $('#sideNavButton2').sideNav('show');
                          ACTIVE = false;
                                    } else {
                           $('#sideNavButton1').sideNav('hide');
                            $('#sideNavButton1').sideNav('show');
                          $('#sideNavButton2').sideNav('show');
                          $('#sideNavButton2').sideNav('hide');
                          ACTIVE = true;
                          }
						}
					});	



             	$(".exit-btn").click(function(){
                    side1Width =$('#slide-1').css("transform")
                    side2Width =$('#slide-2').css("transform")
                    if(side1Width == "matrix(1, 0, 0, 1, 0, 0)" || side2Width == "matrix(1, 0, 0, 1, 0, 0)"){

                        if(ACTIVE){
                              $('#sideNavButton2').sideNav('show');
                              $('#sideNavButton2').sideNav('hide');
                            } else {
                              $('#sideNavButton1').sideNav('show');
                              $('#sideNavButton1').sideNav('hide');
                                    }
                              FIRST_TOGGLE = true;
                              ACTIVE = true;
                              report_status.innerHTML= false;
    						}
    					});
                            });	



$("#link-alerts").click(function(){
  $.ajax({
                                url : "/map/marker/",
                              dataType : 'html',
                              success : function (data) {
                                    if(!ACTIVE){
                                  $("#slide-1").empty().append(data);
                              }
                                else {
                                        
                                     $("#slide-2").empty().append(data);    
                                        
                                        }

                                 report_status.innerHTML= false;


                                    }
                        });        

        
      }); 

$("#link-download").click(function(){
  $.ajax({
                              url : "/map/downloads/",
                              dataType : 'html',
                              success : function (data) {
                                    if(!ACTIVE){
                                  $("#slide-1").empty().append(data);
                              }
                                else {
                                        
                                     $("#slide-2").empty().append(data);    
                                        
                                        }

                                 report_status.innerHTML= false;

                                    }
                        });        

        
      }); 

$("#link-reports").click(function(){
  $.ajax({
                              url : "/map/hosp_overview/",
                              dataType : 'html',
                              success : function (data) {
                                    if(!ACTIVE){
                                  $("#slide-1").empty().append(data);
                              }
                                else {
                                        
                                     $("#slide-2").empty().append(data);    
                                        
                                        }

                                report_status.innerHTML= true;

                                    }
                        });        

        

      });  

     

$("#createAlert").click(function(){
     
        type.innerHTML='Circle';
        $('#type').change();
        
      });   

$("#sendAlert").click(function(){
     
        type.innerHTML='None';
        $('#type').change();
        alert("Alert Sent");
        
        
      });


         



