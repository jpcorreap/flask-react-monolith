import { Grid, TextField, Button, Alert } from "@mui/material";
import React, { useState } from "react";
import logo from "../assets/full_size_logo.png";
import { Link } from "react-router-dom";

function Register() {
  const [state, setState] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    setState({ [e.currentTarget.id]: e.currentTarget.value });
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
        <h1 style={{ color: "#978C87" }}>Registro de usuarios</h1>
        <br />
        <TextField
          id="outlined-basic"
          label="Correo electrónico *"
          variant="outlined"
          type={"email"}
          style={{ backgroundColor: "white" }}
          onChange={(e) => console.info(e.target.value)}
        />
        <br />
        <TextField
          id="outlined-basic"
          label="Contraseña *"
          variant="outlined"
          type={"password"}
          style={{ backgroundColor: "white" }}
        />
        <br />
        <br />

        <Button variant="contained" style={{ backgroundColor: "#3E2B2E" }}>
          Registrarse
        </Button>
        <p>
          ¿Ya tienes una cuenta? <Link to="/">Inicia sesión</Link>.
        </p>
      </Grid>
    </Grid>
  );
}

export default Register;
