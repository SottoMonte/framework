try:
    from js import WebSocket
except Exception as e:
    print(f"Error sending message: {e}")

class adapter:
    def __init__(self, **constants):
        self.config = constants.get('config', {})
        self.url = self.config.get('url', 'ws://localhost:8000/messenger')
        self.socket = None
        self.processable = constants.get('processable', [])
        
    def connect(self):
        try:
            self.socket = WebSocket(self.url)
            self.socket.onopen = self.on_open
            self.socket.onmessage = self.on_message
            self.socket.onclose = self.on_close
            self.socket.onerror = self.on_error
            print(f"Connecting to {self.url}")
        except Exception as e:
            print(f"Failed to create WebSocket: {e}")
    
    def on_open(self, event):
        print(f"WebSocket connection opened to {self.url}")

    def on_message(self, event):
        print(f"Received message: {event.data}")

    def on_close(self, event):
        print(f"WebSocket connection closed: {event.code}, {event.reason}")

    def on_error(self, event):
        print(f"WebSocket error: {event}")

    def send(self, message):
        if self.socket and self.socket.readyState == WebSocket.OPEN:
            try:
                self.socket.send(message)
                print(f"Sent message: {message}")
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            self.connect()
            print("WebSocket is not open. Cannot send message.")

    def close(self):
        if self.socket and self.socket.readyState in [WebSocket.OPEN, WebSocket.CONNECTING]:
            self.socket.close()
            print("Closing WebSocket connection.")

    async def can(self, **constants):
        name = constants.get('name')
        if name in self.processable:
            return True
        return False

    async def post(self, **constants):
        message = constants.get('msg', '')
        if message:
            self.send(message)

    async def read(self, **constants):
        # Since `js.WebSocket` does not support async/await, you cannot use `await`
        # Instead, messages are handled via `on_message` callback.
        print("Reading messages via on_message callback.")
