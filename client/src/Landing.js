import './App.css'
import Youtube from 'react-youtube'

const videoList = [
    {id: "fPYho_m142c"}, 
    {id: "eMpszInH0xw"}, 
    {id: "gCMQS3UDabo"}, 
    {id: "YqvOHgBhnBU"}, 
    {id: "9MRmNDDp5i8"}
]

function Landing(){
    return (
        <div className="container">
            <div className="topbar">
                <div className="label">CarMotion</div>
                <div className="avatar-wrapper">
                    <a className="avatar"></a>
                </div>
            </div>

            <div>
                {videoList.map((video) => (
                    <div>
                        <Youtube videoId={video.id} iframeClassName="player"/>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Landing;