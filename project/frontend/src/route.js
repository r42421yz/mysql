
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LoginRegister from './pages/LoginRegister';
import Dashboard from './pages/Dashboard';
import Predict from "./Predict";

function AppRoutes() {
  return (
    <React.StrictMode>
      <Predict />
    </React.StrictMode>
    // <Routes>
    //   <Route path="/" element={<LoginRegister />} />
    //   <Route path="/dashboard" element={<Dashboard />} />
    // </Routes>
  );
}

export default AppRoutes;
