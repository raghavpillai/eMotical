import * as React from "react";
import c from "classnames";
import "./like.css";

class Like extends React.Component {
  state = {
    likeActive: false,
    dislikeActive: false,
  };

  setDislike() {
    this.setState({
      dislikeActive: !this.state.dislikeActive,
    });
  }
  setLike() {
    this.setState({
      likeActive: !this.state.likeActive,
    });
  }

  handleLike() {
    if (this.state.dislikeActive) {
      this.setLike();
      this.setDislike();
    }
    this.setLike();
  }

  handleDislike() {
    if (this.state.likeActive) {
      this.setDislike();
      this.setLike();
    }
    this.setDislike();
  }

  render() {
    return (
      <>
        <button
          onClick={() => this.handleLike()}
          className={c({ ["active"]: this.state.likeActive })}
        >
          {this.state.like}
        </button>
        <button
          className={c({ ["active"]: this.state.dislikeActive })}
          onClick={() => this.handleDislike()}
        >
          {this.state.dislike}
        </button>
      </>
    );
  }
}
