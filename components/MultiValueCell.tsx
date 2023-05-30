import { Fragment } from "react";
import { HIGHLIGHT_COLOR } from "../constants/table";

const Row = ({ value1, value2, value3, highestValues, highlightKey }) => (
  <p>
    {value1} {value2} (
    <span
      style={{
        backgroundColor: highestValues.includes(highlightKey)
          ? HIGHLIGHT_COLOR
          : "",
      }}
    >
      {value3}
    </span>
    )
  </p>
);

const MultiValueCell = ({
  highestValues,
  row1,
  row1HighlightKey,
  row2,
  row2HighlightKey,
}: {
  highestValues: string[];
  row1: any[];
  row1HighlightKey: string;
  row2: any[];
  row2HighlightKey: string;
}) => {
  return (
    <Fragment>
      <Row
        value1={row1[0]}
        value2={row1[1]}
        value3={row1[2]}
        highlightKey={row1HighlightKey}
        highestValues={highestValues}
      />
      <Row
        value1={row2[0]}
        value2={row2[1]}
        value3={row2[2]}
        highlightKey={row2HighlightKey}
        highestValues={highestValues}
      />
    </Fragment>
  );
};

export default MultiValueCell;
