import TonyServer

url = 'http://192.168.4.2'
url_stream = url + ':81/stream'
url_cmd = url + '/action'

cmds = ["LED_ON",
"LED_OFF",
"FOLLOW_LINE",
"STOP",
"LOOK_AROUND",
"STOP_LOOKING",
"HORIZONTAL_SERVO",
"VERTICAL_SERVO"]

while True:
    CMD = input(">")
    CMD.strip().replace(" ", "_")
    if CMD == "stop" or CMD == "s":
        break
    if CMD == "show":
        for c in cmds:
            print(c)
    CMD = CMD.strip().replace(" ", "_").upper()
    if CMD.split("-")[0] in cmds:
        TonyServer.cmd(CMD, url_cmd)
        print(CMD)
    else:
        print("Command not valid")


