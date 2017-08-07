 		var FIRST_TOGGLE = true;
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
                    if(ACTIVE){
                          $('#sideNavButton2').sideNav('show');
                          $('#sideNavButton2').sideNav('hide');
                        } else {
                          $('#sideNavButton1').sideNav('show');
                          $('#sideNavButton1').sideNav('hide');
                                }
                          FIRST_TOGGLE = true;
                          ACTIVE = true;
						});
					});	

$("#link-reports").click(function(){
  $.ajax({
                              url : "/map/marker/",
                              data : {"name" : "Bo", "date" : "2017-07-27"},
                              dataType : 'html',
                              success : function (data) {
                                    if(!ACTIVE){
                                  $("#slide-1").empty().append(data);
                              }
                                else {
                                        
                                     $("#slide-2").empty().append(data);    
                                        
                                        }
                                    }
                        });        

        
      }); 

$("#activatehello").click(function(){
  $.ajax({
                              url : "/map/hellotest/",
                              dataType : 'html',
                              success : function (data) {
                                    if(!ACTIVE){
                                  $("#slide-1").empty().append(data);
                              }
                                else {
                                        
                                     $("#slide-2").empty().append(data);    
                                        
                                        }
                                    }
                        });        

        
      }); 

$("#activatehosp").click(function(){
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
                                    }
                        });        

        
      });   



