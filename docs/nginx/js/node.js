const express = require('express');
const app = express();

// 添加跨域支持
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

// 定义路由
app.get('/', (req, res) => {
  res.send('Hello, world! This is from Node.js server.port:8001');
});

// 监听端口
const PORT = 8002;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

