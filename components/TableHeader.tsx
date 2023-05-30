import { Fragment } from "react";
import { TableColumn } from "../constants/table";

const TableHeader = ({ columns }: { columns: TableColumn[] }) => {
  return (
    <Fragment>
      {columns.map(({ key, columnName }) => (
        <th key={key}>{columnName || key}</th>
      ))}
    </Fragment>
  );
};

export default TableHeader;
