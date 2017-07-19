var React = require('react')
var ReactDOM = require('react-dom')
var App = require('./app')
var Test = require('./testing')


ReactDOM.render(<App />, document.getElementById('react-app'))
ReactDOM.render(<Test />, document.getElementById('testing'))

