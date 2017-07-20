var React = require('react')
var ReactDOM = require('react-dom')
var Hello = require('./app')
var Search = require('./testing')
import Calendar from './date-range-picker'


$(document).ready(function () {
ReactDOM.render(<Hello />, document.getElementById('react-app'))
ReactDOM.render(<Search />, document.getElementById('testing'))
ReactDOM.render(<Calendar />, document.getElementById('Calendar'))

});




