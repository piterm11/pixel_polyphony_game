import "./App.css";
import "./Lobby.css";
import axios from 'axios'
import React, {useState, useEffect} from 'react'
function Lobby({match}) {
	var dataComponent = [];

	useEffect(() =>{
		getData()
	}, [])
	const [item, setItem] = useState({})
	const getData = async() => {
		const item = await axios.get(`http://localhost:8000/api/lobby/${match.params.id}/`)
		setItem(item.data)
		console.log(item.data)
	}
	return (
		<div className="App">
			<div className="App-header">
				<div className="container">
					<div className="instruments">
						Lobby id: {item.code}
					</div>
					<div className="users">
						Users:
						
						{item.team.forEach(function (el) {
								dataComponent.push(<li style={{listStyleType: "none", paddingLeft: "20px"}}> {el.name} </li>)
							})}
						{dataComponent}
					</div>
					<div className="ready">
						{item.confirmed_players} / {item.all_players}
						<span style={{display: "block", position: "absolute", bottom: "30px", left: "30px", fontSize: "120px"}}>Ready</span>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Lobby;
