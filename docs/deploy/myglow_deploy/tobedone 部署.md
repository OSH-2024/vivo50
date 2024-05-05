# TOBEDONE 部署

## 系统要求

ubuntu版本：18

neo4j版本：4.4.0

python版本：3.6

neo4j的java版本：11

storage和server的java版本：8

mysql版本：5/8（正在测试中）

推荐使用两台机器进行

## 0. 在两台机器上把tobedone的全部文件clone下来

`git clone https://github.com/OSH-2022/x-TOBEDONE.git`

## 1. 在一台机器上进行neo4j安装

### 安装 jdk11

+ 首先卸载服务器上原本可能存在的 openjdk

  `sudo apt-get remove openjdk*`

+ 找到压缩包`jdk-11.0.1_linux-x64_bin.tar.gz `

+ 找到一个合适的路径，建议在 `/usr/local`，新建文件夹，在其中解压缩

  `sudo tar -xvf jdk-11.0.1_linux-x64_bin.tar.gz`

+ 从根目录进入 etc/profile 文件

  ```java
  export JAVA_HOME=/usr/local/上一步新建的文件夹/jdk-11.0.1
  export JRE_HOME=${JAVA_HOME}/jre
  export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
  export PATH=${JAVA_HOME}/bin:~/.local/bin:$PATH
  ```

  最后一行xxx代表用户名

+ 使该配置文件生效

  `source /etc/profile`

+ 查看是否成功安装：

  `java -version`

  ![image-20220405145021107](src/image-20220405145021107.png)

  注：可能会出现，使用命令 `source /etc/profile` 后，使用 `java -version`可以正确显示上述命令，而关掉当前命令行终端再打开后，再次输入 `java -version` 却显示没有 java 命令，如已经严格按照上述步骤配置，那么解决方案是重启。

### 安装 neo4j

+ 找到压缩包` neo4j-community-4.4.0-unix.tar.gz`

+ 解压缩

  `tar -xvf neo4j-community-4.4.0-unix.tar.gz`

+ 找到解压缩后的文件夹修改配置文件，该配置文件是在 /neo4j-community-4.4.0/conf 中的 neo4j.conf

  `sudo vim neo4j.conf`

