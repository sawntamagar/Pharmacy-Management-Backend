import React from "react";
import "../../App.css";
import { Routes, Route } from "react-router-dom";
import Navbar from "../Navbar/Navbar";


const Layout = () => {
    return (
        <Routes>
            <Route path="/" element={<Navbar />} />
          </Routes>
    )
}

export default Layout;