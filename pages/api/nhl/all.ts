import type { NextApiRequest, NextApiResponse } from "next";

import { queryAsPromise, disconnect, connectToMySql } from "../../../utils/db";

type Data = {
  name: string;
};

const NHL_ASSIST_TABLE  = 'nhl_assists';
const NHL_SOG_TABLE  = 'sog';
const NBA_PA_TABLE  = 'atg';
const NBA_PAR_TABLE  = 'nhl_points';
const NBA_POINTS_TABLE  = 'points';
const NBA_PR_TABLE  = 'pr';
const NBA_REBOUNDS_TABLE  = 'rebounds';
const NBA_THREES_TABLE  = 'threes';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const connection = await connectToMySql();
  try {
    const data = await queryAsPromise(
      connection,
      "SELECT * FROM nhl_assists UNION SELECT * FROM nhl_points UNION SELECT * from sog ORDER BY ROI_DK desc"
    );

    res.status(200).json({ data });
  } catch (e) {
    res.status(500);
  } finally {
    disconnect(connection);
  }
}
