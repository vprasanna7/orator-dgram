import React, { useEffect, useState, useRef } from 'react'
import DailyIframe from '@daily-co/daily-js'

const Transcript: React.FC = () => {
  const [transcript, setTranscript] = useState<string>('')
  const [isRecording, setIsRecording] = useState(false)
  const callFrameRef = useRef<DailyIframe.DailyCall | null>(null)

  useEffect(() => {
    callFrameRef.current = DailyIframe.createFrame({
      showLeaveButton: true,
      iframeStyle: {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '100%',
        height: '100%',
      },
    })

    callFrameRef.current.join({ url: import.meta.env.VITE_DAILY_ROOM_URL as string })

    return () => {
      callFrameRef.current?.destroy()
    }
  }, [])

  useEffect(() => {
    if (isRecording) {
      callFrameRef.current?.startRecording()
    } else {
      callFrameRef.current?.stopRecording()
    }
  }, [isRecording])

  const handleToggleRecording = () => {
    setIsRecording(!isRecording)
  }

  return (
    <div>
      <button onClick={handleToggleRecording}>
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
      <div>{transcript}</div>
    </div>
  )
}

export default Transcript