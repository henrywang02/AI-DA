import React, { useState, useEffect } from 'react';
import { fetchLabelMappings, fetchOpenApiSchema, insertTrainingRow, retrainModels } from '../services/api';
import { VALID_FIELDS } from './configs';


const AddTrainingRowForm = () => {
    const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
    const [formData, setFormData] = useState<any>({});
    const [labelMappings, setLabelMappings] = useState<any>({});

    useEffect(() => {
        const init = async () => {
            const mappings = await fetchLabelMappings();
            const openapi = await fetchOpenApiSchema();

            const example = openapi.components.schemas.CarFeaturesWithPrice?.example || {};
            setFormData(example);
            setLabelMappings(mappings);
        };
        init();
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: parseFloat(value) || 0 });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await insertTrainingRow(formData);
        alert('Training row added successfully!');
    };

    return (
        <>
            <form onSubmit={handleSubmit} className='add_training_row'>
                <h2>Training Row Addition form</h2>

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

                {/* Numerical fields */}
                {[
                    'horsepower', 'maximum_seating', 'mileage', 'torque', 'year', 'combined_fuel_economy',
                    'legroom', 'major_options_count', 'size_of_vehicle', 'price'
                ].map(field => (
                    <div key={field}>
                        <label>{field}</label>
                        <input
                            type="number"
                            name={field}
                            value={formData[field] ?? ''}
                            onChange={handleChange}
                            required
                        />
                    </div>
                ))}
                <div>
                    <button type="submit">Add Training Row</button>
                    <button className='retrain' onClick={(e) => {
                        e.preventDefault()
                        retrainModels()
                        }}>Retrain</button>
                </div>
            </form>
        </>
    );
};

export default AddTrainingRowForm;
