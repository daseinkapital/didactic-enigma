import React from 'react';
import DatetimeRangePicker from 'react-bootstrap-datetimerangepicker';
import moment from 'moment';
var PropTypes = require('prop-types'); 



import {
  Button,
} from 'react-bootstrap';

class DateRangePicker extends React.Component {

  constructor(props) {
    super(props);

    this.handleApply = this.handleApply.bind(this);

    this.state = {
      startDate: moment().subtract(29, 'days'),
      endDate: moment(),
      ranges: {
        'Today': [moment(), moment()],
        'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Last 7 Days': [moment().subtract(6, 'days'), moment()],
        'Last 30 Days': [moment().subtract(29, 'days'), moment()],
        'This Month': [moment().startOf('month'), moment().endOf('month')],
        'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
      },
    };
  }

    
    
  handleApply(event, picker) {
    this.setState({
      startDate: picker.startDate,
      endDate: picker.endDate,
    });
      var start = this.state.startDate.format('YYYY-MM-DD').toString();
      var end = this.state.endDate.format('YYYY-MM-DD').toString();
      $.ajax({
                              url : "/map/changedate/",
                              data : {"startdate" : start, "enddate" : end},
                    
                              success : function (data) {
                                  vectorSource.clear();
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
                                    geometry: new ol.geom.Point(ol.proj.fromLonLat(mark[i])),
            
                                    
                                });
                                
                                feature.setStyle(iconStyle);
                                vectorSource.addFeature(feature);
            
                            };
                             Object.keys(vectorSource).forEach(function(key) {
                            console.log(key, vectorSource[key]);
                            map.render();
                            });               
                                            
                     }
                        });      
  }
    

  render() {
    let start = this.state.startDate.format('MMM DD, YYYY');
    let end = this.state.endDate.format('MMM DD, YYYY');
    let label = start + ' - ' + end;
    if (start === end) {
      label = start;
    }

    return (
      <div className="form-group">
        <label className="control-label col-md-3">Date Range Picker</label>
        <div className="col-md-4">
          <DatetimeRangePicker
            startDate={this.state.startDate}
            endDate={this.state.endDate}
            onApply={this.handleApply}
          >
            <div className="input-group">
              <input type="text" className="form-control" defaultValue={label}/>
                <span className="input-group-btn">
                    <Button className="default date-range-toggle">
                      <i className="fa fa-calendar"/>
                    </Button>
                </span>
            </div>
          </DatetimeRangePicker>
        </div>
      </div>
    );
  }

}

export default DateRangePicker;