+ 可以参考[这个链接](https://blog.csdn.net/u013946356/article/details/81736232)查看更详细的参考，这里只列举几个较为关键的配置

  ①修改 load csv 时路径，找到下面这一行，并在前面加个 #，可从任意路径读取文件
  dbms.directories.import=import

  ②可以远程通过 ip 访问 neo4j 数据库，找到并删除以下这一行开头的 #

  dbms.default_listen_address=0.0.0.0

  ③允许从远程 url 来 load csv
  dbms.security.allow_csv_import_from_file_urls=true

  ④设置 neo4j 可读可写
  dbms.read_only=false

  ⑤默认 bolt 端口是 7687，http 端口是 7474，https 关口是 7473；修改如下：		

  ![image-20220405151833045](src/image-20220405151833045.png)

+ 启动服务（同样道理./neo4j stop停止服务）

  `cd neo4j-community-4.4.0`

  `cd bin`

  `./neo4j start`	

+ 浏览器查看
  http://0.0.0.0:7474/
  登录用户名密码默认都是 neo4j
  会让修改一下密码，~~建议修改为 11，因为简单~~

  ![image-20220405153110974](src/image-20220405153110974.png)

+ 注：可能会出现按照上述步骤配置，能够在命令行显示 neo4j 已经启动，但是浏览器打开对应网址却无法加载，这时考虑是否是因为虚拟机的防火墙导致，关闭防火墙指令：

  `sudo ufw disable`

## 2. ray安装（此后所有操作均在另一台机器上进行）

首先要进行[pip换源](https://www.runoob.com/w3cnote/pip-cn-mirror.html)

安装ray**.whl文件

```shell
sudo pip3 install ray**.whl
```



安装结果如下：

![image-20220408161425411](src/image-20220408161425411.png)

## 3. 部署

### neo4j & serverweb

+ `pip3 install websockets`

  `pip3 install neo4j`

`python3 serverWeb.py`

### ray & tagging

#### tagging程序依赖包安装

默认配置为清华源

```shell
pip install pdfplumber
pip install sphinx
pip install ffmpeg
pip install SpeechRecognition
pip install tinytag
pip install pydub
pip install nltk
pip install spacy
python -m nltk.downloader stopwords
python -m nltk.downloader universal_tagset
python3 -m spacy download en
pip install git+https://github.com/boudinfl/pke.git
```

在最后一步安装pke库的时候很可能出现git clone无反应的结果，此时需要手动clone库并执行`python3 setup.py install`。

#### ray

`ray start --head --port=6379`

#### tagging

`pip install watchdog mysql.connector`

`python3 tag_server.py`

### storage & server

#### 安装 jdk8

与上述安装jdk11的过程类似。

#### 安装 Maven

maven 是 java 的项目管理工具。简单来说，当我们修改了 dontpanic 的源码后，就要用 maven 来编译生成一个可执行文件。

具体安装过程可以参照[这个链接](https://www.shuzhiduo.com/A/pRdBwwE2zn/)，注：只需完成1、2步与换源即可

Maven 的使用比较复杂，但是目前我们用到的部分较少，只有以下这些：

+ 想要编译一个 java 项目，需要进入到它的目录下，也就是 pom.xml 文件所在的那一级目录，然后输入 `mvn clean package` ，即可重新编译生成可执行文件
+ 生成的文件，位于刚才的目录下的 target 文件夹，名字最长，且后缀名为 .jar 的那个，运行它需用命令 `java -jar xxx.jar`

#### 安装 tomcat

它的用途是 web 后端

具体安装，可以参考[这个链接](https://blog.csdn.net/gbz2000/article/details/115103722) 的 Step1 到 Step6（推荐把第7步也做完）

#### 安装 mysql

***此处仍有bug！！！***

***22年使用的mysql版本是5.1.39***

***mysql5.1.39暂时找不到合适的安装方式，最新的mysql5.7.42无法使用java连接，需回滚到5.7.36才能连接，但这样将与安装mysql5.1无异***

***mysql 8的最新版本不保证可以成功使用***

##### mysql 8

这个的作用是作为数据库

`sudo apt install mysql-server`

第一次登入，直接用 `mysql -u root` (如果不行就 `sudo mysql -u root`)

然后修改密码，dontpanic 将密码定位 201314，我们也沿用这个，避免需要在源代码中做修改

改密码，需要在 mysql 中 (也就是先 `mysql -u root` 进入 mysql 的命令行内)，运行这条命令 

`ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '201314';`

然后输入 exit 再回车退出

然后需要把 dontpanic 文件夹下的 demo/normal/mysql.sql 文件导入 mysql，这里首先在 mysql 中创建一个叫 DFS 的数据库：

```mysql
ubuntu@VM-12-15-ubuntu:~/Documents/OSH_2022/Project/x-dontpanic/demo/normal$ mysql -u root -p
Enter password: (这里输入密码201314)
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 14
Server version: 8.0.29-0ubuntu0.20.04.3 (Ubuntu)

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(从这里开始)
mysql> CREATE DATABASE DFS;
Query OK, 1 row affected (0.02 sec)

mysql> exit
Bye
```

然后修改 dontpanic 文件夹下的 demo/normal/mysql.sql（原因应该是 mysql 版本不兼容），把最后一行改成这样：(localhost 改成 127.0.0.1 会出错，只能用 localhost)

```mysql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
```

保存退出

最后在命令行输入 `mysql -u root -p <mysql.sql` 即可（要输密码）

##### mysql 5

需要自行寻找mysql的tar.gz包，并与[maven库](https://developer.aliyun.com/mvn/search)中mysql-connector-java的版本比较，找到可以安装并有对应connector的版本进行安装。

22年的osh项目使用了mysql5.1.39，这是符合上述条件的版本，但需要通过tar.gz手动安装。

#### 运行 server 和 client

目前发现的一个问题是，无法连接数据库，可能性比较大的原因是，这个项目当时使用的 mysql 数据库版本低，而我们目前下载的 mysql 版本高，这两个版本不兼容。

而版本信息，是写在 pom.xml 文件中的，这个文件包含了项目的基本信息，用于描述项目如何构建，声明项目依赖等等。

而需要做的修改是：打开 /src/server/ 文件夹下的 pom.xml，大概第十六行的位置，有一个版本号，将它改为你的 mysql 版本号，保存退出。

然后使用 maven 进行重新编译生成

然后在 target 文件夹下运行生成的可执行文件，这个就是新的 server.jar

然后在 /demo/normal/ 文件夹下修改 setup.ini，它的倒数第二行的路径，是存储节点用来存放文件碎片的目录，需要已经创建好，你需要在自己本地创建一个文件，然后将其路径写在这里

然后运行 client.jar 

注：无需运行 /demo/normal 文件夹下的 server.jar，因为你已经修改了 server 的源文件（在上面修改 pom.xml 中的数据库版本时），然后你新编译生成的，就是新的 server.jar 文件

**运行结果**

![非容器化dontpanic运行结果](src/非容器化dontpanic运行结果.png)

### 启动网页端

请参考本目录下文件夹“非容器化部署web-app-name-2020”，这个文件夹下是所需要的全部 web 代码，请将它复制到你的 tomcat 下的 webapps 文件夹内：

```shell
sudo cp -r web-app-name-2020 /opt/tomcat/webapps
```

检查下自己的 tomcat 有没有启动

```shell
sudo systemctl status tomcat
```

如果没有的话，启动 tomcat

```shell
sudo systemctl start tomcat
```

之后打开 `localhost:8080/web-app-name-2020`，即可看到登录界面，注册并登录后即可上传和下载文件。

下载的文件在 download 文件夹中
