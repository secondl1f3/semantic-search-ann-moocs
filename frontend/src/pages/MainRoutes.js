import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Main from "./Main";
import Results from "./Results";
import StatisticsPage from '../components/Statistics';

const MainRoutes = () => {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Main />} />
          <Route exact path="/statistics" element={<StatisticsPage />} />
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
