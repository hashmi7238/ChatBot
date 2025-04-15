import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import hashlib
import datetime

# Excel file to store users
EXCEL_FILE = 'users.xlsx'

# Function to load users from the Excel file
def load_users():
    """Load users from Excel file."""
    try:
        df = pd.read_excel(EXCEL_FILE)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['email', 'username', 'password', 'date_joined'])

# Function to save users to the Excel file
def save_users(df):
    """Save updated users to the Excel file."""
    df.to_excel(EXCEL_FILE, index=False)

# Function to insert a new user into the Excel file
def insert_user(email, username, password):
    """Insert new user into Excel file."""
    df = load_users()
    date_joined = str(datetime.datetime.now())
    new_user = pd.DataFrame({
        'email': [email],
        'username': [username],
        'password': [password],
        'date_joined': [date_joined]
    })
    df = pd.concat([df, new_user], ignore_index=True)
    save_users(df)

# Function to check if an email already exists
def get_user_emails():
    """Get a list of all user emails from Excel."""
    df = load_users()
    return df['email'].tolist()

# Function to check if a username already exists
def get_usernames():
    """Get a list of all usernames from Excel."""
    df = load_users()
    return df['username'].tolist()

# Function to validate email format
def validate_email(email):
    """Check if email is valid."""
    return '@' in email and '.' in email

# Sign-up form function
def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader('Sign Up')
        email = st.text_input('Email', placeholder='Enter Your Email')
        username = st.text_input('Username', placeholder='Enter Your Username')
        password1 = st.text_input('Password', placeholder='Enter Your Password', type='password')
        password2 = st.text_input('Confirm Password', placeholder='Confirm Your Password', type='password')

        # Sign up button
        if st.form_submit_button('Sign Up'):
            # Validation checks
            if email and username and password1 and password2:
                if validate_email(email):
                    if email not in get_user_emails():
                        if username not in get_usernames():
                            if password1 == password2:
                                # Hash the password before storing
                                hashed_password = hashlib.sha256(password1.encode()).hexdigest()
                                insert_user(email, username, hashed_password)
                                st.success('Account created successfully!')
                                st.balloons()
                            else:
                                st.error('Passwords do not match!')
                        else:
                            st.error('Username already exists!')
                    else:
                        st.error('Email already exists!')
                else:
                    st.error('Invalid email format!')
            else:
                st.error('Please fill in all fields!')

# Authenticate users from the Excel file
def authenticate_users():
    # Load users
    df = load_users()
    emails = df['email'].tolist()
    usernames = df['username'].tolist()
    passwords = df['password'].tolist()

    # Create a credentials dictionary for streamlit_authenticator
    credentials = {'usernames': {}}
    for i in range(len(usernames)):
        credentials['usernames'][usernames[i]] = {'name': emails[i], 'password': passwords[i]}

    # Set up authentication
    authenticator = stauth.Authenticate(credentials, 'app_name', 'abcdef', cookie_expiry_days=30)

    return authenticator

# Streamlit App
st.title('User Sign Up and Authentication')

# Display Sign Up form
if st.sidebar.button('Sign Up'):
    sign_up()

authenticator = authenticate_users()
# Display Login form
if st.sidebar.button('Login'):
    authenticator.login(location="main")
