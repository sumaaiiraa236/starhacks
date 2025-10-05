from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio, os, json
app = FastAPI(title='CareCrew API')

class ConnectionManager:
    def __init__(self):
        self.active = []
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
    def disconnect(self, ws: WebSocket):
        try: self.active.remove(ws)
        except: pass
    async def broadcast(self, msg: str):
        to_remove = []
        for c in list(self.active):
            try:
                await c.send_text(msg)
            except Exception:
                to_remove.append(c)
        for r in to_remove:
            self.disconnect(r)

manager = ConnectionManager()
WS_EVENTS_FILE = os.path.join(os.path.dirname(__file__), 'ws_events.jsonl')

async def tail_file_and_broadcast():
    last = 0
    while True:
        try:
            if os.path.exists(WS_EVENTS_FILE):
                size = os.path.getsize(WS_EVENTS_FILE)
                if size > last:
                    with open(WS_EVENTS_FILE, 'r', encoding='utf-8') as f:
                        f.seek(last)
                        for line in f:
                            line=line.strip()
                            if not line: continue
                            await manager.broadcast(line)
                    last = size
        except Exception:
            pass
        await asyncio.sleep(0.5)

@app.on_event('startup')
async def startup():
    asyncio.create_task(tail_file_and_broadcast())

@app.websocket('/ws')
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)
