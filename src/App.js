import React, { useState } from 'react';
import './App.css';
import { generateMidi, downloadMidi, playMidi } from './midiService'; // You will create this service
import MidiVisualizer from './midiVisualizer';



function App() {
  const [midiPath, setMidiPath] = useState(null);

  const handleGenerate = () => {
    const midi = generateMidi(); // This will now return the path
    setMidiPath(midi);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>MIDI Generator</h1>
        <button onClick={handleGenerate}>Generate</button>
        {midiPath && <MidiVisualizer midiPath={midiPath} />} 
      </header>
      {midiPath && (
        <div className="midi-container">
          
          <button onClick={() => playMidi(midiPath)}>Play</button>
          <button onClick={() => downloadMidi(midiPath)}>Download</button>
           
    </div>
      )}
    </div>
  );
}

export default App;
