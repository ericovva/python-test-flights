from aiohttp import web
import helper
import json

async def find_flight(request):
    # !TODO limit, offset pagination
    try:
        source = request.query['source']
        dest = request.query['dest']
    except Exception as e:
        return web.Response(text='{"error": "Invalid source or dest"}', status=400)
    else:
        result = helper.find_flight(source, dest)
        return web.Response(text=json.dumps(result))

async def filter_flight(request):
    cond = request.query.get('cond', '')
    # !TODO limit, offset pagination
    try:
        source = request.query['source']
        dest = request.query['dest']
    except Exception as e:
        return web.Response(text='{"error": "Invalid source or dest"}', status=400)
    else:
        result = helper.filter_flight(source, dest, cond)
        return web.Response(text=json.dumps(result))

app = web.Application()
app.add_routes([
    web.get('/top', filter_flight),
    web.get('/', find_flight),
])

web.run_app(app)
