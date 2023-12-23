import pandas as pd
import pickle  # Import pickle for loading the model

# Function to reformat date columns
def reformat_date_columns(dataframe):
    date_columns = [col for col in dataframe.columns if '-' in col]
    for col in date_columns:
        new_col_name = '-'.join(col.split('-')[:2])
        dataframe.rename(columns={col: new_col_name}, inplace=True)
    return dataframe


def predict_with_saved_model(model_path, county, budget, forecast_years, dataset_path):
    # Load the saved models using pickle
    with open(model_path, 'rb') as file:
        saved_models = pickle.load(file)

    # Load dataset
    housing_market_data = pd.read_csv(dataset_path)
    housing_market_data = reformat_date_columns(housing_market_data)

    zip_predictions = {}
    for zipcode, group in housing_market_data.groupby('RegionName'):
        if group['CountyName'].iloc[0] == county and group.iloc[-1, -2] <= budget:  # Filtering by county and budget
            if zipcode in saved_models:
                model = saved_models[zipcode]
                forecast = model.get_forecast(steps=12 * forecast_years)
                prediction = forecast.predicted_mean

                last_actual = group.iloc[-1, -2]  # Assuming second last column is the price
                predicted_value = prediction.iloc[-1]
                growth_rate = (predicted_value - last_actual) / last_actual

                zip_predictions[zipcode] = growth_rate

    top_5_zips = sorted(zip_predictions.items(), key=lambda x: x[1], reverse=True)[:5]
    return top_5_zips
