// import logo from './logo.svg';
import React from 'react';
import './App.css';
import Layout from './components/Main/Layout';
import {Routes, Route} from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
// import Hello from './components/Hello';

// import Navbar from './components/Navbar';

function App() {
  return (
    <>
   
      
      <Routes>
        <Navbar/>
        <Route path="/" element={<Layout />} />
      </Routes>
    </>
    
    
    );
}

export default App;
