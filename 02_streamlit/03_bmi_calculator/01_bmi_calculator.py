# import the streamlit library
import streamlit as st

# give a title to our app
st.title('Welcome to BMI Calculator')

# TAKE WEIGHT INPUT in kgs
weight = st.number_input("Enter your weight (in kgs)")

# TAKE HEIGHT INPUT
status = st.radio('Select your height format:', ('cms', 'meters', 'feet'))

height = 0
bmi = None  # Initialize bmi outside try block

if status == 'cms':
    height = st.number_input('Centimeters')
    if height > 0:
        bmi = weight / ((height / 100) ** 2)

elif status == 'meters':
    height = st.number_input('Meters')
    if height > 0:
        bmi = weight / (height ** 2)

else:
    height = st.number_input('Feet')
    if height > 0:
        bmi = weight / ((height / 3.28) ** 2)

# Check if the button is pressed
if st.button('Calculate BMI'):
    if bmi is not None:
        st.text("Your BMI Index is {:.2f}.".format(bmi))

        # give the interpretation of BMI index
        if bmi < 16:
            st.error("You are Extremely Underweight")
        elif 16 <= bmi < 18.5:
            st.warning("You are Underweight")
        elif 18.5 <= bmi < 25:
            st.success("Healthy")
        elif 25 <= bmi < 30:
            st.warning("Overweight")
        else:
            st.error("Extremely Overweight")
    else:
        st.warning("Please enter valid height to calculate BMI.")
