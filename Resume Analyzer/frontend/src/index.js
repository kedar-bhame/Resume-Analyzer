import React from 'react';
import {createRoot} from 'react-dom/client';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Layout from './Layout';
import App from './App';
import Review from './components/Review';
import Templates from './components/Templates';
import Login from './components/Login';
import Signup from './components/Signup';
import './styles.css';

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<App/>} />
          <Route path="/review" element={<Review/>} />
          <Route path="/templates" element={<Templates/>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/signup" element={<Signup/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
