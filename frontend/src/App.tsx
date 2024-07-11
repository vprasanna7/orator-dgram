import React, { useState, useRef, useEffect } from 'react';
import './App.css'; // We'll create this file for styling

const App: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      socketRef.current = new WebSocket('wss://api.deepgram.com/v1/listen', [
        'token',
        import.meta.env.VITE_DEEPGRAM_API_KEY as string,
      ]);

      socketRef.current.onopen = () => {
        console.log('WebSocket connection established');
        mediaRecorderRef.current!.start(100);
      };

      socketRef.current.onmessage = (event) => {
        const result = JSON.parse(event.data);
        if (result.channel && result.channel.alternatives && result.channel.alternatives[0]) {
          setTranscript((prev) => prev + result.channel.alternatives[0].transcript + ' ');
        }
      };

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0 && socketRef.current?.readyState === WebSocket.OPEN) {
          socketRef.current.send(event.data);
        }
      };

      setIsRecording(true);
      setError(null);
    } catch (error) {
      console.error('Error starting recording:', error);
      setError('Could not access microphone. Please ensure you have granted the necessary permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
    if (socketRef.current) {
      socketRef.current.close();
    }
    setIsRecording(false);
  };

  useEffect(() => {
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  return (
    <div className="app-container">
      <h1>Orator Meeting Assistant</h1>
      <div className="controls">
        <button 
          className={`record-button ${isRecording ? 'stop' : 'start'}`}
          onClick={isRecording ? stopRecording : startRecording}
        >
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="transcript-container">
        <h2>Transcript:</h2>
        <p className="transcript">{transcript}</p>
      </div>
    </div>
  );
};

export default App;