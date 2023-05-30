// @ts-ignore
import type { NextPage } from "next";
import { useEffect, useState } from "react";
import Image from "next/image";
import Box from '@mui/material/Box';

import styles from "../../styles/Home.module.css";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { DataGrid, GridColDef, GridCellParams } from "@mui/x-data-grid";

const TABLE_COLUMNS: GridColDef[] = [
    { field: "event", headerName: "event", width: 200 },
    { field: "fighter", headerName: "Fighter", width: 200 },
    { field: "betonlineag", headerName: "betonlineag", width: 50 },
    { field: "pinnacle", headerName: "pinnacle", width: 50 },
    { field: "williamhill_us", headerName: "williamhill", width: 50 },
    { field: "sugarhouse", headerName: "sugarhouse", width: 50 },
    { field: "twinspires", headerName: "twinspires", width: 50 },
    { field: "betrivers", headerName: "betrivers", width: 50 },
    { field: "sport888", headerName: "sport888", width: 50 },
    { field: "lowvig", headerName: "lowvig", width: 50 },
    { field: "barstool", headerName: "barstool", width: 50 },
    { field: "betus", headerName: "betus", width: 50 },
    { field: "unibet_us", headerName: "unibet", width: 50 },
    { field: "fanduel", headerName: "fanduel", width: 50 },
    { field: "draftkings", headerName: "draftkings", width: 50 },
    { field: "betclic", headerName: "betclic", width: 50 },
    { field: "superbook", headerName: "superbook", width: 50 },
    { field: "betfair", headerName: "betfair", width: 50 },
    { field: "betmgm", headerName: "betmgm", width: 50 },
    { field: "marathonbet", headerName: "marathonbet", width: 50 },
    { field: "bovada", headerName: "bovada", width: 50 },


];

const Home: NextPage = () => {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                let res = await fetch("/api/mma/mma_ml").then((o) => o.json());
                let addMaxData = res.map((item) => {
                    const { index, ...tempArr } = item;
                    let tempItem: any = Object.values(tempArr).filter(num => typeof num === 'number');
                    let maxValue = Math.max(...tempItem);
                    return {
                        ...item,
                        max: maxValue
                    }
                });
                const tableData = addMaxData.reduce((groups: any, item: any) => {
                    const group = (groups[item.event] || []);
                    group.push(item);
                    groups[item.event] = group;
                    return groups;
                }, {});
                setData(tableData);
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
                <h1 className={styles.title}>Fight Odds</h1>
                {loading && "Loading"}
                {!loading && data && (
                    <div className={styles.tableContainer}>
                        {Object.keys(data).map((eventId, boxIndex) => (
                            <Box
                                key={boxIndex}
                                sx={{
                                    width: '100%',
                                    '& .super-app.negative': {
                                        backgroundColor: '#FF0000',
                                    },
                                    '& .super-app.positive': {
                                        backgroundColor: '#228C22',
                                    },
                                }}
                            >
                                <h3>{eventId}</h3>
                                <TableContainer style={{ height: '100%', borderLeft: '1px solid grey', borderRight: '1px solid grey' }}>
                                    <Table stickyHeader aria-label="sticky collapsible table">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Fighter</TableCell>
                                                {
                                                    Object.keys(data[eventId][0]).map((item, index) => (
                                                        item !== 'index' && item !== 'event' && item !== 'fighter' && item !== 'max' && <TableCell key={index}>{item}</TableCell>
                                                    ))
                                                }
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {
                                                data[eventId].map((item: any, index: number) => (
                                                    <TableRow key={index}>
                                                        <TableCell style={{ whiteSpace: 'nowrap' }}>{item['fighter']}</TableCell>
                                                        {Object.keys(item).map((cellKey, j) => (
                                                            cellKey !== 'index' && cellKey !== 'event' && cellKey !== 'fighter' && cellKey !== 'max' &&
                                                            <TableCell key={j} style={{ color: `${item['max'] === item[cellKey] ? 'white' : ''}`, backgroundColor: `${item['max'] === item[cellKey] ? 'green' : ''}` }}>
                                                                {item[cellKey]}
                                                            </TableCell>
                                                        ))}
                                                    </TableRow>
                                                ))
                                            }
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Box>
                        ))}



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
