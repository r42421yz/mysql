import React, { useState } from "react";

function Predict(){
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [result, setResult] = useState(null);

    const handleFileChange = (e) => {
        const f = e.target.files[0]
        if(f){
            setFile(f);
            setPreview(URL.createObjectURL(f));
        }
    };

    const handleUpload = async () => {
        if (!file) {
            alert ("请先选择一张图片");
            return;
        }
    

    const formData = new FormData();
    formData.append("file", file);

    try{
        const res = await fetch("http://127.0.0.1:5000/predict", {
            method : "POST",
            body : formData,
        });
        const data = await res.json();
        setResult(data);
    }catch (err) {
        console.error(err);
        setResult({error : "请求失败：" + err.message});
    }
};

return (
    <div style = {{padding:20, fontFamily: "Arial"}}>
        <h2>手写数字识别</h2>

        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleUpload} style={{marginLeft: 10}}>
            上传并识别
        </button>

        {preview && (
            <div style={{margin:20}}>
                <p>预览:</p>
                <img
                    src = {preview}
                    alt = "preview"
                    style={{maxWidth:200, border:"1px solid #cc"}}
                />
            </div>
        )}

        {result && (
            <div style={{marginTop:20}}>
                {result.error ? (
                    <p style={{color:"red"}}>{result.error}</p>
                ):(
                    <>
                        <p>
                            预测结果：<b>{result.label}</b>
                        </p>
                    </>
                )}
            </div>
        )}
    </div>
    );
}

export default Predict;