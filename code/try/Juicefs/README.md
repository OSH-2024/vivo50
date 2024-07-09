### 目前部署记录
- 首先安装juicefs，参考`x-FutureWithBuzzyBees`小组，
```bash
curl -sSL https://d.juicefs.com/install | sh -
```
- 然后需要配置redis
> 如果本地化安装，可以修改`redis.conf`文件设置密码和开放端口，然后
   `redis://admin:passwd@disgrafs.redis.rds.aliyuncs.com:6379/1  `中的admin指代用户名，可以省略，直接`redis://:password@....`，@后面的时redis的地址，如果本地化的话一般是端口127.0.0.1:(port)，之前组是部署在了阿里云上，这个提供了redis。 
对下面的配置juicefs
   --storage为oss，则需要设置阿里云bucket，这个我申请了一个，地址为`https://vivo-prime.oss-cn-hangzhou.aliyuncs.com`，然后有access和secretkey，我后续发到群里。

然后创建一下本地JuiceFS，请替换access和secretkey
注：这里的oss
```bash
juicefs format \
    --storage oss \
    --bucket https://disgrafs-prime.oss-cn-hangzhou.aliyuncs.com \
    --access-key AAAAAAAAAAAAAAAAAAc \
    --secret-key ssdadsadsadsadasdsadsadas0U \
    redis://admin:passwd@disgrafs.redis.rds.aliyuncs.com:6379/1  \
    myjfs
```
接着需要运行以下代码，这里的redis需要替换成自己的，后面的`~/Desktop/DisgraFS`是挂载juicefs的文件夹，可自定义。
```bash
sudo juicefs mount redis://admin:passwd@disgrafs.redis.rds.aliyuncs.com:6379/1 ~/Desktop/DisgraFS
```
可能会遇到fuse错误，我下载了fuse之后还是提示没有权限
其他的参考`x-FutureWithBuzzyBees`文档部署客户端。

