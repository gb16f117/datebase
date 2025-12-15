import pymysql
from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.connection_params = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '123qwe?!',  # MySQL密码
            'database': 'student_db',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'port': 3306
        }

    def get_db_connection(self):
        """获取数据库连接"""
        return pymysql.connect(**self.connection_params)

    def create_table(self):
        """创建用户表（如果不存在）"""
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    age INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql)
            connection.commit()
        finally:
            connection.close()

    def get_all_users(self):
        """查询所有用户"""
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
                return users
        except Exception as e:
            raise Exception(f"查询用户失败: {str(e)}")
        finally:
            connection.close()

    def get_user_by_id(self, user_id):
        """根据ID查询单个用户"""
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                return user
        except Exception as e:
            raise Exception(f"查询用户失败: {str(e)}")
        finally:
            connection.close()

    def add_user(self, name, email, age=None):
        """添加新用户"""
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, email, age))
            connection.commit()
            return cursor.lastrowid
        except pymysql.IntegrityError:
            raise Exception("邮箱已存在")
        except Exception as e:
            raise Exception(f"添加用户失败: {str(e)}")
        finally:
            connection.close()

    def update_user(self, user_id, name, email, age=None):
        """更新用户信息"""
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查用户是否存在
                cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
                if not cursor.fetchone():
                    raise Exception("用户不存在")

                sql = "UPDATE users SET name = %s, email = %s, age = %s WHERE id = %s"
                cursor.execute(sql, (name, email, age, user_id))
            connection.commit()
        except pymysql.IntegrityError:
            raise Exception("邮箱已存在")
        except Exception as e:
            raise Exception(f"更新用户失败: {str(e)}")
        finally:
            connection.close()

    def delete_user(self, user_id):
        """删除用户"""
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查用户是否存在
                cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
                if not cursor.fetchone():
                    raise Exception("用户不存在")

                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
        except Exception as e:
            raise Exception(f"删除用户失败: {str(e)}")
        finally:
            connection.close()

    def search_users(self, name=None, email=None, min_age=None):
        """按条件搜索用户"""
        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 设置连接字符集为utf8mb4
                cursor.execute("SET NAMES utf8mb4")
                cursor.execute("SET CHARACTER SET utf8mb4")
                
                sql = "SELECT * FROM users WHERE 1=1"
                params = []

                if name:
                    sql += " AND name LIKE %s"
                    params.append(f"%{name}%")
                if email:
                    sql += " AND email LIKE %s"
                    params.append(f"%{email}%")
                if min_age:
                    sql += " AND age >= %s"
                    params.append(int(min_age))

                cursor.execute(sql, params)
                users = cursor.fetchall()
                return users
        except Exception as e:
            raise Exception(f"搜索用户失败: {str(e)}")
        finally:
            connection.close()

# 创建全局数据库服务实例
db_service = DatabaseService()