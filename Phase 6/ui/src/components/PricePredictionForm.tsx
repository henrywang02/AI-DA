import React, { useState, useEffect, useRef } from 'react';
import { fetchLabelMappings, fetchOpenApiSchema, predictPrice } from '../services/api';
import { VALID_FIELDS } from './configs';


const PricePredictionForm = () => {
  const [formData, setFormData] = useState<any>({});
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [labelMappings, setLabelMappings] = useState<any>({});
  const [result, setResult] = useState<any>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const offset = useRef({ x: 0, y: 0 });
  const resultRef = useRef<HTMLDivElement>(null);
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    const init = async () => {
      const mappings = await fetchLabelMappings();
      const openapi = await fetchOpenApiSchema();
      const example = openapi.components.schemas.CarFeatures?.example || {};
      setFormData(example);
      setLabelMappings(mappings);

      (function pos_up() {
        const parent = formRef.current;
        if (parent) {
          const new_pos = {
            x: (parent.clientWidth / 2) + parent.clientLeft,
            y: (parent.clientHeight / 2) + parent.clientTop
          };
          setPosition(new_pos);
        }
      })();
    };
    init();
  }, []);

  // Predict automatically whenever formData changes
  const predict = async () => {
    try {
      setFieldErrors({});
      const prediction = await predictPrice(formData);
      setResult(prediction);
    } catch (error: any) {
      if (error.response?.status === 422) {
        const newFieldErrors: Record<string, string> = {};
        const details = error.response.data.detail;
        details.forEach((validationError: any) => {
          const loc = validationError.loc;
          const fieldName = loc[loc.length - 1];
          newFieldErrors[fieldName] = validationError.msg;
        });
        setFieldErrors(newFieldErrors);
        setResult(null);
      } else {
        console.error(error);
      }
    }
  };

  useEffect(() => {
    if (Object.keys(formData).length > 0) {
      predict();
    }
  }, [formData]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    predict()
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prevData: any) => ({
      ...prevData,
      [name]: parseFloat(value) || 0
    }));
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (resultRef.current) {
      setIsDragging(true);
      offset.current = {
        x: e.clientX - resultRef.current.offsetLeft,
        y: e.clientY - resultRef.current.offsetTop
      };
    }
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (isDragging) {
      setPosition({
        x: e.clientX - offset.current.x,
        y: e.clientY - offset.current.y
      });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    } else {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    }
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging]);

  return (
    <form onSubmit={handleSubmit} className='price_prediction' ref={formRef}>
      <h2>Price prediction form</h2>

      {Object.keys(labelMappings).map(field => ((VALID_FIELDS.includes(field)) ?
        (<div key={field} className='form-group'>
          <label>{field}</label>
          <select name={field} value={formData[field] ?? ''} onChange={handleChange}>
            {Object.entries(labelMappings[field]).map(([label, code]) => (
              <option key={code} value={code}>{label}</option>
            ))}
          </select>
          {fieldErrors[field] && <p className="field-error">{fieldErrors[field]}</p>}
        </div>) : null
      ))}

      {[
        'horsepower', 'maximum_seating', 'mileage', 'torque', 'year', 'combined_fuel_economy',
        'legroom', 'major_options_count', 'size_of_vehicle'
      ].map(field => (
        <div key={field} className='form-group'>
          <label>{field}</label>
          <input
            type="number"
            name={field}
            value={formData[field] ?? ''}
            onChange={handleChange}
            required
          />
          {fieldErrors[field] && <p className="field-error">{fieldErrors[field]}</p>}
        </div>
      ))}

      <button type="submit" onClick={handleSubmit}>Get Prediction</button>

      {result && (
        <div
          className='prediction_result'
          ref={resultRef}
          onMouseDown={handleMouseDown}
          style={{ position: 'absolute', left: position.x, top: position.y, cursor: 'grab' }}
        >
          <h3>Prediction Results</h3>
          <p>Linear Regression: {result.lr_prediction}</p>
          <p>XGBoost: {result.xgb_prediction}</p>
          <p>MLP: {result.mlp_prediction}</p>
          <button className='close' onClick={() => setResult(null)}>Close</button>
        </div>
      )}
    </form>
  );
};

export default PricePredictionForm;
