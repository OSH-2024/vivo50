import asyncio
import websockets
import tagging
import queue
import _thread

taskQueue = queue.Queue()
sendQueue = queue.Queue()

#处理服务器发起的命令
def cmd_handler():

    cmd_text = str()
    if not taskQueue.empty():
        cmd_text = taskQueue.get()
    else:
        return

    result = ()

    #接收标签返回值
    tag_recv = ""

# try:
    cmd_dict = eval(cmd_text)


    if cmd_dict["type"] == "create":
        tag_recv = tagging.tagging(cmd_dict["path1"])
        result = ("create", tag_recv)

    elif cmd_dict["type"] == "move":
        result = ("move", cmd_dict["path1"] ,cmd_dict["path2"])

    elif cmd_dict["type"] == "delete":
        result = ("delete", cmd_dict["path1"])

    else:
        result = ("invalid",)
