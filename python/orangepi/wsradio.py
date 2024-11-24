
import tornado
import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import asyncio
import subprocess


#Tornado Folder Paths
settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"), static_path = os.path.join(os.path.dirname(__file__), "static")
    )


#Tonado server port
PORT = 8081


def broadcast_message(message):
    print("broadcast_message "+ message)
    for client in WSHandler.clients:
        client.write_message("info="+message)



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print ("[HTTP](MainHandler) User Connected.")
        self.render("index.html")

    def post(self):
        value = self.get_argument('sleep')
        print("set sleep "+ value)
        global MIN_SLEEPV
        MIN_SLEEPV = int(value)
        os.system("/usr/bin/python startsleeper.py "+ str(MIN_SLEEPV))
        # display.display("starting sleep timer\n", True)
        display.frezeeDisplay(3)
        myoled.displayfs("starting sleep timer\nin "+ str(MIN_SLEEPV)+" minutes",15)
        # ok()
        self.render("index.html")

class postHandler(tornado.web.RequestHandler):
    def get(self):
        value = self.get_argument('playlist')
        print(value)
        self.write(value)
    def post(self):
        value = self.get_argument('sleep')
        sr=subprocess.check_output("mpc volume "+ value, shell=True).decode("utf-8")
        self.write("volume"+sr)
# class staticFileHandler(tornado.web.StaticFileHandler):
#     def get(self):
class shellCmd(tornado.web.RequestHandler):#scmd
    def get(self,input):
        # print("input="+str(input))
        # cmd=self.get_argument('hostname')
        if input=="playlist":
            sr=subprocess.check_output("mpc playlist", shell=True).decode("utf-8")
            pl=sr.splitlines(keepends=False)
            rp=""
            for i in range(len(pl)):
                rp+= "<button class=\"button1\" onclick=\"sendcmd('mpc play " + str(i+1) +"')\"><a>"+str(i+1)+". "+pl[i]+"</a></button>"
            self.write(rp)
        elif input== "iplaylist":
            sr=subprocess.check_output("mpc lsplaylists", shell=True).decode("utf-8")
            pl=sr.splitlines(keepends=False)
            rp=""
            for i in range(len(pl)):
                rp+= "<button class=\"button1\" onclick=\"sendcmd('mpc load " + pl[i] +"')\"><a>"+str(i+1)+". "+pl[i]+"</a></button>"
            self.write(rp)
        elif input== "status":
            sr=subprocess.check_output("mpc", shell=True).decode("utf-8")
            self.write(sr)
        elif input== "hostname":
            sr=subprocess.check_output("hostname", shell=True).decode("utf-8")
            self.write(sr)
        else:
            self.write("hai")
    def post(self):
        value = self.get_argument('cmd')
        sr=subprocess.check_output("mpc volume "+ value, shell=True).decode("utf-8")
        self.write("volume"+sr)
        # print(cmd)

class WSHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    def open(self):
        print ('[WS] Connection was opened.')
        self.clients.add(self)
        print(f"Client connected: {self.request.remote_ip}")

    def on_message(self, message):
        print ('[WS] Incoming message:'), message

        if message.startswith("0>"):
            sbmsg=message[2:]
            if sbmsg.startswith("mpc load"):
                subprocess.check_output("mpc clear", shell=True)
                subprocess.check_output(sbmsg, shell=True).decode("utf-8")
                subprocess.check_output("mpc play   ", shell=True).decode("utf-8")
            else:
                sr=subprocess.check_output(sbmsg, shell=True).decode("utf-8")
    # if message == "on_g":
    #   print("OK") #GPIO.output(16, True)
    # if message == "off_g":
    #   print("OK") #GPIO.output(16, False)
    #
    # if message == "on_r":
    #   print("OK") #GPIO.output(18, True)
    # if message == "off_r":
    #   print("OK") #GPIO.output(18, False)
    #
    # if message == 'on_b':
    #   print("OK") #GPIO.output(11 , True)
    # if message == 'off_b':
    #   print("OK") #GPIO.output(11 , False)
    #
    # if message == 'on_w':
    #   print("OK") #GPIO.output(13 , True)
    # if message == 'off_w':
    #   print("OK") #GPIO.output(13 , False)

    def on_close(self):
        print ('[WS] Connection was closed.')

    @classmethod
    def send_message(cls, message):
        removable = set()
        for ws in cls.live_web_sockets:
            if not ws.ws_connection or not ws.ws_connection.stream.socket:
                removable.add(ws)
            else:
                ws.write_message(message)
        for ws in removable:
            cls.live_web_sockets.remove(ws)

# websock= WSHandler(tornado.websocket.WebSocketHandler)
application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/cmd/', postHandler),
  (r'/scmd/(\w+)', shellCmd),
  (r'/ws', WSHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "/root/static"}),
  ], **settings)


# if __name__ == "__main__":
# try:
#     http_server = tornado.httpserver.HTTPServer(application)
#     http_server.listen(PORT)
#     main_loop = tornado.ioloop.IOLoop.instance()
#
#     print ("Tornado Server started")
#     main_loop.start()
#
# except:
#     print ("Exception triggered - Tornado Server stopped.")
#     print("OK") #GPIO.cleanup()

async def main():
    # app = make_app()
    # app.listen(8888)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)
    print("Server started at http://127.0.0.1:"+str(PORT))
    await asyncio.Event().wait()  # Keep the server running

if __name__ == "__main__":
    asyncio.run(main())
