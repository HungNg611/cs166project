import {BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Login";
import './App.css';
function App() {

  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
            <Route exact path="/login" exact element={<Login/>}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;