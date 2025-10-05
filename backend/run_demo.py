import asyncio, sys, os
from event_replay import replay_csv_loop
from test_listener import start_listeners

if __name__=='__main__':
    csv = sys.argv[1] if len(sys.argv)>1 else '../data/health_monitoring.csv'
    # start listeners (non-blocking)
    try:
        start_listeners()
    except Exception:
        pass
    asyncio.run(replay_csv_loop(csv, speed=50, elder_id='e1', loop_once=True, max_events=200))
