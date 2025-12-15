#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from database_service import db_service
import random
from datetime import datetime

def generate_test_data():
    """生成50条测试数据"""
    # 中文姓名列表
    first_names = ['张', '李', '王', '刘', '陈', '杨', '赵', '黄', '周', '吴']
    last_names = ['明', '伟', '芳', '娜', '强', '磊', '军', '杰', '超', '鹏', 
                  '秀英', '敏', '静', '丽', '艳', '勇', '浩', '宇', '鑫', '婷']
    
    # 邮箱域名列表
    email_domains = ['gmail.com', 'qq.com', '163.com', '126.com', 'sina.com', 'hotmail.com']
    
    test_data = []
    
    for i in range(50):
        # 生成随机姓名
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name}{last_name}"
        
        # 生成随机邮箱（确保唯一性）
        email = f"{first_name.lower()}{last_name.lower()}{i+1}@{random.choice(email_domains)}"
        
        # 生成随机年龄（18-60岁）
        age = random.randint(18, 60)
        
        test_data.append({
            'name': name,
            'email': email,
            'age': age
        })
    
    return test_data

def add_test_data():
    """向数据库添加测试数据"""
    try:
        # 确保数据库表存在
        db_service.create_table()
        print("✅ 数据库表已创建/确认存在")
        
        # 生成测试数据
        test_data = generate_test_data()
        print(f"📊 生成了 {len(test_data)} 条测试数据")
        
        # 添加数据到数据库
        success_count = 0
        error_count = 0
        
        for i, data in enumerate(test_data, 1):
            try:
                user_id = db_service.add_user(data['name'], data['email'], data['age'])
                print(f"✅ 第 {i} 条数据添加成功: {data['name']} ({data['email']}) - ID: {user_id}")
                success_count += 1
            except Exception as e:
                print(f"❌ 第 {i} 条数据添加失败: {data['name']} - 错误: {str(e)}")
                error_count += 1
        
        print(f"\n📈 数据添加完成:")
        print(f"   ✅ 成功: {success_count} 条")
        print(f"   ❌ 失败: {error_count} 条")
        print(f"   📊 总计: {len(test_data)} 条")
        
        # 验证数据是否成功添加
        try:
            users = db_service.get_all_users()
            print(f"\n🔍 数据库当前共有 {len(users)} 条用户记录")
        except Exception as e:
            print(f"❌ 验证数据时出错: {str(e)}")
            
    except Exception as e:
        print(f"❌ 添加测试数据时发生错误: {str(e)}")

if __name__ == '__main__':
    print("🚀 开始向数据库添加50条测试数据...")
    add_test_data()
    print("\n🎉 测试数据添加任务完成！")