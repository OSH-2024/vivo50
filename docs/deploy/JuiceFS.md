部署主要参考官方文档 [快速上手 - 《JuiceFS 云服务版 v4.6.0 分布式文件系统教程》 - 书栈网 · BookStack](https://www.bookstack.cn/read/JuiceFS-cloud-4.6.0-zh/25a0c4234840280e.md)

大致流程如下

1、在[阿里云](https://www.aliyun.com/)创建并登录账户，新用户实名认证后有三个月的试用期。开通试用之后，点击账号，可以看到  Access Key 入口，创建一个 Access Key 用于 JuiceFS 挂载。创建之后会生成 `AccessKey ID` 和 `AccessKey Secret`，这个要记录下来后面会用到。

![](https://img2024.cnblogs.com/blog/1996139/202406/1996139-20240605142746139-1539378758.png)

![image](https://static.sitestack.cn/projects/JuiceFS-cloud-4.6.0-zh/9573983a183d515745c3fd108f95f841.png)

接下来下来需要在阿里云的 OSS（对象存储服务）中创建一个存储桶，用于存放文件系统中的文件。直接按照默认的配置即可，Bucket的名字参照第一个，忽略第二个。

![](https://img2024.cnblogs.com/blog/1996139/202406/1996139-20240605142756219-974589900.png)

2、进入[注册 - JuiceFS](https://juicefs.com/accounts/register)，注册并登录 JuiceFS 账号。

![](https://img2024.cnblogs.com/blog/1996139/202406/1996139-20240605142928315-1163435612.png)

服务器区域填阿里云注册时候的区域，点击创建文件系统，结果如下：

![](https://img2024.cnblogs.com/blog/1996139/202406/1996139-20240605143055306-1636701296.png)

点开控制中心的设置，复制挂载命令和加粗的 Token，之后要用到。

![](https://img2024.cnblogs.com/blog/1996139/202406/1996139-20240605143141111-525420948.png)

3、在 Linux 虚拟机中挂载文件系统。官方文档要求的配置是 python 3.5+以上版本，并需要自行安装 FUSE。我的 ubuntu 版本是 22.04，软件源是清华源，安装时自带了 FUSE，版本是 3.10.5。

打开终端，输入从 JuiceFS 控制台复制的命令即可挂载。

可能需要稍微改动一下，我的命令是：

`sudo curl -L https://juicefs.com/static/juicefs -o /usr/local/bin/juicefs && sudo chmod +x /usr/local/bin/juicefs`

`sudo juicefs mount vivo50 /jfs`

然后会提示你输入 JuiceFS 的 Token 和之前保存的阿里云的 Acces Key。

等几秒钟之后就会提示挂载完成，此时 `/jfs` 目录下就是挂载的文件系统。可以直接在这个目录下加入或者删除文件。
我简单测试了一下，在两台虚拟机上同时挂载，然后修改其中一个 `/jfs` 目录下的内容，另一个也会被修改。所以可以取代 My-Glow 小组的 storage 模块，实现分布式存储。
