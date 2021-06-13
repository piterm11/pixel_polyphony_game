import React from 'react'
import "./App.css";
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import Home from './Home';
import Join from './Join';
import Lobby from './Lobby';
import Game from './Game';
function App() {
    return (
        <Router>
            <Switch>
                <Route exact path="/" component= {Home} />
                <Route exact path="/join" component = {Join}/>
                <Route exact path="/lobby/:id" component = {Lobby}/>
                <Route exact path="/game/:id" component = {Game}/>
            </Switch>
        </Router>
    );
}

export default App;
