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
	var gameID = 41
	const sounds = {
		piano: {
			note_c: 'sounds/piano/piano0.mp3',
			note_D: 'sounds/piano/piano1.mp3',
			note_E: 'sounds/piano/piano2.mp3',
			note_F: 'sounds/piano/piano3.mp3',
			note_G: 'sounds/piano/piano4.mp3',
			note_A: 'sounds/piano/piano5.mp3',
			note_H: 'sounds/piano/piano6.mp3',
			note_C: 'sounds/piano/piano7.mp3'
		},
		drum: {
			note_c: 'sounds/drum/drum0.mp3',
			note_D: 'sounds/drum/drum1.mp3',
			note_E: 'sounds/drum/drum2.mp3',
			note_F: 'sounds/drum/drum3.mp3',
			note_G: 'sounds/drum/drum4.mp3',
			note_A: 'sounds/drum/drum5.mp3',
			note_H: 'sounds/drum/drum6.mp3',
			note_C: 'sounds/drum/drum7.mp3'
		},
		saxophone: {
			note_c: 'sounds/saxophone/saxophone0.mp3',
			note_D: 'sounds/saxophone/saxophone1.mp3',
			note_E: 'sounds/saxophone/saxophone2.mp3',
			note_F: 'sounds/saxophone/saxophone3.mp3',
			note_G: 'sounds/saxophone/saxophone4.mp3',
			note_A: 'sounds/saxophone/saxophone5.mp3',
			note_H: 'sounds/saxophone/saxophone6.mp3',
			note_C: 'sounds/saxophone/saxophone7.mp3'
		},
		flute: {
			note_c: 'sounds/flute/flute0.mp3',
			note_D: 'sounds/flute/flute1.mp3',
			note_E: 'sounds/flute/flute2.mp3',
			note_F: 'sounds/flute/flute3.mp3',
			note_G: 'sounds/flute/flute4.mp3',
			note_A: 'sounds/flute/flute5.mp3',
			note_H: 'sounds/flute/flute6.mp3',
			note_C: 'sounds/flute/flute7.mp3'
		},
		trumpet: {
			note_c: 'sounds/trumpet/trumpet0.mp3',
			note_D: 'sounds/trumpet/trumpet1.mp3',
			note_E: 'sounds/trumpet/trumpet2.mp3',
			note_F: 'sounds/trumpet/trumpet3.mp3',
			note_G: 'sounds/trumpet/trumpet4.mp3',
			note_A: 'sounds/trumpet/trumpet5.mp3',
			note_H: 'sounds/trumpet/trumpet6.mp3',
			note_C: 'sounds/trumpet/trumpet7.mp3'
		}
	}


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
	const [time, setTime] = useState(59)
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
		console.log(gameID)
		const socket = new WebSocket(`ws://localhost:8000/api/hit/${gameID}/`)
		socket.onopen = () => {
			console.log("Hello from websocket")
		}
		const notes = document.getElementsByClassName("note")
		const notesArray = [...notes]
		notesArray.forEach(((note) => {
			note.addEventListener('click', (e) => {
				console.log(selectedInstrument, e.target.className)
			})
		}))
		document.addEventListener('keydown', (e) => {
			if (e.repeat || !(e.key in clickNotes)) return
			notesArray[clickNotes[e.key]].classList.add('note-active')
			setTimeout(() => {
				notesArray[clickNotes[e.key]].classList.remove('note-active')
				console.log(selectedInstrument, notesArray[clickNotes[e.key]].className)
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
		gameID = item.data.game_number
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
			alignItems: 'flex-end',
			imageRendering: 'pixelated'
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
