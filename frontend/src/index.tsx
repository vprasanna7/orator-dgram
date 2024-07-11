import React from 'react';
import ReactDOM from 'react-dom/client';
import { DailyProvider } from '@daily-co/daily-react';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <DailyProvider>
      <App />
    </DailyProvider>
  </React.StrictMode>
);