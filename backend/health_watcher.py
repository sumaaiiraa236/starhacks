from bus import subscribe, publish
from db import get_elder_profile, insert_event_log
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

THRESHOLDS = {'hr_max':110, 'spo2_min':93}

def handle_vitals(event):
    hr = None
    if 'HeartRate' in event: hr = int(event.get('HeartRate') or 0)
    elif 'Heart Rate' in event: hr = int(event.get('Heart Rate') or 0)
    spo2 = event.get('OxygenSaturation') or event.get('SpO2') or event.get('SpO₂')
    if spo2 is not None:
        try: spo2 = int(spo2)
        except: spo2 = None
    if hr and hr > THRESHOLDS['hr_max']:
        eid = insert_event_log(event.get('elder_id','e1'), event.get('timestamp'), 'HealthWatcher', 'HIGH_HR_ALERT', event)
        publish('alerts', {'type':'HIGH_HR_ALERT','id':eid,'hr':hr})
        print(f'[HealthWatcher] HIGH HR detected: {hr} -> event_id={eid}')

subscribe('vitals', lambda e: handle_vitals(e))
