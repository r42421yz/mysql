import './App.css';
import React, {useState} from 'react';

function App() {

  // 定义状态变量
  // [状态值（变量， 改变状态的函数] = useState(初始值)
  const [input1, setInput1] = useState('');
  const [input2, setInput2] = useState('');
  const [input3, setInput3] = useState('');
  const [response, setResponse] = useState('');

  const handleGet = async () => {
    // 发GET请求
    const res = await fetch(`http://localhost:5000/api/handle-get?param=${input1}`);
    // 取出响应的JSON
    const data = await res.json();
    setResponse(data.message);
  };

  const handlePost = async () => {
    // 发送POST请求
    const res = await fetch(`http://localhost:5000/api/handle-post?param=${input3}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bodyParam: input2 }),
    });
    const data = await res.json();
    setResponse(data.message);
  };
  

  return (
    <div className="App">
      <div>
        <h2>Flask+React</h2>

        <div>
          <input 
            type="text" placeholder='输入框1 (GET param)' 
            value={input1} onChange={(e)=>setInput1(e.target.value)}
          />
          <button onClick={handleGet}>发送GET请求</button>
        </div>

        <br/>

        <div>
          <input 
            type="text" placeholder='输入框2 (body param)' 
            value={input2} onChange={(e)=>setInput2(e.target.value)}
          />
          <input 
            type="text" placeholder='输入框3 (URL param)' 
            value={input3} onChange={(e)=>setInput3(e.target.value)}
          />
          <button onClick={handlePost}>发送POST请求</button>
        </div>

        <br/>
        <div>响应结果：{response}</div>
      </div>
    </div>
  );
}

export default App;
