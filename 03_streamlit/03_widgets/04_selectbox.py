# import streamlit as st
# import pandas as pd

# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# })

# # Combine the two columns into a single list for the selectbox options
# all_options = df['first column'].tolist() + df['second column'].tolist()

# option = st.selectbox(
#     'Which number do you like best?',
#     all_options
# )

# st.write('You selected: ', option)

#####--------------------------------------------------------------------------#####

import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

# First selectbox: Choose which column to display
column_choice = st.selectbox(
    'From which column do you want to pick a number?',
    df.columns.tolist() # Gives 'first column', 'second column' as options
)

# Second selectbox: Display numbers from the chosen column
if column_choice: # Ensure a column has been selected
    option = st.selectbox(
        f'Which number from "{column_choice}" do you like best?',
        df[column_choice]
    )
    st.write('You selected: ', option)