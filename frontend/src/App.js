import { MantineProvider } from "@mantine/core";
import React from "react";
import MainRoutes from "./pages/MainRoutes";

export default function App() {
  return (
    <MantineProvider withGlobalStyles withNormalizeCSS>
      <MainRoutes />
    </MantineProvider>
  );
}
