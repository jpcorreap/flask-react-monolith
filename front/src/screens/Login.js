import { Grid, TextField, Button, Alert } from "@mui/material";
import React, { useState } from "react";
import logo from "../assets/full_size_logo.png";
import { Link } from "react-router-dom";
import useFetchRequest from "../hooks/useFetchRequest";

function Login() {
  const [state, setState] = useState({ email: "", password: "" });
  const { post } = useFetchRequest();

  const handleChange = (e) => {
    setState({ ...state, [e.currentTarget.id]: e.currentTarget.value });
  };

  const handleLogin = () => {
    console.info(state);
    post("http://localhost:5000/auth/login", state)
      .then((response) => response.json())
      .then((response) => localStorage.setItem("token", response.token));
  };

  return (
    <Grid
      container
      direction="column"
      justifyContent="center"
      alignItems="center"
      style={{ backgroundColor: "#ECE9E8" }}
    >
      <Grid
        container
        direction="column"
        justifyContent="center"
        alignItems="center"
        style={{
          backgroundColor: "#fff",
          minHeight: "20vh",
          width: "100vw",
        }}
      >
        <img src={logo} alt="" width={400} />
      </Grid>
      <Grid
        container
        direction="column"
        justifyContent="center"
        alignItems="center"
        style={{
          backgroundColor: "#ECE9E8",
          minHeight: "80vh",
          width: "98vw",
        }}
      >
        <h1 style={{ color: "#978C87" }}>Ingreso de usuarios</h1>
        <br />
        <TextField
          id="email"
          label="Correo electrónico *"
          variant="outlined"
          type={"email"}
          style={{ backgroundColor: "white" }}
          value={state.email}
          onChange={handleChange}
        />
        <br />
        <TextField
          id="password"
          label="Contraseña *"
          variant="outlined"
          type={"password"}
          style={{ backgroundColor: "white" }}
          value={state.password}
          onChange={handleChange}
        />
        <br />
        <br />

        <Button
          variant="contained"
          style={{ backgroundColor: "#3E2B2E" }}
          onClick={handleLogin}
        >
          Iniciar sesión
        </Button>
        <p>
          ¿No tienes una cuenta? <Link to="/register">Regístrate</Link>.
        </p>
        <Alert severity="warning">Usuario o contraseña incorrectos</Alert>
      </Grid>
    </Grid>
  );
}

export default Login;
