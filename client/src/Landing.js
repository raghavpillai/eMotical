import './App.css'
import Youtube from 'react-youtube'
import { useNavigate } from 'react-router-dom'

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
                <div className="label">eMotical</div>
                <div className="avatar-wrapper">
                    <a className="avatar"></a>
                </div>
            </div>
            <p className='section-title'>Cars</p>

            <div className='row-container small'>
                
                {videoList.map((video) => (
                    <div className='watch-tile-wrapper'>
                        <a className='watch-button' href={"/view/"+ video.id}>
                            <Youtube videoId={video.id} iframeClassName="player small"/>
                        </a>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Landing;