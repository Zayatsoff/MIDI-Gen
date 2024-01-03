
import MidiPlayer from 'midi-player-js';
import { Midi } from '@tonejs/midi';

// This is a placeholder. Integrate with AI model for actual MIDI generation.
export const generateMidi = () => {
    // Generate MIDI data

    return 'http://localhost:3000/sample_midi.mid' ; // Placeholder for MIDI data
  };
  
  export const downloadMidi = (midiBlob) => {
    const url = URL.createObjectURL(midiBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generated-midi.mid';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
  

// Function to play a MIDI Blob
export const playMidi = async (midiUrl) => {
    try {
        const response = await fetch(midiUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const midiBlob = await response.blob();

        // Use FileReader to read the Blob
        const reader = new FileReader();
        reader.onload = function(e) {
            var data = e.target.result;
            // Assuming midiPlayer can play from a data URI
            var player = new MidiPlayer.Player(function(event) {
                // Handle playback events here
            });

            player.loadDataUri(data);
            player.play();
        };
        reader.readAsDataURL(midiBlob);
    } catch (e) {
        console.error('Error fetching or playing MIDI file:', e);
    }
};


