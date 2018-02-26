class Welcome extends React.Component {
    render() {
        return <h1>Welcome to PinShop!</h1>
    }
}

ReactDOM.render(
    <Welcome />,
    document.getElementById("root")
);

class SearchClick extends React.Component { 

    render() {
        return <a href="http://localhost:5001/search"><button>
                   Search!</button></a>
    }
}

ReactDOM.render(
    <SearchClick />,
    document.getElementById("root2")
);

class SignUp extends React.Component { 

    render() {
        return <a href="http://localhost:5001/register"><button>
                   Sign Up!</button></a>
    }
}

ReactDOM.render(
    <SignUp />,
    document.getElementById("root3")
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

const SlideOne = (props) => {
  return <div className="slide"><img src="https://t4.ftcdn.net/jpg/00/79/84/03/240_F_79840369_XBIgbOK4z6PpHwIH8EweqQDseEa3Ec0c.jpg" /></div>
}

const SlideTwo = (props) => {
  return <div className="slide"><img src="https://www.purseblog.com/images/2015/01/Purseonals-Chanel-Reissue-227-2.jpg" /></div>
}

const SlideThree = (props) => {
  return <div className="slide"><img src="http://weandthecolor.com/wp-content/uploads/2012/11/Black-and-White-Fashion-Photography-by-Riccardo-Vimercati-2343668.jpg" /></div>
}

{/* Create Arrows */}

const RightArrow = (props) => {
  return (
    <div onClick={props.nextSlide} className="nextArrow">
      <i className="fa fa-arrow-right fa-2x" aria-hidden="true"></i>
    </div>
  );
}

const LeftArrow = (props) => {
  return (
     <div onClick={props.previousSlide} className="backArrow">
      <i className="fa fa-arrow-left fa-2x" aria-hidden="true"></i>
    </div>
  );
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

  render() {
    return (
      <div className="slider">

        { this.state.slideCount === 1 ? <SlideOne /> : null }
        { this.state.slideCount === 2 ? <SlideTwo /> : null }
        { this.state.slideCount === 3 ? <SlideThree /> : null }

        <RightArrow nextSlide={this.nextSlide} />
        <LeftArrow previousSlide={this.previousSlide} />
                
      </div>
    );
  }

   nextSlide() {
      this.setState({ slideCount: this.state.slideCount + 1 })

    }
    previousSlide() {
      this.setState({ slideCount: this.state.slideCount - 1 })
  }
}

ReactDOM.render(
    <Slider />,
    document.getElementById("root4")
);
