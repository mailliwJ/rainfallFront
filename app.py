import streamlit as st
from requests import request
from requests.exceptions import RequestException

# =====================================================================================================================================================================

BASE_URL = 'https://mailliwj.pythonanywhere.com'

# Endpoints
HOME_URL = f'{BASE_URL}/home'
PREDICT_URL = f'{BASE_URL}/predict'
RETRAIN_SAVE_URL = f'{BASE_URL}/retrain_save'
DELETE_URL = f'{BASE_URL}/reset_remove'
RUN_URL = f'{BASE_URL}/reset_run'

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
st.set_page_config(layout='wide')

def main():
    menu = st.sidebar.radio('Menu', ['Home', 'Predict', 'Retrain Model'], index=0)

    if menu == 'Home':
        home()
    elif menu == "Predict":
        predict()
    elif menu == 'Retrain Model':
        retrain()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def home():    
    st.title('Welcome to RainFall')

    st.markdown("""
    This application is designed to predict rainfall based on a set of climatic parameters.  
    You can also retrain the prediction model using new data saved as a CSV file.

    ### How to use RainFall:
    1. **Predict**:
    - Navigate to the ***Predict*** page using the sidebar.
    - Enter values for the required climatic parameters and click ***'Predict Rainfall'***.
    
    2. **Retrain Model**:
    - Navigate to the **Retrain Model** page using the sidebar.
    - Upload a CSV file containing new training data to retrain the model.
    - For details of the required structure of the CSV file, see below.
    
    ### Example CSV File
    To retrain the model you should upload a CSV file that has the following header line:
    
    date,cloud_cover,sunshine,global_radiation,max_temp,mean_temp,min_temp,precipitation,pressure,snow_depth
    """)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def predict():
    st.title('Make a rainfall prediction')
    st.markdown('Enter values for the climatic paramters to predict rainfall in mm')

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
    st.write('1. Upload a CSV file containing the latest climatic data and retrain the model.')
    st.write('2. Compare the new performance metrics to the currently stored metrics.')
    st.write('3. Choose whether to save the updated dataset and retrained model or keep what you had previously.')


    upload_file = st.file_uploader('Choose a CSV file to upload', type='csv')

    if upload_file is not None:
        st.session_state['uploaded_file'] = upload_file
        st.success('File uploaded successfully. Click "Retrain & Evaluate"')

        if st.button('Retrain & Evaluate'):
            if 'uploaded_file' not in st.session_state:
                st.error('No file uploaded. Please upload a CSV file first')
                return

            file = st.session_state['uploaded_file']
            file = {'file': (file.name, file, 'text/csv')}

            with st.spinner('Retraining model and evaluating...'):
                st.write('Sending file payload:', file)
                result = make_request('POST', RETRAIN_SAVE_URL, files=file, params={'action':'evaluate'})

                if result:
                    st.session_state['current_metrics'] = result.get('Current Evaluation Metrics')
                    st.session_state['new_metrics'] = result.get('New Evaluation Metrics')
                    st.session_state['evaluation_complete'] = True
                    st.success('Model retrained and evaluated successfully')
                else:
                    st.error('Failed to re-evaluate the model')

        if st.session_state.get('evaluation_complete'):
            st.subheader('Evaluation Metrics')
                    
            left_table, right_table = st.columns(2)
            with left_table:
                st.markdown('Current Model Metrics')
                st.dataframe(st.session_state['current_metrics'], hide_index=True, column_order=['Model','MSE','RMSE','MAPE'])
                    
            with right_table:
                st.markdown('Updated Dataset Metrics')
                st.dataframe(st.session_state['new_metrics'], hide_index=True, column_order=['Model','MSE','RMSE','MAPE'])

            if st.button('Save Dataset and Retrained Model'):
                with st.spinner('Saving data and retraining model...'):
                    file = {'file': ('uploaded_file', st.session_state['uploaded_file'])}
                    save_result = make_request('POST', RETRAIN_SAVE_URL, files=file, params={'action':'save'})
                    
                    if save_result:
                        st.success('Dataset and model saved successfully.')
                    else:
                        st.error('Failed to save updated model and dataset')
            
            elif st.button('Reject Updates'):
                st.warning('Updates rejected. Original model and dataset preserved')            

# ================================================================================================================================================================================================================================================================

if __name__ == '__main__':
    main()