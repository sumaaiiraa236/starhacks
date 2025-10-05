import os, logging
from db import query_recent_events, insert_advice_history
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def summarize_and_store(elder_id='e1'):
    rows = query_recent_events(elder_id, limit=10)
    facts = [f"{r['timestamp']} {r['source_agent']} {r['event_type']}" for r in rows]
    summary = 'Recent events:\n' + '\n'.join(facts[:5])
    insert_advice_history(elder_id, rows[0]['timestamp'] if rows else '', summary, {'count': len(facts)})
    print('[FamilyLiaison] Summary generated (safe RAG-style)')

if __name__=='__main__':
    summarize_and_store('e1')
