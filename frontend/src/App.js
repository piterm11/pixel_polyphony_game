import React from 'react'
import "./App.css";
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import Home from './Home';
import Join from './Join';
import Lobby from './Lobby';
function App() {
    return (
        <Router>
            <Switch>
                <Route exact path="/" component= {Home} />
                <Route exact path="/join" component = {Join}/>
                <Route exact path="/lobby" component = {Lobby}/>
            </Switch>
        </Router>
    );
}

export default App;
