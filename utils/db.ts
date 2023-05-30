import mysql from "mysql";

const host = process.env.DB_HOST;
const user = process.env.DB_USERNAME;
const password = process.env.DB_PASSWORD;
const database = process.env.DB_DB;

export const connectToMySql = () => {
  const connection = mysql.createConnection({
    host,
    user,
    password,
    database,
  });

  connection.connect();
  return connection;
};

export const disconnect = (connection) => connection.end();

export const queryAsPromise = (connection, query, values?) =>
  new Promise((resolve, reject) =>
    connection.query(query, values, function (error, results, fields) {
      if (error) return reject(error);
      return resolve(results);
    })
  );
