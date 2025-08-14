
import asyncio
from aiohttp import web
from ..services.bot_logger_service import logger
from ..models.priority_log import PriorityLog

async def health(request):
    return web.json_response({"ok": True})

async def stats(request):
    data = await PriorityLog.find_many(limit=5)
    return web.json_response({"latest": data})

async def create_app():
    app = web.Application()
    app.add_routes([web.get("/health", health), web.get("/stats", stats)])
    return app

async def run_http_server(host="0.0.0.0", port=8080):
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info("HTTP admin running on http://%s:%d", host, port)
