import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  // strict mode double-induces effects - so 2 of everything in the browser console
  // <React.StrictMode>
  //   <App />
  // </React.StrictMode>,
  <App />
)
