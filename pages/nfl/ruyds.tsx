// @ts-ignore
import type { NextPage } from "next";
import { useEffect, useState } from "react";
import Image from "next/image";
import clsx from 'clsx';
import Box from '@mui/material/Box';
import styles from "../../styles/Home.module.css";
import LaunchIcon from "@mui/icons-material/Launch";
import IconButton from '@mui/material/IconButton';

import { DataGrid, GridColDef, GridCellParams } from "@mui/x-data-grid";

const TABLE_COLUMNS: GridColDef[] = [
  { field: "DISPLAY", headerName: "Prop", width: 300 },
  { field: "TEAM", headerName: "Team" },
  { field: "CARRIES", headerName: "Attempts" },
  { field: "RUSH YARDS", headerName: "Yards" },
  { field: "LINE_DK", headerName: "LINE_DK" },
  { field: "AMERICAN_DK", headerName: "DK" },
  { field: "ROI_DK", headerName: "ROI_DK", type: 'number',
    renderCell: (params) =>
    <p>
      <a href="https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-props&subcategory=assists">{params.row.ROI_DK}%</a>
      <IconButton href="https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-props&subcategory=assists"> <LaunchIcon />
      </IconButton>
    </p>,
    cellClassName: (params: GridCellParams<number>) => {
      if (params.value == null) {
        return '0';
      }

      return clsx('super-app', {
        neutral: params.value < 20,
        negative: params.value < 0,
        positive: params.value > 20,
      });
    },
  },
  { field: "LINE_FD", headerName: "LINE_FD" },
  { field: "AMERICAN_FD", headerName: "FD" },
  { field: "ROI_FD", headerName: "ROI_FD", type: 'number',
    renderCell: (params) =>
      <p>
        <a href={params.row.URL_FD}>{params.row.ROI_FD}%</a>
        <IconButton href={params.row.URL_FD}> <LaunchIcon />
        </IconButton>
      </p>,
    cellClassName: (params: GridCellParams<number>) => {
      if (params.value == null) {
        return '0';
      }

      return clsx('super-app', {
        neutral: params.value < 20,
        negative: params.value < 0,
        positive: params.value > 20,
      });
    },   
    },
  { field: "LINE_MGM", headerName: "LINE_MGM" },
  { field: "AMERICAN_MGM", headerName: "MGM" },
  { field: "ROI_MGM", headerName: "ROI_MGM", type: 'number',
    renderCell: (params) =>
    <p>
      <a href={params.row.URL_MGM}>{params.row.ROI_MGM}%</a>
      <IconButton href={params.row.URL_MGM}> <LaunchIcon />
      </IconButton>
    </p>,
    cellClassName: (params: GridCellParams<number>) => {
      if (params.value == null) {
        return '0';
      }

      return clsx('super-app', {
        neutral: params.value < 20,
        negative: params.value < 0,
        positive: params.value > 20,
      });
    },   
    },
  { field: "LINE_CZR", headerName: "LINE_CZR" },
  { field: "AMERICAN_CZR", headerName: "CZR" },
  { field: "ROI_CZR", headerName: "ROI_CZR", type: 'number',
    valueFormatter: ({ value }) => `${value} %`, 
    cellClassName: (params: GridCellParams<number>) => {
      if (params.value == null) {
        return '0';
      }

      return clsx('super-app', {
        neutral: params.value < 20,
        negative: params.value < 0,
        positive: params.value > 20,
      });
    },   
  
  },

];

const Home: NextPage = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const res = await fetch("/api/nfl/ruyds").then((o) => o.json());
        setData(res.data);
      } catch (e) {
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>Rushing Yards</h1>
        {loading && "Loading"}
        {!loading && data && (
          <div className={styles.tableContainer}>
          <Box
            sx={{
              height: '100%',
              width: '100%',
              '& .super-app.negative': {
                backgroundColor: '#FF0000',
              },
              '& .super-app.positive': {
                backgroundColor: '#228C22',
              },
            }}
          >
            <DataGrid
              rows={data}
              getRowId={(row) => row.index}
              columns={TABLE_COLUMNS}
            />
          </Box>

          </div>
        )}
      </main>

      <footer className={styles.footer}>
        <a href="https://prophub.ca" target="_blank" rel="noopener noreferrer">
          Powered by{" "}
          <span className={styles.logo}>
            <Image src="/prophub.jpg" alt="Rfr3sh" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  );
};



export default Home;
