import './App.css';
import React, { useEffect, useState } from 'react';
import { Tab } from './components/Tab'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home'
import { AddSite } from './pages/AddSite';
import axios from 'axios'

export default function App() {
  const [selectedTab, setSelectedTab] = useState("Apps");

  function handleTabClick(tabTitle) {
    setSelectedTab(tabTitle);
  }

  useEffect(() => {
    setSelectedTab("Apps");
  }, []);

  useEffect(() => {
    console.log(selectedTab);
  }, [handleTabClick]);

  return (
    <Router>
      <div className="App">
        <h1>Cantonica</h1>
        <div className="tab-container">
          <Tab
            title="Apps"
            selected={selectedTab === "Apps"}
            onClick={() => handleTabClick("Apps")}
          />
          <Tab
            title="Saved Apps"
            selected={selectedTab === "Saved Apps"}
            onClick={() => handleTabClick("Saved Apps")}
          />
          <Tab
            title="Index New Apps"
            selected={selectedTab === "Index New Apps"}
            onClick={() => handleTabClick("Index New Apps")}
          />
        </div>
        <div className="content">
          {selectedTab === "Apps" && (
            <div>
              <Home />
            </div>
          )}
          {selectedTab === "Saved Apps" && (
            <div>
              <h1>Hey</h1>
            </div>
          )}
          {selectedTab === "Index New Apps" && (
            <div>
              <AddSite />
            </div>
          )}
        </div>
      </div>

    
      <Routes>
        <Route index path="/"  />
        <Route path="/AddSite" element={<AddSite />} />
      </Routes>
    </Router>
  );
}
