import threading, time

# tkinter events from threads
# https://stackoverflow.com/questions/64287940/update-tkinter-gui-from-a-separate-thread-running-a-command

class EventThread(threading.Thread):
    def __init__(self, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        # self.queue = queue
        self.daemon = True
        # self.receive_messages = args[0]
        self.frame_seconds = (1. / 20.) # 20 fps update rate
        self.root_delegate = None

    # Thread.start() process
    def run(self):
        while True:
            self.root_delegate.event_generate("<<TickUpdate>>", when="tail", state=123) # trigger event in main thread
            time.sleep(self.frame_seconds)

ui_bg_thread = EventThread()
#ui_bg_thread.start()