import { AppBar, Grid, Hidden, IconButton, Toolbar } from "@mui/material";
import EventsList from "../screens/EventsList";
import Login from "../screens/Login";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import { useMemo, useState } from "react";

const HomeSwitch = () => {
  /*alert(localStorage.getItem("token"));
  const userSignedIn = useMemo(
    () => !!localStorage.getItem("token"),
    [localStorage]
  );*/

  const [username, setUsername] = useState();
  const [token, setToken] = useState();

  if (!token) return <Login setUsername={setUsername} setToken={setToken} />;

  const handleLogout = () => {
    setUsername();
    setToken();
  };

  return (
    <Grid>
      <AppBar
        position="sticky"
        elevation={5}
        style={{
          display: "flex",
          flexWrap: "wrap",
          width: "100%",
          height: "60px",
          backgroundColor: "white !important",
          "& .MuiAppBar-colorPrimary": {
            backgroundColor: "white",
          },
        }}
      >
        <Toolbar>
          <Grid
            container
            direction="row"
            justify="space-between"
            alignItems="center"
            xs={12}
          >
            <Grid
              container
              direction="row"
              justify="flex-start"
              alignItems="center"
              style={{
                paddingTop: 5,
                height: "100%",
                "@media( min-width : 600px )": {
                  paddingLeft: "40px",
                  paddingRight: "40px",
                  paddingBottom: "10px",
                },
              }}
              xs
            >
              <img
                style={{
                  height: "50px",
                }}
                alt=""
              />
              <Hidden smDown>
                <p
                  style={{
                    color: "#67B8C2",
                    fontWeight: "700",
                    padding: 0,
                    marginTop: 0,
                    marginRight: 0,
                    marginBottom: 0,
                    marginLeft: "3px",
                    "@media( min-width : 600px )": {
                      marginLeft: "10px",
                    },
                    fontSize: "1.4em",
                    cursor: "pointer",
                  }}
                >
                  ABC Soluciones
                </p>
              </Hidden>
            </Grid>
            <Grid
              container
              direction="row"
              justify="flex-end"
              alignItems="center"
              style={{
                paddingTop: 5,
                height: "100%",
                "@media( min-width : 600px )": {
                  paddingLeft: "40px",
                  paddingRight: "40px",
                  paddingBottom: "10px",
                },
              }}
              xs
            >
              <Hidden smDown>
                <p
                  style={{
                    color: "#67B8C2",
                    padding: 0,
                    marginTop: 0,
                    marginRight: 0,
                    marginBottom: 0,
                    marginLeft: 20,
                  }}
                >
                  {username}
                </p>
              </Hidden>
              <IconButton
                style={{
                  height: "50px",
                  marginRight: 30,
                  "@media( max-width : 600px )": {
                    marginRight: "10px",
                    marginLeft: "10px",
                  },
                  color: "#67B8C2",
                }}
              >
                <ExitToAppIcon onClick={handleLogout} />
              </IconButton>
            </Grid>
          </Grid>
        </Toolbar>
      </AppBar>
      <EventsList token={token} />
    </Grid>
  );
};

export default HomeSwitch;
