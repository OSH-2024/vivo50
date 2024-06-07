## 部署方法

1、参照 `docs/deploy/JiuceFS.md` ，完成 `JuiceFS` 的部署。

2、在终端中输入 `sudo juicefs mount vivo50 /jfs`，将 `JuiceFS` 挂载到本地的 `/jfs` 目录下。

3、把 `web_server` 和 `central_server` 两个目录下的文件拷贝下来。

4、在终端中输入 `sudo chmod 777 /jfs` ，修改一下存储路径的权限。

5、更改 `config.py` 中的文件，其中的 `central_ip` 要改成你本机的地址，`absolute_path` 是从网页端下载下来的文件存储的路径，`json_path` 是 `json` 文件的路径，这个要改成你的 `web_server` 相应的路径，`upload_path` 是上传到网页端的文件需要存放的路径，`storage_path` 是 `JuiceFS` 挂载的路径，上面几个都要改成你自己的机子里面的，一共有三个 `config.py`，记得都要改掉。

6、更改 `test_json` 文件，改成和你的 `JuiceFS` 中的文件完全一致，最好是挂载之前把 `JuiceFS` 中的文件全部删掉，这样 `test_json` 中只有一个空文件夹就可以。

```json
{
    "id": 1,
    "name": "/",
    "isdir": true,
    "children": []
}
```

7、运行 `Central_server` 下的 `Central_Module.py` 和 `web_server` 下的 `web_server.py`。然后在浏览器中输入 `localhost:5000` 这个网址，就可以访问文件系统。

## 实现功能

目前实现的功能相当于去年 `My-Glow` 小组的 `web_server` 、`central_server` 以及 `storage_server` 三个模块。其中 `web_server` 的部分还需要和反向代理相结合，`central_server` 部分需要和打标部分以及图数据库部分相结合。用户可以在当前的文件系统中上传文件，下载文件，创建文件夹，删除文件以及文件夹。





