import './App.css';
import Chat from './chat'
import { useState, useRef, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import YouTube from 'react-youtube';
import home from './icons8-home-24.png'

import bob from './bob.jfif';

const AWS = require("aws-sdk")

AWS.config.update({
  accessKeyId: 'AKIAZEGQS5JFLEEYTFN2',
  secretAccessKey: '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',
  region: 'US-EAST-1'
})

const s3 = new AWS.S3();

function App() {

  let params = useParams();

  function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }

  const [capturing, setCapturing] = useState(false);
  const [session, setSession] = useState(uuidv4());
  const [res, setRes] = useState(null);

  useEffect(() => {
    let video = document.getElementById('video');
    if(video){
      setCapturing(true);
    }
    else{
      setCapturing(false);
    }
  })


  
  
	const start = () => {
    setCapturing(true);
		
		navigator.getUserMedia(
			{
				video: true,
			},
      
			(stream) => {


				let video = document.getElementById('video');
        
				if (video) {
          function capture(){
            var canvas = document.createElement('canvas');
            let video = document.getElementById('video');

            if(!video){
              return;
            }
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
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
      <link rel="preconnect" href="https://fonts.googleapis.com"/>
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
      <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;300&family=Roboto:wght@500&display=swap" rel="stylesheet"/>
      <div className="topbar">
        <div className='logo-container'>
            <a href="/"><img src={home}></img></a>
            <div className="label">eMotical</div>
          </div>
        <div className="avatar-wrapper">
          <img className="avatar" src={bob}></img>
          <p className='label-small'>Hi Hamza!</p>
        </div>

      </div>
      <div className="row-container">
        <div className="screen-wrapper">
          <div className="screen">
              <YouTube
                videoId={params['id']}
                iframeClassName="player"
                opts={opts}
                onPlay={start}
                onPause={stop}
                onEnd={stop} 
              />

            {capturing && 
              <video
                muted
                autoPlay
                id="video">
              </video>
            }
          </div>

          <div className="media">Category: {params['type']}</div>
          <div className='spacer'></div>
          <div className="author-wrapper">
            <div className="author"></div>
            <div className="author-label">Video {params['item']}</div>
            <a className='submit' href={`/report/${session}`}>Submit</a>
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