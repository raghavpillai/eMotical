import './App.css'

const conversationArray = [
    {name: "Sender", message: "How do you feel about this car?"},
    {name: "User", message: "I don't feel good about this car."},
    {name: "Sender", message: "Why are you upset?"},
    {name: "User", message: "I want something more sporty"}
];

function Chat(){
    return (
        <div className="chat-wrapper">
            {conversationArray.map((convo) => (
                <div className="chat-bubble">
                    <h3>{convo.name}</h3>
                    <p>{convo.message}</p>
                </div>
            ))}
        </div>
    )
}

export default Chat;