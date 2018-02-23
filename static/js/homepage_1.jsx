class Welcome extends React.Component {
    render() {
        return <h1>Welcome to PinShop!</h1>
    }
}

ReactDOM.render(
    <Welcome />,
    document.getElementById("root")
);

class Clicker extends React.Component { 

    render() {
        return <a href="http://localhost:5001/search"><button>
                   Search!</button></a>
    }
}

ReactDOM.render(
    <Clicker />,
    document.getElementById("root2")
);