import * as React from 'react';
import {Link} from 'react-router';

import {
  interaction, layer, custom, control, //name spaces
  Interactions, Overlays, Controls,     //group
  Map, Layers, Overlay, Util    //objects
} from "react-openlayers";    

export class App extends React.Component<any, any> {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div className="menu">
        <h1>React OpenLayers</h1>
        <ul className="groups" role="nav">
          <li><Link to="/layers">Layers</Link></li>
          <li><Link to="/controls">Controls</Link></li>
          <li><Link to="/overlays">Overlays</Link></li>
          <li><Link to="/interactions">Interactions</Link></li>
          <li><Link to="/custom">Custom Examples</Link></li>
        </ul>

        {this.props.children}
      </div>
    );
  }
}