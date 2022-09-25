import './App.css';
import { useState, useRef, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import home from './icons8-home-24.png'
import bob from './bob.jfif';
import { VictoryChart, VictoryAxis, VictoryBar, VictoryTheme, VictoryPie} from "victory";
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';


function Dashboard () {
    let params = useParams();
    const session = params['session']
    const [state, setState] = useState(false);
    const percentage = state[1];

    useEffect(()=>{
        fetch(`http://127.0.0.1:8000/v1/emotions/create/${session}`,{
            headers: {
                'Accept': 'application/json',
                'Content-type': 'application/json'
            },
            method: "POST"
          })
          .then((res) => (res.json()))
          .then((res) => console.log(res))
          .catch((err) => (console.log(err)))
      
          fetch('http://127.0.0.1:8000/v1/emotions/end_session',{
              headers: {
                  'Accept': 'application/json',
                  'Content-type': 'application/json'
              },
              method: "GET"
          })
          .then((res) => (res.json()))
          .then((res) => {
            setState(res)
            console.log(res)
          })
          .catch((err) => (console.log(err)))


    }, [])

    const Graph = ( props ) => {
      var angry = []
      var calm = []
      var confused = []
      var disgusted = []
      var fear = []
      var happy = []
      var sad = []
      var surprised = []
      for(let i=0; i < props.data[2]['array'].length-1; i++){
        angry.push({time: i, confidence: props.data[2]['array'][i].angry})
        calm.push({time: i, confidence: props.data[2]['array'][i].calm})
        confused.push({time: i, confidence: props.data[2]['array'][i].confused})
        disgusted.push({time: i, confidence: props.data[2]['array'][i].disgusted})
        fear.push({time: i, confidence: props.data[2]['array'][i].fear})
        happy.push({time: i, confidence: props.data[2]['array'][i].happy})
        sad.push({time: i, confidence: props.data[2]['array'][i].sad})
        surprised.push({time: i, confidence: props.data[2]['array'][i].surprised})
      }

      const items=[angry, calm, confused, disgusted, fear, happy, sad, surprised]
      return (
        <>
        <VictoryChart domainPadding={20} theme={VictoryTheme.material} animate={{ duration: 1000 }}>
          <VictoryAxis colorScale={"warm"}>
          <VictoryAxis
            tickValues={[0, 5, 10, 15]}
            tickFormat={[0, 5, 10, 15]}
          />
          </VictoryAxis>
          <VictoryAxis
            dependentAxis
            tickFormat={(x) => (100*x)}
          />
          <VictoryBar data={happy}x="time"y="confidence"/>
        </VictoryChart>
        </>
      );
    }


    return(
      <div>
        {state !==false && 
          <>
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

          <Graph data={state}/>

          <CircularProgressbar className="status" value={Math.round(percentage)} text={`${Math.round(percentage)}%`} />;
          <p>Customer Satisfaction</p>
          </>
        }
      </div>

    )
}

export default Dashboard;