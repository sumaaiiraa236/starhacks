from db import query_recent_events
import sys
limit = int(sys.argv[1]) if len(sys.argv)>1 else 10
print(query_recent_events('e1', limit=limit))
