from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapterSettings, BotFrameworkAdapter, TurnContext
from botbuilder.schema import Activity
from bot import KnowledgeBot
from config import Config
import asyncio

app = Flask(__name__)

config = Config()
settings = BotFrameworkAdapterSettings(config.microsoft_app_id, config.microsoft_app_password)
adapter = BotFrameworkAdapter(settings)
bot = KnowledgeBot(config)

loop = asyncio.get_event_loop()

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)

    async def call_bot():
        await adapter.process_activity(activity, "", lambda turn_context: bot.on_turn(turn_context))

    task = loop.create_task(call_bot())
    loop.run_until_complete(task)
    return Response(status=202)
