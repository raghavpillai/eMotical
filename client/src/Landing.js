import './App.css'
import Youtube from 'react-youtube'
import { useNavigate } from 'react-router-dom'
import home from './icons8-home-24.png'
import { useState, useEffect } from 'react'

function Landing(){
    const navigate = useNavigate();

    const [videos, setVideo] = useState([])

    useEffect(() =>{
        fetch('http://127.0.0.1:8000/v1/emotions/get_recs/cars', {
            method: 'GET',
            headers:{
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        })
        .then((res) => (res.json()))
        .then((data) => setVideo(data))
        .catch((errors) => console.log(errors))

    }, [])

    return (
        <div className="container">
            <div className="topbar">
                <div className='logo-container'>
                    <a href="/"><img src={home}></img></a>
                    <div className="label"><strong>eMotical</strong></div>
                </div>
                <div className="avatar-wrapper">
                    <a className="avatar"></a>
                </div>
            </div>
            
            {videos[0] &&
            
            <div className='tile-container'>
                <p className='section-title'>Cars</p>
                <div className='tile-videos'>
                    
                    {videos.map((video, idx) => (
                        <div className='watch-tile-wrapper' key={idx}>
                            <a className='watch-button' href={"/view/"+ video + "/" + idx + '/car'}>
                                <Youtube videoId={video} iframeClassName="player small"/>
                            </a>
                        </div>
                    ))}
                </div>
            </div>
            }
        </div>
    )
}

export default Landing;