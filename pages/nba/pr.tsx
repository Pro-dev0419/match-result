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
  { field: "PROP", headerName: "Prop", width: 250 },
  { field: "PR", headerName: "Proj", width: 75 },
  { field: "TEAM", headerName: "Team", width: 75 },
  { field: "MINUTES", headerName: "Min", width: 75 },
  { field: "LINE_DK", headerName: "DK", width: 100,
    renderCell: (params) =>
    <p>
        {params.row.LINE_DK} ({params.row.AMERICAN_DK})
    </p>
    },
  { field: "ROI_DK", headerName: "ROI_DK", type: 'number', width: 100,
    renderCell: (params) =>
    <p>
      <a href="https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-props&subcategory=pts-+-reb">{params.row.ROI_DK}%</a>
      <IconButton href="https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-props&subcategory=pts-+-reb"> <LaunchIcon />
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
  { field: "LINE_FD", headerName: "FD", width: 100,
    renderCell: (params) =>
    <p>
        {params.row.LINE_FD} ({params.row.AMERICAN_FD})
    </p>
    },
  { field: "ROI_FD", headerName: "ROI_FD", type: 'number', width: 100,
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
   { field: "LINE_MGM", headerName: "MGM", width: 100,
    renderCell: (params) =>
    <p>
        {params.row.LINE_MGM} ({params.row.AMERICAN_MGM})
    </p>
    },
  { field: "ROI_MGM", headerName: "ROI_MGM", type: 'number', width: 100,
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
    { field: "LINE_CZR", headerName: "CZR", width: 100,
    renderCell: (params) =>
    <p>
        {params.row.LINE_CZR} ({params.row.AMERICAN_CZR})
    </p>
    },
  { field: "ROI_CZR", headerName: "ROI_CZR", type: 'number', width: 100,
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

  { field: "LINE_RIV", headerName: "RIV", width: 100,
  renderCell: (params) =>
  <p>
      {params.row.LINE_RIV} ({params.row.AMERICAN_RIV})
  </p>
  },
{ field: "ROI_RIV", headerName: "ROI_RIV", type: 'number', width: 100,
  renderCell: (params) =>
  <p>
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
  const [data2, setData2] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const res = await fetch("/api/nba/pr").then((o) => o.json());
        const last_modified = await fetch("/api/nba/last_mod").then((o) => o.json());
        setData(res.data);
        setData2(last_modified.data[0].date);
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
        <h1 className={styles.title}>Points + Rebounds</h1>
        <div>Projections Update: {data2}</div>
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