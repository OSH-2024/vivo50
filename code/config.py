class args():
    def __init__(self):
        self.set={
            # general
            "absolute_path":"D:\\PycharmProjects\\NewDFS\\",
            "split_char":"%$$%@#!#(*%^&%",
            "use_ray":False,
            "listen_ip":"0.0.0.0",
            "keywords_num":10,
            # web_server
            "web_ip":"127.0.0.1",
            "visit_web_port":5000,
            "web_listen_central":10000,
            "web_send_central":3333,
            # central_server
            "central_ip": "192.168.209.1",
            "central_listen_web":3333,
            "central_send_web":10000,
            "central_listen_storage":6000,
            "central_send_storage":8888,

            # Ray_Module
            "Ray_listen_neo":4001,
            "Ray_send_neo":4000,
            # storage_server
            "storage_num":2,
            "storage_ip":["192.168.137.159"],
            "storage_listen_central":[8888],
            "storage_send_central":[6000],
            # neo_server
            "neo_ip":"192.168.209.136",
            "neo_listen_Ray":4000,
            "neo_send_Ray":4001,
}

