import zmq
import json
import threading
import time
from typing import Dict, Any, Callable

class EventBus:
    def __init__(self, addr: str = "tcp://127.0.0.1:5555"):
        self.addr = addr
        self.context = zmq.Context()
        self.pub = self.context.socket(zmq.PUB)
        self.pub.bind(addr)
        self.sub = self.context.socket(zmq.SUB)
        self.sub.connect(addr)
        self.sub.setsockopt_string(zmq.SUBSCRIBE, "")
        self.running = True
        self.handlers: Dict[str, Callable] = {}
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()

    def _listen(self):
        while self.running:
            try:
                topic, msg = self.sub.recv_multipart(flags=zmq.NOBLOCK)
                topic_str = topic.decode()
                data = json.loads(msg.decode())
                if topic_str in self.handlers:
                    self.handlers[topic_str](data)
            except zmq.Again:
                time.sleep(0.05)
            except Exception as e:
                print(f"[EventBus] Error: {e}")

    def on(self, topic: str, handler: Callable):
        self.handlers[topic] = handler

    def emit(self, topic: str, data: Dict[str, Any]):
        self.pub.send_multipart([topic.encode(), json.dumps(data).encode()])

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1)
        self.pub.close()
        self.sub.close()
        self.context.term()