import './App.css'
import { useState } from 'react';



function Chat(){
    const [arr, setArr] = useState([]);
    const [res, setRes] = useState([]);

    const handleSubmit = (event) =>{
        if(event.target===document.getElementById("input") && event.code !== 'Enter'){
            return
        }
        
        var sender;

        let obj = {name: 'User', message: document.getElementById("input").value};
        
        setArr(curr => [...curr, obj]);
        
        fetch('http://127.0.0.1:8000/v1/emotions/chat/', {
            method: 'GET',
            headers:{
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: {
                'message': obj.message
            }
        })
        .then((res) => (res.json()))
        .then((data) => setRes(data))

        if(arr.length >= 5){
            setArr((arr) => arr.filter((_, index) => index !== 0))
        }
        
        if(document.getElementById("input").value === "I am not happy"){
            sender = {name: 'Sender', message: "Why are you not happy?"}
        }
        else if(document.getElementById("input").value === "I am sad"){
            sender = {name: 'Sender', message: "Why are you upset?"}
        }
        else if(document.getElementById("input").value === "This makes me upset"){
            sender = {name: 'Sender', message: "What about it makes you upset"}
        }
        else if(document.getElementById("input").value === "This makes me happy"){
            sender = {name: 'Sender', message: "I am glad this makes you happy"}
        }

        if(sender){
            setArr(curr => [...curr, sender]);
        }

        document.getElementById("input").value = ""
    }
    
    const getSide = (obj) => {
        if(obj === 'Sender'){
            return 'message-wrapper float-left'
        }
        return 'message-wrapper float-right'
    }

    return (
        <div className='container-3'>
            <div className="chat-wrapper">
                {arr.map((convo) => (
                    <div className={getSide(convo.name)}>
                        <div className='chat-bubble'>
                            <h3>{convo.name}</h3>
                            <p>{convo.message}</p>
                        </div>
                    </div>
                ))}
            </div>

            <div className = "input-wrapper">
                <input className="text-input" id="input" type="text" onKeyDown={handleSubmit}></input>
                <submit className="input-submit" onClick={handleSubmit}>Send</submit>
            </div>

        </div>
    )
}

export default Chat;