import "./App.css";
import { Routes, Route } from "react-router-dom";
import HomeSwitch from "./components/HomeSwitch";
import Register from "./screens/Register";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomeSwitch />} />
      <Route path="register" element={<Register />} />
    </Routes>
  );
}

export default App;
