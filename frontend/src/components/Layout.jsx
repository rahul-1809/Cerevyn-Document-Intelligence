import React from 'react';
import './Layout.css';

function Layout({ sidebar, main }) {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1 className="app-title">Cerevyn</h1>
          <p className="app-subtitle">Document Intelligence</p>
        </div>
        <div className="sidebar-content">
          {sidebar}
        </div>
      </aside>
      <main className="main-content">
        {main}
      </main>
    </div>
  );
}

export default Layout;
