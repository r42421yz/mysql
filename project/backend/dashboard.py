from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from collections import Counter
import re
import sys
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


db = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='baidu',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    cursor = db.cursor()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'message': '用户已存在'}), 400

    hash_pw = generate_password_hash(password)
    insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(insert_query, (username, hash_pw))
    db.commit()
    
    return jsonify({'message': '注册成功'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    cursor = db.cursor()
    
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    if user_data and check_password_hash(user_data['password'], password):
        return jsonify({'message': '登录成功'})
    
    return jsonify({'message': '用户名或密码错误'}), 401

@app.route('/api/chart')
def chart_data():
    chart_type = request.args.get('type')
    cursor = db.cursor()

    if chart_type in ['genres', 'country']:
        field = chart_type
        query = f"SELECT {field} FROM movies"
        cursor.execute(query)
        rows = cursor.fetchall()

        all_items = []
        for row in rows:
            if row[field]:
                items = [item.strip() for item in row[field].split()]
                all_items.extend(items)
        count = Counter(all_items)
        top_items = count.most_common(10)
        return jsonify([{"name":k, "value":v} for k, v in top_items])

    elif chart_type in ['director', 'actors']:
        field = chart_type
        query = f"SELECT {field} FROM movies"
        cursor.execute(query)
        rows = cursor.fetchall()

        all_items = []
        for row in rows:
            raw = row[field]
            if raw:
                items = re.split(r'[/、\xa0]', raw)
                cleaned_items = [clean_name(item) for item in items if clean_name(item)]
                all_items.extend(cleaned_items)

        count = Counter(all_items)
        top_items = count.most_common(10)
        return jsonify([{"name":k, "value":v} for k, v in top_items])

    elif chart_type == 'rating':
        query = "SELECT rating AS name, COUNT(*) AS value FROM movies GROUP BY rating ORDER BY name"
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify(data)
    elif chart_type == 'year':
        query = "SELECT year, COUNT(*) as count FROM movies WHERE year IS NOT NULL GROUP BY year ORDER BY year"
        cursor.execute(query)
        result = cursor.fetchall()
        data = [{'name': str(row['year']), 'value': row['count']} for row in result]

        return jsonify(data)
    else:
        return jsonify([])
    
    
def clean_name(name):
    if not name:
        return None
    name = re.sub(r'\s+[A-Za-z].*$', '', name)
    name = re.sub(r'[\.…\u3000]+.*$', '', name)
    name =  name.strip()
    return name if name else None


if __name__ == '__main__':
    app.run(debug=True)
