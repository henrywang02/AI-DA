## Phase 1 (Business Understanding)

### 1. Define Business Objectives

- Optimizing Pricing Strategies: Analyzing pricing trends to help dealerships set competitive prices. 
- Understanding Vehicle Demand: Indentifying key factors that influence vehicle sales. 
- Enhancing Customer Decision Making: Providing insights to customers about vehicle quaility, reliability, and market trends. 
- Improving Inventory Management: Helping dealerships manage stock by predicting demand for different car models. 

### 2. Dataset Information: 

The dataset contains 3 million real-world used car details. This data was obtained by running a self-made web crawler on the Cargunus inventory in September 2020. This data is for academic, research, and individual experimentation only and its not intended for commercial purposes. Here is the [aggle link to dataset](https://www.kaggle.com/datasets/ananaymital/us-used-cars-dataset) by the author AnanayMital.

**Inspiration:** 
The dataset can be used to build applications, such as: 
- Predictive models to determine which features of a vehicle influence price fluctuations. 
- An analysis to identify factors affecting the selling time of a used vehicle. 

### 3. Analyze the Current Situation: 

**Data Availability**: The dataset contains comprehensive details about used cars, including VIN, fuel economy, engine type, pricing, delear information, and more. 

**Challenges:** 
  + Missing or inconsistent data (e.g., mising values for bed size in non-pickup trucks). 
  + Potential outliers in pricing and mileage. 
  + Variation in vehicle descriptions and specifications. 

**Opportunities:** 
  + Rich dataset allows for deep market analysis. 
  + Potential to integrate with external sources for enhanced insights (e.g., histoical sales data, economic trends). 

### 4. Define Initial Goals of Data Analysis 

1. Identify Factors Affecting Pricing: Analyse how different attributes (e.g., engine type, mileage, condition) impact vehicle prices. 
1. Predict Days on Market: Develop models to estimate how long a car will take to sell based on its attributes. 
2. Market Trend Analysis: Understand fuel efficiency trends, demand for electric vehicles, and geographic preferences.

### 5. Define Initial Goals of Modelling 

**Regression Models:** 
   + Price Prediction Model: Estimate car prices based on attributes. 
   + Fuel Economy Estimation: Predict fuel efficiency based on car specifications. (optional) 

**Classification Models:** 
   + Vehicle Type Classification: Categorize vehicles into body types, fuel types, or transmission types.

### 6. Define the Project's Goals 
**Short-Term Goals:** 
   1. Clean and preprocess the dataset. 
   1. Perform exploratory data analysis (EDA) to uncover initial insights. 
   1. Develop basic models for price estimation and demand prediction. 

**Long-Term Goals:** 
  1. Deploy a machine learning model for dealerships to optimize pricing strategies. 
  2. Develop a recommendation system for customers. (Optional) 
  3. Integrate with external APIs to provide real-time vehicle pricing insights. (Optional) 

### 7. Measuring Success 

**Model Performance Metrics:**
   + Price Prediction: RMSE, MAE, R-squared. 
   + Classification Models: Precision, Recall, F1-score. 

**Business Impact Metrics:**
   + Reduction in days on market for listed cars. 
   + Increased sales through optimized pricing. 
   + Improved customer satisfaction based on data-driven recommendations. 

### 8. Customer 

**Who is the main customer?**
- The primary client is a car store chain operating in the USA with commercial interests in utilizing data analytics for future trading. The chain's core business is the sale of used vehicles, independent of the car brand. 

**Customer Requirements** 
The customer is particularly interested in: 
- Understanding what features affect the price and sale time of used vehicles. 
- Insights into various vehicle types and manufacturers to enhance their stock strategy. 
- Identifying which used cars sell faster to optimize inventory and reduce storage costs. 
- Analyzing the impact of additional features (e.g., Bluetooth, navigation system) on the selling price. 
- Predicting price and/or sale time based on vehicle characteristics. 

A reference example of a similar company in Finland is Kamux, a stock-listed, internationally operating used car dealership chain. 
The measurement data used for this analysis was collected in 2020 over approximately one year. 

### 9. Technologies Used 
- Data Processing: Python (Pandas, NumPy), SQL (If needed). 
- Visualization: Matplotlib, Seaborn. 
- Machine Learning: Scikit-Learn, TensorFlow, some ML frameworks.

### 10. Required Skills

- Data Analysis & Preprocessing: Experience with Pandas, NumPy, data cleaning techniques. 
- Visualization: Using Python libraries to do visualisations and data analysis.
- Machine Learning: Experience with regression, classification, and clustering models. 
- Database Management: SQL databases. (deployment)
- Reporting: Creating interactive dashboards and data reports. (out of scope for now)

### 11. Work Distribution

| Task                            | Responsible Party     |
| ------------------------------- | --------------------- |
| Phase 1: Business Understanding | Shared responsibility |
| Phase 2: Data Understanding     | Shared responsibility |
| Phase 3: Data Preparation       | Shared responsibility |
| Phase 4: Modeling               | Shared responsibility |
| Phase 5: Evaluation             | Shared responsibility |
| Phase 6: Deployment             | Shared responsibility |
| Phase 7: Final report           | Shared responsibility |

### Next Steps 

1. Conduct Exploratory Data Analysis (EDA) and clean missing data. 
2. Identify key variables affecting pricing and demand. 
3. Develop a prototype machine learning model for price prediction. 
4. Validate models with real-world test data and refine them. 
5. Deploy initial insights via a dashboard or API. (If needed)
