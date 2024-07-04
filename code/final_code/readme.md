## 部署方法

1、参照 `docs/deploy/JiuceFS.md` ，完成 `JuiceFS` 的部署。

2、在终端中输入 `sudo juicefs mount vivo50 /jfs`，将 `JuiceFS` 挂载到本地的 `/jfs` 目录下。

3、把 `final_code` 目录下的所有文件拷贝下来。

4、在终端中输入 `sudo chmod 777 /jfs` ，修改一下存储路径的权限。

5、更改 `config.py` 中的文件，其中的 `central_ip` 要改成你本机的地址，`download_path` 是从网页端下载下来的文件存储的路径，`json_path` 是 `json` 文件的路径，这个要改成你的 `web_server` 相应的路径，`upload_path` 是上传到网页端的文件存放的缓冲区路径，`storage_path` 是 `JuiceFS` 挂载的路径，上面几个都要改成你自己的机子里面的，所有目录下的 `config.py`记得都要改掉。

6、更改 `test_json` 和  `test_json2` 文件，`test_json`  要改成和你的 `JuiceFS` 中的文件完全一致，最好是挂载之前把 `JuiceFS` 中的文件全部删掉，这样 `test_json` 中只有一个空文件夹就可以。

```json
{
    "id": 1,
    "name": "/",
    "isdir": true,
    "children": []
}
```

7、运行 `web_server` 下的 `web_server.py`。然后在浏览器中输入 `localhost:5000` 这个网址，就可以访问文件系统。

8、启动 `neo4j`，在终端中收入`cd neo4j-community-5.20.0/bin/` ，然后输入 `./neo4j start`。

9、运行 `neo4j_server` 下的 `neo4j_server.py`,在 `http://0.0.0.0:7474/browser/` 下即可查看图数据库中的结点以及边的对应关系。

10、清除图数据库的所有节点，需要输入命令 `MATCH (n) DETACH DELETE n`。

