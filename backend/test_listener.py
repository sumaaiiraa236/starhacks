from bus import subscribe
import asyncio, json, logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

async def on_raw(e):
    print('\n[RAW EVENT] ', e.get('timestamp'), e.get('DeviceID', e.get('Device-ID', '')))
async def on_vitals(e):
    print('\n[VITALS] ', e.get('timestamp'), 'HR=', e.get('HeartRate', e.get('Heart Rate', e.get('HeartRate'))))
async def on_safety(e):
    print('\n[SAFETY] ', e.get('timestamp'), e)
async def on_reminder(e):
    print('\n[REMINDER] ', e.get('timestamp'), e.get('Reminder', e.get('Message')))

def start_listeners():
    subscribe('raw', on_raw)
    subscribe('vitals', on_vitals)
    subscribe('safety', on_safety)
    subscribe('reminder', on_reminder)
    print('Listeners started: raw, vitals, safety, reminder')
