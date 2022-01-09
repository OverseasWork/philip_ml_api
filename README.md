### step1
#### 构建环境
cd scripts/ </n>
source env.sh </n>

### step2
#### 启动服务
cd scripts/ </n>
source start.sh </n>

### step3
### Nginx负载均衡
nginx 监听 master:8005，分布转发 master:8004，node:8004

### 接口文档说明
http://0.0.0.0:8005/docs