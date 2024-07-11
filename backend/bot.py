import asyncio
import logging
from fastapi import FastAPI, WebSocket
from dotenv import load_dotenv
import os

# Pipecat and TerifAI components
from pipecat.transports.services.daily import DailyParams, DailyTransport
from pipecat.vad.vad_analyzer import VADParams
from pipecat.vad.silero import SileroVADAnalyzer
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.processors.aggregators.llm_response import LLMUserResponseAggregator
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask

load_dotenv()

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Initialize Deepgram client
deepgram_service = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Set up Daily transport
    transport = DailyTransport(
        room_url=os.getenv("DAILY_ROOM_URL"),
        token=os.getenv("DAILY_TOKEN"),
        user_name="Orator Bot",
        params=DailyParams(
            audio_out_enabled=True,
            vad_enabled=True,
            vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
            vad_audio_passthrough=True,
        ),
    )

    # Set up pipeline
    pipeline = Pipeline([
        transport.input(),
        deepgram_service,
        LLMUserResponseAggregator([]),  # Initialize with empty message history
        transport.output(),
    ])

    task = PipelineTask(
        pipeline,
        PipelineParams(
            allow_interruptions=True,
            enable_metrics=True,
            report_only_initial_ttfb=True,
        ),
    )

    # Event handlers
    @transport.event_handler("on_first_participant_joined")
    async def on_first_participant_joined(transport, participant):
        logging.info(f"Participant joined: {participant['id']}")
        transport.capture_participant_transcription(participant["id"])

    # Run pipeline
    runner = PipelineRunner()
    try:
        await runner.run(task)
    except Exception as e:
        logging.error(f"Error in pipeline: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)