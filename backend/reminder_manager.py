from bus import subscribe, publish
from db import insert_event_log
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def handle_reminder(event):
    eid = insert_event_log(event.get('elder_id','e1'), event.get('timestamp'), 'ReminderManager', 'REMINDER_ISSUED', event)
    print(f'[ReminderManager] Reminder issued -> id={eid}')

subscribe('reminder', lambda e: handle_reminder(e))
