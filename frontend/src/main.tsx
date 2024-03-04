import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ReactDOM from "react-dom/client";
import "./index.css";
import HomePage from "./pages/HomePage";
import ProductPage from "./pages/ProductPage";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Router basename="/">
      <Routes>
        <Route path="/" element={<HomePage />} />

        <Route path="/product/:productID" element={<ProductPage />} />

        <Route
          path="*"
          element={
            <div className=" flex content-center justify-center">
              404 Not found{" "}
            </div>
          }
        />
      </Routes>
    </Router>
    {/* <HomePage /> */}
  </React.StrictMode>
);
