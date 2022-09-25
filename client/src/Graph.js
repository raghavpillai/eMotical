import { VictoryChart, VictoryStack, VictoryArea, VictoryTheme } from "victory";
import "./App.css";

const data = [
  { second: 1, positivityScore: 95 },
  { second: 2, positivityScore: 25 },
  { second: 3, positivityScore: -65 },
  { second: 4, positivityScore: 85 },
  { second: 5, positivityScore: 75 },
];

function Graph() {
  return (
    <VictoryChart
      theme={VictoryTheme.material}
      animate={{
        duration: 2000,
        onLoad: { duration: 1000 },
      }}
    >
      <VictoryLine
        style={{
          data: { stroke: "#c43a31" },
          parent: { border: "1px solid #ccc" },
        }}
        data={data}
      />
    </VictoryChart>
  );
}

export default Graph;
