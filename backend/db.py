import os, json, sqlite3
DB_PATH = os.path.join(os.path.dirname(__file__), 'carecrew.db')
def _conn():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = _conn(); cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS elder_profile (elder_id TEXT PRIMARY KEY, name TEXT, baseline_vitals TEXT, emergency_contacts TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS event_log (id INTEGER PRIMARY KEY AUTOINCREMENT, elder_id TEXT, timestamp TEXT, source_agent TEXT, event_type TEXT, payload TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS advice_history (id INTEGER PRIMARY KEY AUTOINCREMENT, elder_id TEXT, timestamp TEXT, summary TEXT, metadata TEXT)')
    conn.commit(); conn.close()
def upsert_elder_profile(elder_id,name,baseline_vitals,emergency_contacts):
    conn=_conn(); cur=conn.cursor(); cur.execute('INSERT OR REPLACE INTO elder_profile (elder_id,name,baseline_vitals,emergency_contacts) VALUES (?,?,?,?)', (elder_id,name,json.dumps(baseline_vitals), json.dumps(emergency_contacts))); conn.commit(); conn.close()
def get_elder_profile(elder_id):
    conn=_conn(); cur=conn.cursor(); cur.execute('SELECT elder_id,name,baseline_vitals,emergency_contacts FROM elder_profile WHERE elder_id=?',(elder_id,)); r=cur.fetchone(); conn.close()
    if not r: return None
    return {'elder_id': r['elder_id'], 'name': r['name'], 'baseline_vitals': json.loads(r['baseline_vitals']) if r['baseline_vitals'] else {}, 'emergency_contacts': json.loads(r['emergency_contacts']) if r['emergency_contacts'] else {}}
def insert_event_log(elder_id,timestamp,source_agent,event_type,payload):
    conn=_conn(); cur=conn.cursor(); cur.execute('INSERT INTO event_log (elder_id,timestamp,source_agent,event_type,payload) VALUES (?,?,?,?,?)', (elder_id,timestamp,source_agent,event_type,json.dumps(payload))); eid=cur.lastrowid; conn.commit(); conn.close(); return eid
def query_recent_events(elder_id, limit=100):
    conn=_conn(); cur=conn.cursor(); cur.execute('SELECT id,elder_id,timestamp,source_agent,event_type,payload FROM event_log WHERE elder_id=? ORDER BY id DESC LIMIT ?', (elder_id, limit)); rows=cur.fetchall(); conn.close()
    out=[]
    for r in rows: out.append({'id': r['id'], 'elder_id': r['elder_id'], 'timestamp': r['timestamp'], 'source_agent': r['source_agent'], 'event_type': r['event_type'], 'payload': json.loads(r['payload']) if r['payload'] else {}})
    return out
def insert_advice_history(elder_id,timestamp,summary,metadata):
    conn=_conn(); cur=conn.cursor(); cur.execute('INSERT INTO advice_history (elder_id,timestamp,summary,metadata) VALUES (?,?,?,?)', (elder_id,timestamp,summary,json.dumps(metadata))); aid=cur.lastrowid; conn.commit(); conn.close(); return aid
