import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { legacy_createStore as createStore, applyMiddleware, compose} from "redux";
import thunk from 'redux-thunk';

import reducers from './reducers';

import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(<App />)

// root means everything in App https://stackoverflow.com/a/65531078/6501621

