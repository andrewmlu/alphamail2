import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { legacy_createStore as createStore, applyMiddleware, compose} from "redux";
import thunk from 'redux-thunk';

import reducers from './reducers';

import { BrowserRouter, Routes, Route, useParams } from 'react-router-dom';

import App from './App';
import './index.css';
import Carousel from "./components/carousel";
import Recents from "./components/recents";
import NotFound from "./components/notfound";
import Thread from "./components/thread";
import Composer from "./components/composer";

const store = createStore(reducers, compose(applyMiddleware(thunk)));

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
    <Provider store={store}>
        <BrowserRouter>
            <Routes>
                <Route path={'/'} element={<App />}>
                    <Route index element={<Carousel />}/>
                    <Route path={'threads'} element={<Recents />}/>
                    <Route path={'thread/:threadId'} element={<Thread />}/>
                    <Route path={'compose'} element={<Composer />}/>
                    <Route path={':notfound'} element={<NotFound />}/>
                </Route>
            </Routes>
        </BrowserRouter>
    </Provider>

)

// root means everything in App https://stackoverflow.com/a/65531078/6501621

