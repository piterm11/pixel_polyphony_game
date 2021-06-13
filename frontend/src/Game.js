import "./App.css"
import "./Game.css"
import piano from "./graphics/piano.gif"
import flute from "./graphics/flute.gif"
import drum from "./graphics/drum.gif"
import saxophone from "./graphics/saxophone.gif"
import trumpet from "./graphics/trumpet.gif"
import axios from 'axios'
import React, {useState, useEffect} from 'react'

function Game({match}) {
	let notesComponent = []
	var selectedInstrument = ""
	const addNotes = () => {
		for (const [key, value] of Object.entries(notes)) {
			if (key === 'c')
				notesComponent.push(
				<div style={{backgroundColor: value[1], border: 'none'}} className={`note ${key}`}> 
					<span style={{fontWeight: '700', marginBottom: 'auto'}}>{key}</span>
					<span style={{fontWeight: '400', textTransform: 'lowercase'}}>{value[0]}</span>
				</div>)
			else
				notesComponent.push(
					<div style={{backgroundColor: value[1]}} className={`note ${key}`}> 
						<span style={{fontWeight: '700', marginBottom: 'auto'}}>{key}</span>
						<span style={{fontWeight: '400', textTransform: 'lowercase'}}>{value[0]}</span>
					</div>)
		}
	}
	const [time, setTime] = useState(30)
	var clickNotes = {
		'q': 0,
		'w': 1,
		'e': 2,
		'r': 3,
		't': 4,
		'y': 5,
		'u': 6,
		'i': 7,
	}
	useEffect(() =>{
		getData()
		const notes = document.getElementsByClassName("note")
		const xd = [...notes]
		xd.forEach(((note) => {
			note.addEventListener('click', (e) => {
				console.log(selectedInstrument, e.target.className)
			})
		}))
		document.addEventListener('keydown', (e) => {
			if (e.repeat || !(e.key in clickNotes)) return
			console.log(e.key)
			xd[clickNotes[e.key]].classList.add('note-active')
			setTimeout(() => {
				xd[clickNotes[e.key]].classList.remove('note-active')
			}, 200)
		})
		// setInterval(() => {
		// 	setTime(time => time - 1)
		// }, 1000)
	}, [])
	const [lobby, setItem] = useState({
		team: [],
		available_instruments: [],
		player: {}
	})
	const getData = async() => {
		const item = await axios.get(`http://localhost:8000/api/lobby/${match.params.id}/`)
		setItem(item.data)
		console.log(item.data)
		selectedInstrument = item.data.player.instrument
	}

	const single = (element, contain) => {
			if (element === "piano") element = piano
			else if (element === "saxophone") element = saxophone
			else if (element === "drum") element = drum
			else if (element === "flute") element = flute
			else if (element === "trumpet") element = trumpet
			return {
			backgroundImage: `url(${element})`, 
			backgroundRepeat: 'no-repeat', 
			backgroundPosition: 'center',
			backgroundSize: contain ? 'contain' : 'auto',
			width: '100%',
			height: '100%',
			display: 'flex',
			justifyContent: 'center',
			alignItems: 'flex-end'
		}
	}
	const notes = {
		'c': ['Q', '#fb0000'],
		'D': ['W', '#fb6701'],
		'E': ['E', '#fff302'],
		'F': ['R', '#7dfe04'],
		'G': ['T', '#32f2ff'],
		'A': ['Y', '#0d6bff'],
		'H': ['U', '#021aff'],
		'C': ['I', '#6b1aff'],
	}
	let usersComponent = []
	const addUsers = () => {
		lobby.team.forEach((player) => {
			usersComponent.push(<div className="user"><div style={single(player.instrument, false)}>{player.name}</div></div>)
		})
	}
	return (
		<div className="App">
			<div className="App-header">
				<div className="container">
					<div className="timer">00:{time < 10 ? '0' + time : time}</div>
					<div className="username">{lobby.player.name}</div>
					<div className="users">
						{addUsers()}
						{usersComponent}
					</div>
					<div className="playground">
						<div style = {single(lobby.player.instrument, true)}></div>
					</div>
					<div className="keyboard">
						<div className="labels">
							Note:
							<br/>
							<br/>
							<br/>
							Key:
						</div>
						{addNotes()}
						{notesComponent}
					</div>
				</div>
			</div>
		</div>
	);
}

export default Game;
