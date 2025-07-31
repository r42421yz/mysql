import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, Tabs, message, Card } from 'antd';
import axios from 'axios';


function LoginRegister() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();


  const onFinish = async (values, type) => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const res = await axios.post(`http://localhost:5000/${type}`, values);
      setSuccess(res.data.message || '成功')

      if (type == 'login'){
        navigate('/dashboard');
      }else{
        navigate('/');
      }
    } catch (err) {
      setError(err.response?.data?.message || '请求失败');
    }
    setLoading(false);
  };

const loginForm = (
    <Form onFinish={(v) => onFinish(v, 'login')} layout="vertical">
      <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="password" label="密码" rules={[{ required: true }]}>
        <Input.Password />
      </Form.Item>
      <Form.Item>
        <Button htmlType="submit" type="primary" block loading={loading}>
          登录
        </Button>

      </Form.Item>
    </Form>
  )

const registerForm = (
    <Form onFinish={(v) => onFinish(v, 'register')} layout="vertical">
      <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="password" label="密码" rules={[{ required: true, min: 6 }]}>
        <Input.Password />
      </Form.Item>
      <Form.Item>
        <Button htmlType="submit" type="primary" block loading={loading}>
          注册
        </Button>
      </Form.Item>
    </Form>
  );

  return (
    <Card title="用户系统" style={{ maxWidth: 400, margin: '100px auto' }}>
        {error && <div style = {{color : 'red', marginBottom: 16}}>{error}</div>}
        {success && <div style = {{color : 'green', marginBottom: 16}}>{success}</div>}

      <Tabs 
        defaultActiveKey="login"
        items = {[
            {
                key : 'login',
                label : '登录',
                children : loginForm,
            },
            {
                key : 'register',
                label : '注册',
                children : registerForm,
            }
        ]}
        >
        
      </Tabs>
    </Card>
  );
}

export default LoginRegister;
