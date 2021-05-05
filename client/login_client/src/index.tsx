import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { App } from './App';

import { Provider } from 'react-redux'
import { getStore } from './core/store'

ReactDOM.render(
  <React.StrictMode>
    <Provider
      store={getStore()}
    >
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);
