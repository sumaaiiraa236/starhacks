from bus import subscribe, publish
from db import insert_event_log
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def handle_safety(event):
    ev = event.get('Event') or event.get('event') or event.get('Alert') or 'safety'
    if 'fall' in str(ev).lower():
        eid = insert_event_log(event.get('elder_id','e1'), event.get('timestamp'), 'SafetyMonitor', 'FALL_ALERT', event)
        publish('alerts', {'type':'FALL_ALERT','id':eid})
        print(f'[SafetyMonitor] FALL detected -> event_id={eid}')

subscribe('safety', lambda e: handle_safety(e))
