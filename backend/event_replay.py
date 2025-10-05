import asyncio, pandas as pd, json, logging
from datetime import datetime
from bus import publish
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def _normalize(v):
    try:
        import pandas as _pd
        if isinstance(v, _pd.Timestamp): return v.isoformat()
    except Exception:
        pass
    if isinstance(v, datetime): return v.isoformat()
    try: json.dumps(v); return v
    except Exception: return str(v)

def _classify(row):
    s = ' '.join([str(v).lower() for v in row.values])

    if any(k in s for k in ['heart','hr','spo2','oxygen','blood']): return 'vitals'
    if any(k in s for k in ['fall','inactivity','emergency']): return 'safety'
    if any(k in s for k in ['reminder','medication']): return 'reminder'
    return 'raw'

async def replay_csv_loop(csv_path, speed=1.0, elder_id='e1', loop_once=False, max_events=None):
    logging.info('Loading CSV: %s', csv_path)
    df = pd.read_csv(csv_path)
    ts_col=None
    for c in df.columns:
        if c.lower() in ('timestamp','time','datetime'):
            df[c]=pd.to_datetime(df[c], errors='coerce'); ts_col=c; break
    if not ts_col:
        raise ValueError('No timestamp column')
    df = df.dropna(subset=[ts_col]).sort_values(ts_col).reset_index(drop=True)
    if max_events: df = df.head(max_events)
    for i,row in df.iterrows():
        if i>0:
            delta = (row[ts_col] - df[ts_col].iloc[i-1]).total_seconds()
            await asyncio.sleep(max(delta/speed,0))
        payload = row.to_dict(); payload['elder_id']=elder_id; payload['timestamp']=_normalize(row[ts_col])
        topic = _classify(row)
        publish('raw', payload)
        publish(topic, payload)
        logging.info('Published %d/%d -> %s', i+1, len(df), topic)

if __name__=='__main__':
    import asyncio, sys
    csv = sys.argv[1] if len(sys.argv)>1 else '../data/health_monitoring.csv'
    asyncio.run(replay_csv_loop(csv, speed=50, elder_id='e1', loop_once=True, max_events=200))
