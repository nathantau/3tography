import logo from './logo.svg';
import './App.css';

import Home from './components/Home';

function App() {

//   const getData = () => {
//     fetch('http://localhost:5000/')
//     .then(e => e.text())
//     .then(e => console.log(e))
//     .catch(e => console.log('error is ', e))
//   }

  return (
    <div className="App">
        <Home></Home>
    </div>
  );
}

export default App;
