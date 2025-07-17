from flask import Flask, request, jsonify
from flask_cors import CORS 

# 创建一个Flask应用实例
app = Flask(__name__)
# 给flask app加上跨域支持，允许前端访问不同端口的后端接口
CORS(app)

@app.route('/api/handle-get', methods=['GET'])
def handle_get():
    param = request.args.get('param')
    return jsonify({"message":f"参数是{param}"})

@app.route('/api/handle-post', methods=['POST'])
def handle_post():
    param = request.args.get('param')
    data = request.get_json()
    body_param = data.get('bodyParam')
    return jsonify({"message":f"body中的参数是{body_param}, param中的参数是{param}"})

if __name__ == "__main__":
    app.run(debug=True)