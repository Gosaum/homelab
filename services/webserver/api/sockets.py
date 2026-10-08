from services import system

def monitor(socketio):
    while True:
        socketio.sleep(1)
        socketio.emit("kpis", system.get_system_kpis())