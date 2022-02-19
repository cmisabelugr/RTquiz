import React from "react";

class BackgroundVideo extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            hola : props.hola,
        };
        this.veces = 0;
    }

    componentDidMount(){
        console.log("Inicializando Video, conectando a MediaSoup y tal...")
    }
    componentDidUpdate(){
        console.log("El video se ha actualizado por su estado " + this.veces)
        this.veces +=1;
    }

    render(){
        return(
            <p>Imagina que esto es un video to tocho en directo.</p>
            
        )
    }
}

export default BackgroundVideo;