# 基于机器学习的中药处方分析预测疾病的系统

## 项目概述

这是一个基于Flask的中医诊断系统，旨在通过机器学习算法，根据输入的中药处方预测可能的疾病。该系统集成了用户认证、诊断功能、历史记录查看以及管理员后台等功能，为中医诊断提供了一个现代化的辅助工具。
```mermaid
graph TD
    A[用户输入处方] --> B[NLP处理]
    B --> C[数据库查询]
    C --> D[机器学习模型]
    D --> E[疾病预测结果]
    F[(中药数据库)] --> C
    G[(疾病数据库)] --> C
    H[(处方数据库)] --> C
    I[模型训练] --> D
    F --> I
    G --> I
    H --> I
  ```

## 功能特点

- 用户认证系统
  - 用户注册
  - 用户登录
  - 用户登出
- 中药处方诊断
  - 输入中药处方
  - 使用机器学习算法（决策树）预测可能的疾病
- 诊断历史记录
  - 查看个人诊断历史
- 管理员后台
  - 添加新的中药
  - 添加新的疾病
  - 建立中药和疾病之间的关联
- 数据可视化（待实现）
  - 诊断结果的图表展示

## 技术栈

- 后端：Python 3.7+，Flask框架
- 数据库：SQLite（通过SQLAlchemy ORM操作）
- 前端：HTML, CSS (Bootstrap), JavaScript
- 机器学习：scikit-learn
- 认证：Flask-Login
- 表单处理：Flask-WTF

## 安装说明

1. 克隆仓库：
```
git clone https://github.com/your-username/tcm-diagnosis-system.git
cd tcm-diagnosis-system
```
2. 创建并激活虚拟环境：
```python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
```
3. 安装依赖：
pip install -r requirements.txt
4. 初始化数据库：
```python
from app import app, db
from models import User, Herb, Disease, HerbDiseaseAssociation

with app.app_context():
    db.create_all()

    # 创建管理员用户
    admin = User(username='admin', email='admin@example.com', is_admin=True)
    admin.set_password('adminpassword')
    db.session.add(admin)
    db.session.commit()
```

## 使用方法

运行应用：
```python app.py ```

在浏览器中访问 http://localhost:5000

使用管理员账户登录（用户名：admin，密码：adminpassword）或注册新用户

管理员可以在后台添加中药、疾病和它们之间的关联

普通用户可以输入中药处方，系统会预测可能的疾病

用户可以查看自己的诊断历史
