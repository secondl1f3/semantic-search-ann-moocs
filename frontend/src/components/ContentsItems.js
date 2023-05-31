import { List, LoadingOverlay } from "@mantine/core";
import React from "react";
import Items from "./Items";

export default function ContentItems({ data = [], loading }) {
  return (
    <List icon={<></>}>
      <LoadingOverlay visible={loading} overlayBlur={2} />
      <Items data={data} />
    </List>
  );
}
