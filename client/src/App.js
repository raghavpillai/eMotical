import logo from './logo.svg';
import './App.css';
import Chat from './chat'

function App() {
  return (
    <div className="container">
      <div className="topbar">
        <div className ="label">CarMotion</div>
        <div className="avatar-wrapper">
          <a className="avatar">a</a>
        </div>

      </div>
      <div className="row-container">
        <div className="screen-wrapper">
          <div className="screen">Hi!</div>
          <div className="media">Media</div>
          <div className="author-wrapper">
            <div className="author"></div>
            <div className="author-label">Doug Demurro</div>
          </div>

        </div>
        <div className="chat">
          <Chat/>
        </div>
      </div>
    </div>

  );
}

export default App;
