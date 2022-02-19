import React from "react";
import GameContainer from "./GameContainer";
class RTQuizClient extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            username : '',
            count: 0,
        };
    }

    componentDidMount(){
        console.log("Inicializando App...")
    }

    render(){
        return(
            <div className="RTQuizContainer" >
            <h1>RTQuiz</h1>
            <button onClick={() => this.setState({ count: this.state.count + 1 })}>
          Actualiza el prop del GameContainer
        </button>
        <GameContainer hola={this.state.count} />
            </div>
        )
    }
}

export default RTQuizClient;