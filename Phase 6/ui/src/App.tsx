import AddTrainingRowForm from './components/AddTrainingRowForm';
import PricePredictionForm from './components/PricePredictionForm';
import './App.css'; 

function App() {
  return (
    <>
    <div className="forms-container">
      <AddTrainingRowForm />
      <PricePredictionForm />
    </div>
    </>
  );
}

export default App;
