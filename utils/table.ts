export const getHighestValue = (
  row: { [k: string]: any },
  keysToCompare: string[]
) => {
  const max = Math.max(
    ...keysToCompare.map((o) => row[o]).filter((o) => o !== null)
  );

  const highestKeys = keysToCompare.filter((o) => row[o] && row[o] === max);

  console.log(row, max, highestKeys);
  return highestKeys;
};
