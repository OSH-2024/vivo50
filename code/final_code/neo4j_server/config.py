class args():
    def __init__(self):
        self.set={
            # general
            "download_path":"/home/liuchang/dfile",
            "json_path":"/home/liuchang/newfs/web_server/static/test.json",
            "json_path2":"/home/liuchang/newfs/web_server/static/test2.json",
            "upload_path":"/home/liuchang/upfile",
            "storage_path":"/jfs",
            "split_char":"%$$%@#!#(*%^&%",
            "use_ray":False,
            "listen_ip":"0.0.0.0",
            "keywords_num":10,
            # web_server
            "web_ip":"127.0.0.1",
            "visit_web_port":5000,
            # central_server
            "central_ip": "192.168.136.131",
            # Ray_Module
            "Ray_listen_neo":4001,
            "Ray_send_neo":4000,
            # neo_server
            "neo_ip":"192.168.136.131",
            "neo_listen_Ray":4000,
            "neo_send_Ray":4001,
}