import logo from './logo.svg';
import './App.css';
import Chat from './chat'
import { useState, useRef, useEffect } from 'react'
import YouTube from 'react-youtube';

const AWS = require("aws-sdk")

AWS.config.update({
  accessKeyId: 'AKIAZEGQS5JFLEEYTFN2',
  secretAccessKey: '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',
  region: 'US-EAST-1'
})

const s3 = new AWS.S3();

function App() {
  const [capturing, setCapturing] = useState(false);

  useEffect(() => {
    let video = document.getElementById('video');
    if(video){
      setCapturing(true);
    }
    else{
      setCapturing(false);
    }
  })

  function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }
  

  const session = uuidv4();
  
	const start = () => {
    setCapturing(true);
		
		navigator.getUserMedia(
			{
				video: true,
			},
      
			(stream) => {


				let video = document.getElementById('video');
        var canvas = document.createElement('canvas');
				if (capturing) {
          function capture(){
            
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            var ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            let link = canvas.toDataURL('image/png');

            console.log(link)
  
            const id = uuidv4()
            if(link){
              (async () =>{
                await s3.putObject({
                    Body: link,
                    Bucket: `carmotion-videos/${session}`,
                    Key: `${id}.txt`
                  }).promise();
                })(); 
            }
          }


					video.srcObject = stream;
          setInterval(capture, 500);
				}

        
			},
			(err) => console.error(err)
		);
	};

  const stop = () => {
		setCapturing(false);
		let video = document.getElementById('video');
		video.srcObject.getTracks()[0].stop();
	};

  var opts;


  return (
    <div className="container">
      <div className="topbar">
        <div className ="label">CarMotion</div>
        <div className="avatar-wrapper">
          <a className="avatar"></a>
        </div>

      </div>
      <div className="row-container">
        <div className="screen-wrapper">
          <div className="screen">
              <YouTube
                videoId="2g811Eo7K8U"
                iframeClassName="player"
                opts={opts}
                onPlay={start}
                onPause={stop}
                onEnd={stop} 
              />

              <video
                muted
                autoPlay
                id="video">
              </video>
          </div>

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