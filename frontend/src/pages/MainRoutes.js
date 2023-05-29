import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Main from "./Main";
import Results from "./Results";

const MainRoutes = () => {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Main />} />
          <Route
            exact
            path="/results/:searchValue/:lang"
            element={<Results />}
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
};

export default MainRoutes;
