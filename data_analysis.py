import pandas as pd
import numpy as np

# Load the crop data and soil moisture data
crop_data = pd.read_csv('crop_data.csv')
soil_data = pd.read_csv('soil_moisture1.csv')

# Comment out or remove these print statements
# print(soil_data.head())
# print(crop_data.head())

def perform_soil_moisture_analysis(crop_name, soil_type, latitude, longitude, crop_age):
    # Filter crop data based on crop name and soil type
    crop_info = crop_data[(crop_data['Crop Name'] == crop_name) & (crop_data['Soil Type'] == soil_type)]
    
    if crop_info.empty:
        return f"No data found for crop '{crop_name}' and soil type '{soil_type}'."

    # Determine the growth phase based on crop age
    total_days = 0
    for _, row in crop_info.iterrows():
        total_days += row['Duration of Phase (days)']
        if crop_age <= total_days:
            growth_phase = row['Growth Phase']
            break
    else:
        return f"The crop has exceeded the growth phases defined in the dataset."

    # Get the required moisture for the determined growth phase
    required_moisture = crop_info[crop_info['Growth Phase'] == growth_phase]['Optimal Soil Moisture Content (cm³/cm³)'].values[0]

    # Find the nearest latitude and longitude in the soil data
    soil_data['distance'] = np.sqrt((soil_data['latitude'] - latitude)**2 + (soil_data['longitude'] - longitude)**2)
    nearest_soil_data = soil_data.loc[soil_data['distance'].idxmin()]

    # Get the soil moisture from the nearest data point
    actual_soil_moisture = nearest_soil_data['adjusted_soil_moisture']

    if pd.isna(actual_soil_moisture):
        return {
            'Crop Name': crop_name,
            'Soil Type': soil_type,
            'Growth Phase': growth_phase,
            'Actual Soil Moisture': 'Data not available',
            'Required Moisture': required_moisture,
            'Irrigation Needed': 'N/A',
            'Irrigation Amount (mm)': 'N/A'
        }

    # Calculate if irrigation is needed and how much
    irrigation_needed = actual_soil_moisture < required_moisture
    irrigation_amount = max(0, (required_moisture - actual_soil_moisture) * 1000)  # Convert to mm

    return {
        'Crop Name': crop_name,
        'Soil Type': soil_type,
        'Growth Phase': growth_phase,
        'Actual Soil Moisture': round(actual_soil_moisture,5),
        'Required Moisture': required_moisture,
        'Irrigation Needed': 'Yes' if irrigation_needed else 'No',
        'Irrigation Amount (mm)': round(irrigation_amount, 2)
    }

# # Example latitude and longitude values
# latitude = 68.51881  # Replace with the latitude you are testing
# longitude = -179.81328  # Replace with the longitude you are testing

# Check if the latitude and longitude exist in the soil_data DataFrame
# matching_rows = soil_data[(soil_data['latitude'] == latitude) & (soil_data['longitude'] == longitude)]
# print(matching_rows)
