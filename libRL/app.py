import sys
import socket
import multiprocessing
from cefpython3 import cefpython as cef
from os import path, system

here = path.abspath(path.dirname(__file__))
sys.path.insert(0, path.split(here)[0])

from libRL.gui.main import run_app


class handler:
    def __init__(self):
        port = find_port()

        p1 = multiprocessing.Process(target=run_app, args=[port])
        p2 = multiprocessing.Process(target=self.cef_func, args=[port])

        p1.start()
        p2.start()

        p2.join()
        p1.terminate()


    def cef_func(self, port):
        
        sys.excepthook = cef.ExceptHook
        cef.DpiAware.EnableHighDpiSupport()

        cef.Initialize(
            switches={
                'disable-gpu-compositing': None
            }
        )
        
        url = "http://localhost:" + str(port) + '/'

        cef.CreateBrowserSync(
            url=url,
            window_title='libRL.app',
        )
        cef.MessageLoop()
        cef.Shutdown()
        

def find_port():
    port_attempts = 0
    while port_attempts < 1000:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', 0))
            app_port = sock.getsockname()[1]
            sock.close()
            print('push to port:' + str(app_port))
            return app_port
        except:
            port_attempts += 1

    print("FAILED AFTER 1000 PORT ATTEMPTS")
    sys.exit(1)

def browser_version(port):
    run_app(port)

def init():

    pltfrm = sys.platform

    version = sys.version_info

    if pltfrm == "win32" and version[1] < 8:
        handler()

    else:
        print('Currently the embedded app is available on windows in python 3.7')
        print('Pushing to localhost...')
        port = find_port()
        print('opened on localhost:' + port) 
        browser_version(port)

if __name__ == "__main__":
    handler()

