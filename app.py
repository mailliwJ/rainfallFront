import streamlit as st
from requests import request
from requests.exceptions import RequestException

# =====================================================================================================================================================================

BASE_URL = 'https://mailliwj.pythonanywhere.com'

# Endpoints
HOME_URL = f'{BASE_URL}/'
PREDICT_URL = f'{BASE_URL}/predict'
RETRAIN_SAVE_URL = f'{BASE_URL}/retrain_save'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# https://tinyurl.com/raiseStatusCode
# Helper function to make API requests keep code neater
def make_request(method, url, **kwargs):
    try:
        response = request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        st.error(f'Error contacting the API: {e}')
        return None

# =====================================================================================================================================================================

def main():
    st.title('Rainfall Prediction Application')
    st.sidebar.title('')

    menu = st.sidebar.radio('Menu', ['Predict', 'Retrain Model'])
    if menu == "Predict":
        predict()
    elif menu == 'Retrain Model':
        retrain()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def predict():
    st.title('Make a rainfall predictions')
    st.markdown('Enter climatic paramters to predict rainfall in mm')

    cloud_cover = st.number_input('Cloud Cover (oktas)', min_value=0, max_value=500)
    sunshine = st.number_input('Sunshine (hours)', min_value=0, max_value=24)
    global_radiation = st.number_input('Global Radiation (W/m2)', min_value=0, max_value=200000)
    max_temp = st.number_input('Max Temperature (oC)', min_value=-50, max_value=50)
    mean_temp = st.number_input('Mean Temperature (oC)', min_value=-50, max_value=50)
    min_temp = st.number_input('Min Temperature (oC)', min_value=-50, max_value=50)
    pressure = st.number_input('Pressure (kPa)', min_value=0, max_value=500)

    if st.button('Predict Rainfall'):
        payload = {
            'cloud_cover': cloud_cover,
            'sunshine': sunshine,
            'global_radiation': global_radiation,
            'max_temp': max_temp,
            'mean_temp': mean_temp,
            'min_temp': min_temp,
            'pressure': pressure
            }

        with st.spinner('Making prediction...'):
            result = make_request('POST', PREDICT_URL, json=payload)
            if result:
                prediction = result.get('Prediction', None)

                if prediction is not None:
                    st.success(f'The predicted rainfall is {prediction:.1f}mm')
                else:
                    st.error('Could not retrieve a valid prediction from the API')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def retrain():
    st.title('Update Training Data and Retrain Model')
    st.write(f'Upload a CSV file containing the latest climatic data\nRetrain the model and then compare the performance metrics')

    upload_file = st.file_uploader('Choose a CSV file to upload', type='csv')
    file = {'file': ('new_data.csv', upload_file, 'text/csv')}

    if upload_file is not None:
        st.write('File uploaded successfully. Click "Retrain & Evaluate"')

        if st.button('Retrain & Evaluate'):
            with st.spinner('Retraining model and evaluating...'):
                result = make_request('POST', RETRAIN_SAVE_URL, files=file)

                if result:
                    st.success('Model retrained and evaluated')
                    
                    st.subheader('Metric Evaluations')
                    
                    left_table, right_table = st.columns(2)
                    with left_table:
                        st.markdown('Current Model Metrics')
                        st.dataframe(result['Current Evaluation Metrics'])
                    
                    with right_table:
                        st.markdown('Updated Dataset Metrics')
                        st.dataframe(result['New Evaluation Metrics'])

                    if st.button('Save Dataset and Retrain Model'):
                        with st.spinner('Saving data and retraining model...'):
                            save_result = make_request('PUT', RETRAIN_SAVE_URL, files=file)
                            if save_result:
                                st.success('Dataset and model saved successfully.')
                            else:
                                st.error('Failed to save updated model and dataset')

                    elif st.button('Reject Updates'):
                        st.warning('Updates rejected. Original model and dataset preserved')

# ================================================================================================================================================================================================================================================================

if __name__ == '__main__':
    main()