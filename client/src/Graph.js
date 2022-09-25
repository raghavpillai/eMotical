import {VictoryChart, VictoryStack, VictoryArea, VictoryTheme} from "victory"
import "./App.css"

const data = [
    {second: 1, positivityScore: 95},
    {second: 2, positivityScore: 25},
    {second: 3, positivityScore: -65},
    {second: 4, positivityScore: 85},
    {second: 5, positivityScore: 75},
]
function Graph(){
    return (
        <VictoryChart theme={VictoryTheme.material} animate={{duration: 1000}}>
            <VictoryStack colorScale={"blue"}>
                <VictoryArea data={data} x="second" y="positivityScore" interpolation={"basis"}/>
            </VictoryStack>
        </VictoryChart>
    )
}

export default Graph