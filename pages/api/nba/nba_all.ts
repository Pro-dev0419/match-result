import type { NextApiRequest, NextApiResponse } from "next";

import { queryAsPromise, disconnect, connectToMySql } from "../../../utils/db";

type Data = {
  name: string;
};

const NBA_ASSIST_TABLE  = 'assists';
const NBA_ASTRBS_TABLE  = 'astrbs';
const NBA_PA_TABLE  = 'pa';
const NBA_PAR_TABLE  = 'par';
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
      "SELECT * FROM assists UNION SELECT * FROM astrbs UNION SELECT * from pa UNION SELECT * from par UNION SELECT * FROM points UNION SELECT * from pr UNION SELECT * from rebounds ORDER BY ROI_DK desc"
    );

    res.status(200).json({ data });
  } catch (e) {
    res.status(500);
  } finally {
    disconnect(connection);
  }
}
