import dbus
import time

bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")


from xmlrpclib import ServerProxy, Error

PULSE_URL = "http://192.168.1.21:8080/xmlrpc"

server = ServerProxy(PULSE_URL)
token = server.RemoteApi.login('admin', '')
build_id = -1

while True:
    time.sleep(5)
    build = server.RemoteApi.getLatestBuildForProject(token, "global project template", True)[0]
    print build['id'], build['project'], build['succeeded']
    if build_id == build['id']:
        continue

    if not build['succeeded']:
        for conv in purple.PurpleGetIms():
            purple.PurpleConvImSend(purple.PurpleConvIm(conv), "Build do projeto " + build['project'] + " FALHOU!")
