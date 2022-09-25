import './App.css'
import Youtube from 'react-youtube'
import { useNavigate } from 'react-router-dom'
import home from './icons8-home-24.png'

const videoList = [
    {id: "fPYho_m142c"}, 
    {id: "eMpszInH0xw"}, 
    {id: "gCMQS3UDabo"}, 
    {id: "YqvOHgBhnBU"}, 
    {id: "9MRmNDDp5i8"}
]



function Landing(){
    const navigate = useNavigate();

    function openView(id){
        window.location.href = "/view/"+ id;
    }

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
            

            <div className='tile-container'>
                <p className='section-title'>Cars</p>
                <div className='tile-videos'>
                    
                    {videoList.map((video, idx) => (
                        <div className='watch-tile-wrapper' key={idx}>
                            <a className='watch-button' href={"/view/"+ video.id + "/" + idx + '/car'}>
                                <Youtube videoId={video.id} iframeClassName="player small"/>
                            </a>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default Landing;