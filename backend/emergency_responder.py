from bus import subscribe, publish
from db import get_elder_profile, insert_event_log
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def handle_alert(alert):
    # deterministic escalation: print and log
    eid = insert_event_log(alert.get('elder_id','e1'), 'now', 'EmergencyResponder', 'ESCALATION', alert)
    print(f'[EmergencyResponder] Escalation executed -> escalation_id={eid}')

subscribe('alerts', lambda a: handle_alert(a))
