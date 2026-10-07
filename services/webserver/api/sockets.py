from services import system


def monitor(socketio):
    system.get_cpu_percent() # first call
    while True:
        socketio.sleep(0.5)
        socketio.emit("cpu", {"percent": system.get_cpu_percent()}) # measures the load since the previous call