import os
from dataclasses import dataclass
from pipecat.frames.frames import Frame, AudioRawFrame, TranscriptionFrame
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from deepgram import Deepgram
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

class TranscriptionLogger(FrameProcessor):
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, TranscriptionFrame):
            logger.debug(f"Transcription: {frame.text}")

        await self.push_frame(frame)

class DeepgramTerrify(FrameProcessor):
    def __init__(self):
        super().__init__()
        self.deepgram = Deepgram(DEEPGRAM_API_KEY)

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        if isinstance(frame, AudioRawFrame):
            try:
                source = {'buffer': frame.audio, 'mimetype': 'audio/raw'}
                response = await self.deepgram.transcription.prerecorded(source, {
                    'smart_format': True,
                    'model': 'general',
                    'language': 'en-US'
                })
                
                transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                
                if transcript:
                    transcription_frame = TranscriptionFrame(text=transcript)
                    await self.push_frame(transcription_frame, direction)
            except Exception as e:
                logger.error(f"Error in Deepgram transcription: {e}")

        await self.push_frame(frame, direction)