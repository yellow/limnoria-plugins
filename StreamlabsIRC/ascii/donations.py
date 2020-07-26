import websocket
import pprint
import json
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    if 'event' not in message:
        return

    first_square_bracket_index = message.find('[')

    if first_square_bracket_index == -1:
        return

    message_list_string = message[first_square_bracket_index:]
    message_list = json.loads(message[first_square_bracket_index:])
    # pprint.pprint(message_list)
    donation_message = message_list[1]['message'][0]['message']
    print(donation_message)
    for i in range(10):
        time.sleep(1)
        print(i)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        while True:
            time.sleep(15)
            ws.send("2")
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    def stream_sock():
        ws = websocket.WebSocketApp("wss://sockets.streamlabs.com/socket.io/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkJBNTAwNjNEMDk3NzJBMTkyRjFEIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwicGljYXJ0b19pZCI6IjEwNjk5ODYifQ.87-s3jzRFqxNnZKz1KyR-_uQGA8i6wQgWSdHkPh17Vo&EIO=3&transport=websocket",
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()
    thread.start_new_thread(stream_sock, ())

for i in range(100):
    time.sleep(1)
    print(i * 10)
thread.join()
