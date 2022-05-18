import './App.css';
import { Button } from 'react-bootstrap';
import Carousel from './components/carousel';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
      <div className={"container-fluid"}>
        <main>
          <Carousel />
        </main>
      </div>
  );
}

export default App;
