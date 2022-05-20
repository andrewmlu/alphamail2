import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import { BrowserRouter, Outlet, Link } from 'react-router-dom';

// DONE 2022.05.19-22.20 learn react router
function App() {
    return (
        <div className={"container-fluid"}>
            <main>
                <div className="wrapper container-fluid pt-4 p-4">
                    {/* DONE 22.05.19-20.52 fix home button link color */}
                    <Link to={'/'} id={'home-logo'}>
                        <h2 className="font-weight-light mt-2">Alphamail, powered by Bootstrap, React, and Flask</h2>
                    </Link>
                    <Outlet />
                </div>
            </main>
        </div>
    );
}

export default App;
