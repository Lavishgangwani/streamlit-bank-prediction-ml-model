import streamlit as st
import pickle
import numpy as np

# Load the trained model
model = pickle.load(open('x_g_boost_model.pkl', 'rb'))

# Function to predict churn
def predict_churn(creditscore, age, tenure, saving_account, creditcard, isactivemember):
    prediction = model.predict(np.array([
        creditscore,
        age,
        tenure * 12,  # Convert tenure to months
        saving_account, 
        creditcard, 
        isactivemember
    ]).reshape(1, -1))
    return prediction

# Define the Streamlit app
def main():
    # Set page title and icon
    st.set_page_config(page_title="Customer Churn Prediction", page_icon="🔮")

    # Custom CSS to style the header background color
    header_bg = """
    <style>
    .css-1l02zno {
        background-color: orange;
    }
    </style>
    """
    st.markdown(header_bg, unsafe_allow_html=True)

    # Add a title and description to the app
    st.title("Customer Churn Prediction App")
    st.write("Welcome to the Customer Churn Prediction App! Enter customer details below to predict churn probability.")

    # Add input fields for user to enter data
    creditscore = st.slider("Credit Score", min_value=0, max_value=850, step=1, value=0)
    age = st.slider("Age", min_value=18, max_value=100, step=1, value=18)
    tenure = st.slider("Tenure (years)", min_value=0, max_value=10, step=1, value=0)
    saving_account = st.selectbox("Savings Account", ["Low", "Medium", "High"])
    creditcard = st.selectbox("Has Credit Card", ["No", "Yes"])
    isactivemember = st.selectbox("Is Active Member", ["No", "Yes"])

    # Map selectbox values to integers
    saving_account_mapping = {"Low": 1, "Medium": 2, "High": 3}
    saving_account = saving_account_mapping[saving_account]
    creditcard = 1 if creditcard == "Yes" else 0
    isactivemember = 1 if isactivemember == "Yes" else 0

    # Predict churn
    if st.button("Predict Churn"):
        prediction = predict_churn(creditscore, age, tenure, saving_account, creditcard, isactivemember)
        # Display prediction result
        result = "Yes, the customer is likely to churn." if prediction == 1 else "No, the customer is not likely to churn."
        st.success("Churn prediction: {}".format(result))

    # Add a footer with additional information
    st.write("---")
    st.write("Remember: 'The only limit to our realization of tomorrow will be our doubts of today.' - Franklin D. Roosevelt")

# Run the Streamlit app
if __name__ == "__main__":
    main()
