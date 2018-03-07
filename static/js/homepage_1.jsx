class SearchClick extends React.Component { 

    render() {
        return <a href="http://localhost:5001/search"><button id="search-click">
                   Search</button></a>
    }
}

class SignUp extends React.Component { 

    render() {
        return <a href="http://localhost:5001/register"><button id="sign-up">
                   Sign Up</button></a>
    }
}

class Welcome extends React.Component {
    render() { 
        return <div className="welcome">
            <h1>Welcome to PinShop</h1>
            <div className="welcome-button">
                <SearchClick /><SignUp />
            </div>
            </div>
    }
}

ReactDOM.render(
    <Welcome />,
    document.getElementById("root")
);




{/* -- This works so far
class ImageBackground extends React.Component { 

    render() {
        return <img src="https://t4.ftcdn.net/jpg/00/79/84/03/240_F_79840369_XBIgbOK4z6PpHwIH8EweqQDseEa3Ec0c.jpg" />
    }
}

ReactDOM.render(
    <ImageBackground />,
    document.getElementById("root4")
);
*/

/* attempt to create React slideshow */}

{/* Create Slides */}
const IMAGES = [
    "https://images.pexels.com/photos/443088/pexels-photo-443088.jpeg?w=940&h=650&dpr=2&auto=compress&cs=tinysrgb",
    "https://images.pexels.com/photos/674268/pexels-photo-674268.jpeg?h=350&dpr=2&auto=compress&cs=tinysrgb",
    "https://images.pexels.com/photos/48588/pexels-photo-48588.jpeg?w=940&h=650&dpr=2&auto=compress&cs=tinysrgb",
    "https://images.pexels.com/photos/361758/pexels-photo-361758.jpeg?w=940&h=650&dpr=2&auto=compress&cs=tinysrgb"
]

const Slide = (props) => {

    {/*// let background = {
    //     backgroundImage: "https://images.pexels.com/photos/443088/pexels-photo-443088.jpeg?w=940&h=650&dpr=2&auto=compress&cs=tinysrgb",
    //     backgroundSize: 'cover',
    //     backgroundPosition: 'center'  
    // } */}
  {/*return <div className="slide"><img src="https://t4.ftcdn.net/jpg/00/79/84/03/240_F_79840369_XBIgbOK4z6PpHwIH8EweqQDseEa3Ec0c.jpg" /></div>*/}
  return <div className="slide"><img src={props.imgSrc} width="100%" height="auto" /></div>
}


{/* Create Slider React Class */}

class Slider extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
        slideCount: 1
    }

    this.nextSlide = this.nextSlide.bind(this);
    this.previousSlide = this.previousSlide.bind(this);
  }

  componentDidMount() {
    setInterval(this.nextSlide, 3000)
  }

  render() {
    let slide = <Slide imgSrc={IMAGES[this.state.slideCount]} />

    return (

      <div className="slider">

        {slide}

                
      </div>
    );
  }

   nextSlide() {
      this.setState(({slideCount: previousSlideCount}) => {
        let newSlideCount = previousSlideCount + 1
        if (newSlideCount >= this.props.images.length) {
            newSlideCount = 0;}
       

        return {
            slideCount: newSlideCount
        }
    })

    }
    previousSlide() {

      this.setState(({slideCount: previousSlideCount}) => { 
        let newSlideCount = previousSlideCount - 1
        if (newSlideCount < 1) {
            newSlideCount = IMAGES.length - 1;
        }

        return {
            slideCount: newSlideCount
        }

      })
  }
}

ReactDOM.render(
    <Slider images={IMAGES} />,
    document.getElementById("root4")
);
