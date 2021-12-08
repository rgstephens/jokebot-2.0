# rm test.py; cat <<'EOF' >> test.py
# from another pod:  python test_sockets.py http://rasa.gstephens:5005/socket.io
# python test_sockets.py https://gstephens.org/socket.io
# python test_sockets.py https://sara-demo.rasa.com/socket.io/          
# curl "https://sara-demo.rasa.com/socket.io/?transport=polling&EIO=4"
# curl "https://gstephens.org/socket.io/?transport=polling&EIO=4"
# curl "https://sara-demo.rasa.com/socket.io/?transport=polling&EIO=3"
import socketio
import asyncio
import sys

session_id = "python_test2"
hi = "hi"
server = 'http://localhost:5005'

if (len(sys.argv) > 1) and (sys.argv[1]):
    server = sys.argv[1]
    print(f"setting server to {server}")

loop = asyncio.get_event_loop()

sio = socketio.AsyncClient(logger=True, engineio_logger=True)

@sio.event
async def bot_uttered(data):
    print(f">> bot_uttered: {data}")

@sio.on('*')
async def catch_all(event, sid, data):
    print(f">> catch_all: {data}")

@sio.event
async def connect():
    print(">> I'm connected!")

@sio.event
async def connect_error(data):
    print(">> The connection failed!")

@sio.event
async def disconnect():
    print(">> I'm disconnected!")

async def main():
    await sio.connect(server)
    print(">> emitting session_request")
    await sio.emit('session_request', {'session_id': session_id})
    print(">> sleep 2")
    await sio.sleep(2)
    print(">> emitting user_uttered")
    await sio.emit('user_uttered', {'message': hi, 'session_id': session_id})
    await sio.sleep(2)
    await sio.emit('user_uttered', {'message': 'geek joke', 'session_id': session_id})
    await sio.sleep(4)
#sio.disconnect()

loop.run_until_complete(main())
