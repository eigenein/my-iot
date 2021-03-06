from __future__ import annotations

from datetime import timedelta
from typing import Any, Awaitable, Callable, Dict

from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_jinja2 import template

from my_iot import templates
from my_iot.charts import make_float_chart
from my_iot.constants import ACTUAL_KEY, DEFAULT_PERIOD, HTTP_PORT, STATICS
from my_iot.context import Context
from my_iot.database import get_actual, get_log
from my_iot.helpers import run_in_executor
from my_iot.types_ import Event

routes = web.RouteTableDef()


def start(
    context: Context,
    on_startup: Callable[[web.Application], Awaitable[Any]],
    on_cleanup: Callable[[web.Application], Awaitable[Any]],
):
    """
    Start the web app.
    """
    app = web.Application()
    app['context'] = context
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    app.add_routes(routes)

    templates.setup(app)

    # noinspection PyTypeChecker
    web.run_app(app, port=HTTP_PORT, print=None)


@routes.get(r'/')
@template('index.html')
async def get_index(request: web.Request) -> dict:
    context: Context = request.app['context']
    return {
        'actual': (await run_in_executor(get_actual, context.db)).values(),
    }


@routes.get(r'/channel/{channel}')
@template('channel.html')
async def get_channel(request: web.Request) -> dict:
    context: Context = request.app['context']
    channel: str = request.match_info['channel']
    try:
        raw_event: Dict[Any, Any] = context.db[ACTUAL_KEY][channel]
    except KeyError:
        raise HTTPNotFound(text='Channel is not found.')
    event = Event(**raw_event)
    try:
        period = timedelta(seconds=abs(int(request.query.get('period'))))
    except (TypeError, ValueError):
        period = DEFAULT_PERIOD
    events = await run_in_executor(get_log, context.db, channel, period)
    chart = None
    if events:
        if event.unit.is_float:
            chart = await run_in_executor(make_float_chart, events)
    return {
        'chart': chart,
        'event': event,
        'has_events': bool(events),
        'raw_event': raw_event,
        'request': request,
    }


@routes.get(r'/events')
@template('events.html')
async def get_events(request: web.Request) -> dict:
    return {'request': request}


@routes.get(r'/services')
@template('services.html')
async def get_services(request: web.Request) -> dict:
    return {'services': request.app['context'].services}


# Must go at the end.
@routes.get(r'/{name:.+}')
async def get_static(request: web.Request) -> web.Response:
    try:
        body = STATICS[request.match_info['name']]
    except KeyError:
        raise HTTPNotFound()
    else:
        return web.Response(body=body)
