import './App.css'
import { useState } from 'react';



function Chat(){
    const [arr, setArr] = useState([]);

    const handleSubmit = (event) =>{
        if(event.target===document.getElementById("input") && event.code !== 'Enter'){
            return
        }

        let obj = {name: 'User', message: document.getElementById("input").value};

        setArr(curr => [...curr, obj]);

        if(arr.length >= 5){
            setArr((arr) => arr.filter((_, index) => index !== 0))
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