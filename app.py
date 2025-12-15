from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from database_service import db_service

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 直接提供 test_frontend.html 页面
@app.route('/')
def serve_frontend():
    """提供前端页面"""
    return send_from_directory('.', 'test_frontend.html')

# 查询所有用户
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = db_service.get_all_users()
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# 查询单个用户
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = db_service.get_user_by_id(user_id)
        if user:
            return jsonify({'success': True, 'user': user})
        else:
            return jsonify({'success': False, 'error': '用户不存在'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# 添加新用户
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')

    if not name or not email:
        return jsonify({'success': False, 'error': '姓名和邮箱是必填项'}), 400

    try:
        user_id = db_service.add_user(name, email, age)
        return jsonify({'success': True, 'message': '用户添加成功', 'user_id': user_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# 更新用户信息
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')

    try:
        db_service.update_user(user_id, name, email, age)
        return jsonify({'success': True, 'message': '用户更新成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# 删除用户
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        db_service.delete_user(user_id)
        return jsonify({'success': True, 'message': '用户删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# 按条件查询用户
@app.route('/users/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    email = request.args.get('email')
    min_age = request.args.get('min_age')

    try:
        users = db_service.search_users(name, email, min_age)
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # 创建数据库表
    db_service.create_table()
    
    # 启动应用
    app.run(
        host='0.0.0.0',    # 允许外部访问
        port=5001,         # 端口号
        debug=True         # 调试模式
    )