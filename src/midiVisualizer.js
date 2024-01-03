import React, { useEffect, useRef } from 'react';
import { Midi } from '@tonejs/midi';

const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 400;
const NOTE_HEIGHT = 5; // Height of each note rectangle
const PADDING = 10; // Padding in pixels



const MidiVisualizer = ({ midiPath }) => {
    const canvasRef = useRef(null);
    useEffect(() => {
        const drawMidi = async () => {
            try {
                const response = await fetch(midiPath);
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const arrayBuffer = await response.arrayBuffer();
                const midi = new Midi(arrayBuffer);
        
                const canvas = canvasRef.current;
                const ctx = canvas.getContext('2d');

                // Clear the canvas
                ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

                // Adjusted scale factors to account for padding
                const endTime = midi.duration;
                const scaleX = (CANVAS_WIDTH - 2 * PADDING) / endTime;
                const scaleY = (CANVAS_HEIGHT - 2 * PADDING) / 128;

                // Draw notes with padding
                midi.tracks.forEach(track => {
                    track.notes.forEach(note => {
                        const x = PADDING + note.time * scaleX;
                        const y = PADDING + CANVAS_HEIGHT - (note.midi * scaleY) - NOTE_HEIGHT;
                        const width = note.duration * scaleX;
                        const height = NOTE_HEIGHT;

                        ctx.fillStyle = 'white';
                        ctx.fillRect(x, y, width, height);

                        ctx.strokeStyle = 'black';
                        ctx.strokeRect(x, y, width, height);
                    });
                });
            } catch (e) {
                console.error('Error fetching or parsing MIDI file:', e);
            }
        };
        

        drawMidi();
    }, [midiPath]);

    return (
    <div className="canvas-container">
    <canvas ref={canvasRef} width="800" height="400"></canvas>
    </div>
  )
};


export default MidiVisualizer;
