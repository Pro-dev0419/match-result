import type { NextApiRequest, NextApiResponse } from "next";

import { queryAsPromise, disconnect, connectToMySql } from "../../../utils/db";

type Data = {
  name: string;
};

// const { NHL_SOG_TABLE } = process.env;
const MMA_ML_TABLE  = 'mma_ml';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const connection = await connectToMySql();
  try {
    const data: any = await queryAsPromise(
      connection,
      "SELECT * FROM " + MMA_ML_TABLE
    );

    res.status(200).json(data);
  } catch (e) {
    res.status(500);
  } finally {
    disconnect(connection);
  }
}
