import asyncio, logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
subscribers = {}
try:
    from .bus_ws_bridge import append_ws_event
except Exception:
    append_ws_event = None

def publish(topic: str, message: dict):
    handlers = subscribers.get(topic, [])
    logging.info('Publishing message to topic=%s -> handlers=%d', topic, len(handlers))
    # write to ws bridge file for API if available
    try:
        if append_ws_event:
            append_ws_event(topic, message)
    except Exception:
        pass
    for h in handlers:
        try:
            if asyncio.iscoroutinefunction(h):
                asyncio.create_task(h(message))
            else:
                h(message)
        except Exception as e:
            logging.exception('Handler error: %s', e)

def subscribe(topic: str, handler):
    if topic not in subscribers:
        subscribers[topic] = []
    subscribers[topic].append(handler)
    logging.info('Subscribed handler %s to topic=%s', getattr(handler, '__name__', str(handler)), topic)
