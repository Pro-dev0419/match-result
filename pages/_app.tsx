import React, { useState } from "react";
import Link from "next/link";
import "../styles/globals.css";
import styles from "../styles/Home.module.css";
import type { AppProps } from "next/app";
import Head from "next/head";

import { CacheProvider } from "@emotion/react";
import {
  ThemeProvider,
  CssBaseline,
  Button,
  Menu,
  MenuItem,
} from "@mui/material";

import createEmotionCache from "../utility/createEmotionCache";
import lightTheme from "../styles/theme/lightTheme";

const clientSideEmotionCache = createEmotionCache();

type MyAppProps = AppProps & {
  emotionCache: any;
};

const MENU_ITEMS = {
  mlb: [
    { route: "/mlb/so", display: "K Props" },
  ],
  nhl: [
    { route: "/nhl/all", display: "All NHL Props" },
    { route: "/nhl/sog", display: "Shots on Goal" },
    { route: "/nhl/assists", display: "Assists" },
    { route: "/nhl/points", display: "Points" },
    { route: "/nhl/atg", display: "Anytime Goal Scorer" },
    { route: "/nhl/saves", display: "Saves" },
  ],
  // nfl: [
  //   { route: "/nfl/passatt", display: "Pass Attempts" },
  //   { route: "/nfl/passcomp", display: "Pass Completions" },
  //   { route: "/nfl/passyards", display: "Pass Yards" },
  //   { route: "/nfl/recyds", display: "Receiving Yards" },
  //   { route: "/nfl/totrec", display: "Total Receptions" },
  //   { route: "/nfl/ruyds", display: "Rushing Yards" },
  //   { route: "/nfl/rushatt", display: "Rushing Attempts" },
  //   { route: "/nfl/atd", display: "Anytime Touchdown" },
  // ],
  nba: [
    { route: "/nba/all", display: "All Props" },
    { route: "/nba/market", display: "Market Bets" },
    { route: "/nba/pointscombos", display: "All Point Combos" },
    { route: "/nba/points", display: "Points" },
    { route: "/nba/assists", display: "Assists" },
    { route: "/nba/rebounds", display: "Rebounds" },
    { route: "/nba/par", display: "Points Assists Rebounds" },
    { route: "/nba/pr", display: "Points Rebounds" },
    { route: "/nba/pa", display: "Points Assists" },
    { route: "/nba/astrbs", display: "Assists Rebounds" },
    { route: "/nba/threes", display: "Three Pointers Made" },
  ]
};

function MyApp(props: MyAppProps) {
  const { Component, emotionCache = clientSideEmotionCache, pageProps } = props;
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [sport, setSport] = useState("");
  const open = Boolean(anchorEl);
  const handleClick =
    (sport: string) => (event: React.MouseEvent<HTMLButtonElement>) => {
      setAnchorEl(event.currentTarget);
      setSport(sport);
    };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <Head>
        <title>Prop Betting</title>
        <meta
          name="description"
          content="Automatic Update Prop Lines and Suggested Bets"
        />
        <link rel="icon" href="/prophub.jpg" />
      </Head>
      <CacheProvider value={emotionCache}>
        <ThemeProvider theme={lightTheme}>
          <CssBaseline />
          <div className={styles.navbar}>
            {["mlb", "nhl", "nba"].map((menuName) => (
              <Button
                key={menuName}
                id="basic-button"
                aria-controls={open ? "basic-menu" : undefined}
                aria-haspopup="true"
                aria-expanded={open ? "true" : undefined}
                onClick={handleClick(menuName)}
              >
                {menuName}
              </Button>
            ))}
            {sport && (
              <Menu
                id="basic-menu"
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                MenuListProps={{
                  "aria-labelledby": "basic-button",
                }}
              >
                {MENU_ITEMS[sport].map(({ route, display }) => (
                  <MenuItem key={route} onClick={handleClose}>
                    <Link key={route} href={route}>
                      <a>{display}</a>
                    </Link>
                  </MenuItem>
                ))}
              </Menu>
            )}
          </div>
          <Component {...pageProps} />
        </ThemeProvider>
      </CacheProvider>
    </div>
  );
}

export default MyApp;
