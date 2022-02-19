import React from "react";
import BackgroundVideo from "./BackgroundVideo";
class GameContainer extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            hola : props.hola,
        };
    }

    componentDidMount(){
        console.log("Inicializando GameContainer...")
    }

    componentDidUpdate(){
        console.log("El GameContainer se ha actualizado")
    }

    render(){
        return(
            <div id="game-container">
            <p>{this.props.hola}</p>
            <BackgroundVideo />
            </div>
        )
    }
}

export default GameContainer;