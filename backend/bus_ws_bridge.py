

import os, json
WS_EVENTS_FILE = os.path.join(os.path.dirname(__file__), 'ws_events.jsonl')

def append_ws_event(topic, message):
    try:
        with open(WS_EVENTS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'topic': topic, 'message': message}) + '\n')
    except Exception:
        pass
