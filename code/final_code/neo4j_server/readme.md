## neo4j部署文档

### 一、安装 jdk17

- `neo4j` 需要相应的 `java` 版本与其进行适配，我选用的 `neo4j` 版本是 [neo4j-community-5.4.0](https://rec.ustc.edu.cn/share/c89cf710-33c3-11ef-9e8b-0144f6057c36) ，与其对应的 `java` 版本是 [jdk-17](https://rec.ustc.edu.cn/share/1e5ba680-33c4-11ef-9ce8-7b17a40f075d)

- 首先卸载服务器上原本可能存在的 `openjdk`

  `sudo apt-get remove openjdk*`

- 找到压缩包 `jdk-17_linux-x64_bin.tar.gz `

- 找到一个合适的路径，建议在 `/usr/local`，新建文件夹 `jdk17`，在其中解压缩

  `sudo tar -xvf jdk-17_linux-x64_bin.tar.gz`

- 从根目录进入 `etc/profile` 文件，在最后添加下面四行

  ```
  export JAVA_HOME=/usr/local/jdk17/jdk-17.0.11
  export JRE_HOME=${JAVA_HOME}/jre
  export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
  export PATH=${JAVA_HOME}/bin:~/.local/bin:$PATH
  ```

- 使该配置文件生效

  `source /etc/profile`

- 查看是否成功安装：

  `java -version`

  注：可能会出现，使用命令 `source /etc/profile` 后，使用 `java -version`可以正确显示上述命令，而关掉当前命令行终端再打开后，再次输入 `java -version` 却显示没有 java 命令，如已经严格按照上述步骤配置，那么解决方案是重启。

  

### 二、安装  neo4j

- 找到压缩包` neo4j-community-5.4.0-unix.tar.gz`

- 解压缩

 `tar -xvf neo4j-community-5.4.0-unix.tar.gz`

- s找到解压缩后的文件夹修改配置文件，该配置文件是在 `/neo4j-community-5.4.0/conf` 中的 `neo4j.conf`

`sudo vim neo4j.conf`

- 把 `neo4j.conf` 的内容改为当前文件夹下的 `neo4j.conf` 的内容

- 启动服务（同样道理./neo4j stop停止服务）

`cd neo4j-community-5.4.0/bin/`

`./neo4j start`

- 浏览器查看 http://0.0.0.0:7474/ 登录用户名密码默认都是 `neo4j` 会让修改一下密码，这里我将密码改为了 `vivo5000`，注意要修改 `label.html` 第 `173` 行和 `neo4j_server.py` 中相应的部分

    [![image-20220405153110974](https://github.com/OSH-2023/My-Glow/raw/main/deploy/src/image-20220405153110974.png)](https://github.com/OSH-2023/My-Glow/blob/main/deploy/src/image-20220405153110974.png)

- 注：可能会出现按照上述步骤配置，能够在命令行显示 `neo4j` 已经启动，但是浏览器打开对应网址却无法加载，这时考虑是否是因为虚拟机的防火墙导致，关闭防火墙指令：

`sudo ufw disable`
