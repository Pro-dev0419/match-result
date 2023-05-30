// @ts-ignore
import type { NextPage } from "next";
import { useEffect, useState } from "react";
import Image from "next/image";
import styles from "../styles/Home.module.css";
import { getHighestValue } from "../utils/table";
import { TableColumn } from "../constants/table";
import TableHeader from "../components/TableHeader";
import MultiValueCell from "../components/MultiValueCell";

const TABLE_COLUMNS: TableColumn[] = [
  { key: "NAME", columnName: "Pitcher" },
  { key: "K", columnName: "Razz" },
  { key: "K_THEBAT", columnName: "Bat" },
  { key: "PPC" },
  { key: "OPP" },
  { key: "HAND" },
  { key: "LINE_DK", columnName: "DK" },
  { key: "LINE_FD", columnName: "FD" },
  { key: "LINE_MGM", columnName: "MGM" },
  { key: "LINE_CZ", columnName: "CZ" },
];

const VALUES_TO_COMPARE_FOR_HIGHEST = [
  "KO_DK",
  "KU_DK",
  "KO_FD",
  "KU_FD",
  "KO_MGM",
  "KU_MGM",
  "KO_CZ",
  "KU_CZ",
];

const getCellValueByColumn = (column, row, highestValues) => {
  if (column === "LINE_DK") {
    const { LINE_DK, O_DK, KO_DK, U_DK, KU_DK } = row;
    return (
      <div>
        {LINE_DK ? (
          <MultiValueCell
            row1={[LINE_DK, O_DK, KO_DK]}
            row1HighlightKey="KO_DK"
            row2={[LINE_DK, U_DK, KU_DK]}
            row2HighlightKey="KU_DK"
            highestValues={highestValues}
          />
        ) : (
          "-"
        )}
      </div>
    );
  }

  if (column === "LINE_FD") {
    const { LINE_FD, O_FD, KO_FD, U_FD, KU_FD } = row;
    return (
      <div>
        {LINE_FD ? (
          <MultiValueCell
            row1={[LINE_FD, O_FD, KO_FD]}
            row1HighlightKey="KO_FD"
            row2={[LINE_FD, U_FD, KU_FD]}
            row2HighlightKey="KU_FD"
            highestValues={highestValues}
          />
        ) : (
          "-"
        )}
      </div>
    );
  }

  if (column === "LINE_MGM") {
    const { LINE_MGM, O_MGM, KO_MGM, U_MGM, KU_MGM } = row;
    return (
      <div>
        {LINE_MGM ? (
          <MultiValueCell
            row1={[LINE_MGM, O_MGM, KO_MGM]}
            row1HighlightKey="KO_MGM"
            row2={[LINE_MGM, U_MGM, KU_MGM]}
            row2HighlightKey="KU_MGM"
            highestValues={highestValues}
          />
        ) : (
          "-"
        )}
      </div>
    );
  }
  if (column === "LINE_CZ") {
    const { LINE_CZ, O_CZ, KO_CZ, U_CZ, KU_CZ } = row;
    return (
      <div>
        {LINE_CZ ? (
          <MultiValueCell
            row1={[LINE_CZ, O_CZ, KO_CZ]}
            row1HighlightKey="KO_CZ"
            row2={[LINE_CZ, U_CZ, KU_CZ]}
            row2HighlightKey="KU_CZ"
            highestValues={highestValues}
          />
        ) : (
          "-"
        )}
      </div>
    );
  }

  return row[column];
};

const Home: NextPage = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const res = await fetch("/api/mlb").then((o) => o.json());
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
        <h1 className={styles.title}>K Props</h1>
        {loading && "Loading"}
        {!loading && data && (
          <div className={styles.tableContainer}>
            <table>
              <thead>
                <tr>
                  <TableHeader columns={TABLE_COLUMNS} />
                </tr>
              </thead>
              <tbody>
                {data.map((o, i) => {
                  const highestValue = getHighestValue(
                    o,
                    VALUES_TO_COMPARE_FOR_HIGHEST
                  );
                  return (
                    <tr key={i}>
                      {TABLE_COLUMNS.map(({ key }) => {
                        const value = getCellValueByColumn(
                          key,
                          o,
                          highestValue
                        );
                        return <td key={key}>{value}</td>;
                      })}
                    </tr>
                  );
                })}
              </tbody>
            </table>
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
