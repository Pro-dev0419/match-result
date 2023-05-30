// @ts-ignore
import type { NextPage } from "next";
import { useEffect, useState } from "react";
import Image from "next/image";
import styles from "../../styles/Home.module.css";

import { DataGrid, GridColDef } from "@mui/x-data-grid";

const TABLE_COLUMNS: GridColDef[] = [
  { field: "DISPLAY", headerName: "Prop", width: 300 },
  { field: "PASS YARDS", headerName: "Passing Yards" },
  { field: "LINE_DK", headerName: "LINE_DK" },
  { field: "AMERICAN_DK", headerName: "DK" },
  { field: "DK_DIFF", headerName: "DK_DIFF", valueFormatter: ({ value }) => `${value} %` },
  { field: "LINE_FD", headerName: "LINE_FD" },
  { field: "AMERICAN_FD", headerName: "FD" },
  { field: "FD_DIFF", headerName: "FD_DIFF", valueFormatter: ({ value }) => `${value} %` },
  { field: "LINE_MGM", headerName: "LINE_MGM" },
  { field: "AMERICAN_MGM", headerName: "MGM" },
  { field: "MGM_DIFF", headerName: "MGM_DIFF", valueFormatter: ({ value }) => `${value} %` },
  { field: "LINE_CZR", headerName: "LINE_CZR" },
  { field: "AMERICAN_CZR", headerName: "CZR" },
  { field: "CZR_DIFF", headerName: "CZR_DIFF", valueFormatter: ({ value }) => `${value} %` },
];

const Home: NextPage = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const res = await fetch("/api/nfl/passyards").then((o) => o.json());
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
        <h1 className={styles.title}>Passing Yards</h1>
        {loading && "Loading"}
        {!loading && data && (
          <div className={styles.tableContainer}>
            <DataGrid
              rows={data}
              getRowId={(row) => row.index}
              columns={TABLE_COLUMNS}
            />
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
