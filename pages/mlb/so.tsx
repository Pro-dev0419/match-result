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
  { field: "PROP", headerName: "Prop", width: 200 },
  { field: "TEAM", headerName: "Team" , width: 50 },
  { field: "PPC", headerName: "PPC" , width: 50 },
  { field: "K_X", headerName: "K" , width: 50 },
  { field: "ROI_DK", headerName: "DK", type: 'number', width: 100,
    renderCell: (params) =>
    <p>
      {params.row.LINE_DK} ({params.row.AMERICAN_DK}) <br></br>
      <a href="https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props">{params.row.ROI_DK}%</a>
      <IconButton href="https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props"> <LaunchIcon />
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
  { field: "ROI_FD", headerName: "FD", type: 'number', width: 100,
    renderCell: (params) =>
      <p>
        {params.row.LINE_FD} ({params.row.AMERICAN_FD}) <br></br>
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
  { field: "ROI_MGM", headerName: "MGM", type: 'number', width: 100,
    renderCell: (params) =>
    <p>
      {params.row.LINE_MGM} ({params.row.AMERICAN_MGM}) <br></br>
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
  { field: "ROI_CZR", headerName: "CZR", type: 'number', width: 100,
    renderCell: (params) =>
    <p>
      {params.row.LINE_CZR} ({params.row.AMERICAN_CZR}) <br></br>
      <a href={params.row.URL_CZR}>{params.row.ROI_CZR}%</a>
      <IconButton href={params.row.URL_CZR}> <LaunchIcon />
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
  { field: "ROI_ANO", headerName: "ANO", type: 'number', width: 100,
    renderCell: (params) =>
      <p>
        {params.row.LINE_ANO} ({params.row.AMERICAN_ANO}) <br></br>
        <a href={params.row.URL_ANO}>{params.row.ROI_ANO}%</a>
        <IconButton href={params.row.URL_ANO}> <LaunchIcon />
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
  { field: "ROI_RIV", headerName: "RIV", type: 'number', width: 100,
    renderCell: (params) =>
    <p>
      {params.row.LINE_RIV} ({params.row.AMERICAN_RIV}) <br></br>
      <a href={params.row.URL_RIV}>{params.row.ROI_RIV}%</a>
      <IconButton href={params.row.URL_RIV}> <LaunchIcon />
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

];

const Home: NextPage = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const res = await fetch("/api/mlb/so").then((o) => o.json());
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
        <h1 className={styles.title}>Strikeouts</h1>
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
