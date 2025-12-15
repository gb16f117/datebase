# 用户管理API文档

## 概述

这是一个基于Flask的用户管理系统API，提供完整的用户CRUD操作功能。系统使用MySQL数据库存储用户数据，支持中文字符编码。

### 服务信息
- **基础URL**: `http://localhost:5001` 或 `http://你的公网IP:5001`
- **数据格式**: JSON
- **字符编码**: UTF-8
- **跨域支持**: 已启用CORS

---

## 数据库表结构

### users表
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- 用户ID（主键）
    name VARCHAR(100) NOT NULL,                 -- 姓名（必填）
    email VARCHAR(100) UNIQUE NOT NULL,         -- 邮箱（必填，唯一）
    age INT,                                     -- 年龄（可选）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 创建时间
)
```

---

## API接口详情

### 1. 前端页面访问

#### 获取测试页面
```http
GET /
```

**描述**: 获取API测试前端页面

**响应**: HTML页面

---

### 2. 用户管理接口

#### 2.1 获取所有用户

```http
GET /users
```

**描述**: 查询所有用户信息

**响应示例**:
```json
{
    "success": true,
    "users": [
        {
            "id": 1,
            "name": "张三",
            "email": "zhangsan@example.com",
            "age": 25,
            "created_at": "2025-12-12T05:35:45Z"
        },
        {
            "id": 2,
            "name": "李四",
            "email": "lisi@example.com",
            "age": 30,
            "created_at": "2025-12-12T05:36:12Z"
        }
    ]
}
```

**错误响应**:
```json
{
    "success": false,
    "error": "查询用户失败: [具体错误信息]"
}
```

---

#### 2.2 获取单个用户

```http
GET /users/{user_id}
```

**路径参数**:
- `user_id` (int): 用户ID

**描述**: 根据ID获取指定用户信息

**响应示例**:
```json
{
    "success": true,
    "user": {
        "id": 1,
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25,
        "created_at": "2025-12-12T05:35:45Z"
    }
}
```

**错误响应**:
```json
{
    "success": false,
    "error": "用户不存在"
}
```

**状态码**: 404（用户不存在）

---

#### 2.3 添加新用户

```http
POST /users
```

**Content-Type**: `application/json`

**请求体**:
```json
{
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 25
}
```

**字段说明**:
- `name` (string, 必填): 用户姓名
- `email` (string, 必填): 用户邮箱（必须唯一）
- `age` (int, 可选): 用户年龄

**响应示例**:
```json
{
    "success": true,
    "message": "用户添加成功",
    "user_id": 3
}
```

**错误响应**:
```json
{
    "success": false,
    "error": "姓名和邮箱是必填项"
}
```

**状态码**: 400（缺少必填字段）

```json
{
    "success": false,
    "error": "邮箱已存在"
}
```

---

#### 2.4 更新用户信息

```http
PUT /users/{user_id}
```

**路径参数**:
- `user_id` (int): 用户ID

**Content-Type**: `application/json`

**请求体**:
```json
{
    "name": "张三丰",
    "email": "zhangsanfeng@example.com",
    "age": 28
}
```

**字段说明**:
- `name` (string): 更新的姓名
- `email` (string): 更新的邮箱（必须唯一）
- `age` (int): 更新的年龄

**响应示例**:
```json
{
    "success": true,
    "message": "用户更新成功"
}
```

**错误响应**:
```json
{
    "success": false,
    "error": "用户不存在"
}
```

```json
{
    "success": false,
    "error": "邮箱已存在"
}
```

---

#### 2.5 删除用户

```http
DELETE /users/{user_id}
```

**路径参数**:
- `user_id` (int): 用户ID

**描述**: 删除指定用户

**响应示例**:
```json
{
    "success": true,
    "message": "用户删除成功"
}
```

**错误响应**:
```json
{
    "success": false,
    "error": "用户不存在"
}
```

---

#### 2.6 按条件搜索用户

```http
GET /users/search?name=张&email=example&min_age=20
```

**查询参数** (所有参数都是可选的):
- `name` (string): 按姓名模糊搜索
- `email` (string): 按邮箱模糊搜索  
- `min_age` (int): 最小年龄筛选

**描述**: 支持多条件组合搜索用户

**响应示例**:
```json
{
    "success": true,
    "users": [
        {
            "id": 1,
            "name": "张三",
            "email": "zhangsan@example.com",
            "age": 25,
            "created_at": "2025-12-12T05:35:45Z"
        }
    ]
}
```

**错误响应**:
```json
{
    "success": false,
    "error": "搜索用户失败: [具体错误信息]"
}
```

---

## 通用响应格式

### 成功响应
```json
{
    "success": true,
    "data": ...  // 具体数据或message
}
```

### 错误响应
```json
{
    "success": false,
    "error": "错误描述信息"
}
```

---

## 部署信息

### 环境要求
- Python 3.9+
- MySQL 5.7+
- Flask 2.0+
- PyMySQL

### 启动方式
```bash
python app.py
```

### 服务配置
- **监听地址**: 0.0.0.0（允许外部访问）
- **端口**: 5001
- **调试模式**: 启用

### 数据库配置
- **主机**: 127.0.0.1
- **端口**: 3306
- **数据库**: student_db
- **字符集**: utf8mb4（支持中文和特殊字符）

---

## 测试说明

系统提供了完整的前端测试页面 (`/`)，可以直接在浏览器中进行API测试，包括：
- 用户列表查看
- 添加新用户
- 编辑用户信息
- 删除用户
- 条件搜索

---

## 注意事项

1. **邮箱唯一性**: 系统强制邮箱地址唯一，添加或更新时重复邮箱会失败
2. **数据验证**: 姓名和邮箱为必填字段
3. **字符编码**: 全面支持中文字符和特殊符号
4. **错误处理**: 所有API接口都包含完整的异常处理机制
5. **跨域支持**: 已启用CORS，支持跨域请求

---

## API使用示例

### 使用curl测试

```bash
# 获取所有用户
curl http://localhost:5001/users

# 添加新用户
curl -X POST http://localhost:5001/users \
  -H "Content-Type: application/json" \
  -d '{"name":"王五","email":"wangwu@example.com","age":32}'

# 更新用户
curl -X PUT http://localhost:5001/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"张三丰","email":"zhangsanfeng@example.com","age":28}'

# 删除用户
curl -X DELETE http://localhost:5001/users/1

# 搜索用户
curl "http://localhost:5001/users/search?name=张&min_age=25"
```

### 使用JavaScript fetch

```javascript
// 获取所有用户
fetch('http://localhost:5001/users')
  .then(response => response.json())
  .then(data => console.log(data));

// 添加新用户
fetch('http://localhost:5001/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: '王五',
    email: 'wangwu@example.com',
    age: 32
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

*文档最后更新时间: 2025-12-12*