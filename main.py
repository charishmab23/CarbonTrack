import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Carbon Footprint Calculator",
    page_icon="🌍",  
    layout="centered",  
    initial_sidebar_state="expanded"  
)

# Set the theme colors
st.markdown(
    """
    <style>
    .stApp {
        background-color: #D2F7FF;  /* Background color */
    }
    
    /* Style for the Start button (standalone) */
    div.stButton > button {
        background-color: #FFFFFF; /* White background for Start button */
        color: black;              /* Black text for Start button */
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;        /* Rounded corners */
    }

    /* Optional: Hover effect for Start button */
    div.stButton > button:hover {
        background-color: #45a049; /* Darker green on hover */
    }

    /* Style for Next and Submit buttons (inside forms) */
    div.stForm button {
        background-color: #FFFFFF; /* White background to match Start button */
        color: inherit;            /* Keep the default color (inherited from form) */
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;        /* Rounded corners */
    }

    /* Optional: Hover effect for Next and Submit buttons */
    div.stForm button:hover {
        background-color: #45a049; /* Darker green on hover */
    }

    /* Set all text to black */
    body, h1, h2, h3, h4, h5, h6, p, span {
        color: #000000;  /* Text color */
    }
    </style>
    """,
    unsafe_allow_html = True
)


# Initialize session state for the dict if not already present
if "carbon_data" not in st.session_state:
    st.session_state.carbon_data = {
        "primaryTransport": "",
        "mpg": 0,
        "transportation_footprint": 0,
        "electricity_usage": "",
        "electricity_footprint": 0,
        "diet_type": "",
        "diet_footprint": 0,
        "clothes_purchased": "",
        "shopping_footprint": 0,
        "water_consumed": 0,
        "water_footprint": 0,
        "carbon_footprint": 0
    }

# Initialize the session state for the page if it doesn't exist
if "page" not in st.session_state:
    st.session_state.page = "intro"

def intro_page():
    st.title("Annual Carbon Footprint Calculator")
    st.write("See how much of an impact your daily activities have on our climate, and changes you can make to your routine to reduce your contribution!")
    st.image("earth.png", width=200)
    st.markdown(
        """
        <div style="text-align: center;">
            <span style="color: black; font-size: 18px;">Protect our Planet!!</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    if st.button("Start"):
        st.session_state.page = "question1"

def show_first_question():
    st.title("Transportation")
    
    with st.form(key="transport_form"):
        st.session_state.carbon_data["primaryTransport"] = st.radio(
            "What is your primary mode of transportation?",
            ["Car", "Public Transport", "Walking/Bicycle", "Airplane"]
        )
        submit = st.form_submit_button("Next")
    
    if submit:
        if st.session_state.carbon_data["primaryTransport"] == "Car":
            st.session_state.page = "question1_part2"
        else:
            st.session_state.page = "question2"

def show_first_question_part2():
    st.title("Transportation")
    
    with st.form(key="mpg_form"):
        st.session_state.carbon_data["mpg"] = st.number_input("If you answered car, what is your fuel economy (mpg)?", min_value=0)
        submit = st.form_submit_button("Next")
    
    if submit:
        st.session_state.page = "question2"

def show_second_question():
    st.title("Energy Consumption")
    
    with st.form(key="energy_form"):
        st.session_state.carbon_data["electricity_usage"] = st.radio(
            "What is your primary source of home energy?",
            ["Electricity(renewable)", "Electricity(non-renewable)", "Natural Gas", "Other(wood, propane)"]
        )
        submit = st.form_submit_button("Next")
    
    if submit:
        st.session_state.page = "question3"

def show_third_question():
    st.title("Diet")
    
    with st.form(key="diet_form"):
        st.session_state.carbon_data["diet_type"] = st.radio(
            "How would you categorize your diet?",
            ["Omnivore", "Vegetarian", "Vegan"]
        )
        submit = st.form_submit_button("Next")
    
    if submit:
        st.session_state.page = "question4"

def show_fourth_question():
    st.title("Shopping")
    
    with st.form(key="shopping_form"):
        st.session_state.carbon_data["clothes_purchased"] = st.radio("On average, how many articles of clothing do you purchase in a month?", ["0-2", "3-6", "7-12", "13-20", "21+"])
        submit = st.form_submit_button("Next")
    
    if submit:
        st.session_state.page = "question5"

def show_fifth_question():
    st.title("Water Usage")
    
    with st.form(key="water_form"):
        st.session_state.carbon_data["water_consumed"] = st.number_input("Monthly water usage (gallons):", min_value=0)
        submit = st.form_submit_button("Submit")
    
    if submit:
        calculateCarbon()
        st.session_state.page = "results"

def calculateCarbon():
    # Retrieve data from session state for calculations
    carbon_data = st.session_state.carbon_data
    
    # Calculating carbon emissions from transportation
    if carbon_data["primaryTransport"] == "Car":
        carbon_data["transportation_footprint"] = (12000 / carbon_data["mpg"]) * 19.6
    elif carbon_data["primaryTransport"] == "Airplane":
        carbon_data["transportation_footprint"] = 2000 * 0.2
    elif carbon_data["primaryTransport"] == "Public Transport":
        carbon_data["transportation_footprint"] = 500 * 0.1
    elif carbon_data["primaryTransport"] == "Walking/Bicycle":
        carbon_data["transportation_footprint"] = 0

    # Calculating carbon emissions from energy consumption    
    if carbon_data["electricity_usage"] == "Electricity(renewable)":
        carbon_data["electricity_footprint"] = 0
    elif carbon_data["electricity_usage"] == "Electricity(non-renewable)":
        carbon_data["electricity_footprint"] = 10000 * 0.92
    elif carbon_data["electricity_usage"] == "Natural Gas":
        carbon_data["electricity_footprint"] = 800 * 11.7
    elif carbon_data["electricity_usage"] == "Other(wood, propane)":
        carbon_data["electricity_footprint"] = 200 * 12.7

    # Calculating carbon emissions from diet    
    if carbon_data["diet_type"] == "Omnivore":
        carbon_data["diet_footprint"] = 5600
    elif carbon_data["diet_type"] == "Vegetarian":
        carbon_data["diet_footprint"] = 3900
    elif carbon_data["diet_type"] == "Vegan":
        carbon_data["diet_footprint"] = 2600

    # Calculating carbon emissions from shopping    
    if carbon_data["clothes_purchased"] == "0-2":
        carbon_data["shopping_footprint"] = 1 * 25 * 12
    elif carbon_data["clothes_purchased"] == "3-6":
        carbon_data["shopping_footprint"] = 4.5 * 25 * 12
    elif carbon_data["clothes_purchased"] == "7-12":
        carbon_data["shopping_footprint"] = 9.5 * 25 * 12
    elif carbon_data["clothes_purchased"] == "13-20":
        carbon_data["shopping_footprint"] = 16.5 * 25 * 12
    elif carbon_data["clothes_purchased"] == "21+":
        carbon_data["shopping_footprint"] = 30 * 25 * 12
    
    # Calculating carbon emissions from water usage   
    carbon_data["water_footprint"] = 0.001 * carbon_data["water_consumed"] * 12

    # Summing up all footprints to calculate total carbon footprint
    carbon_data["carbon_footprint"] = (
        carbon_data["transportation_footprint"] +
        carbon_data["electricity_footprint"] +
        carbon_data["diet_footprint"] +
        carbon_data["shopping_footprint"] +
        carbon_data["water_footprint"]
    )
    # Update session state with final results
    st.session_state.carbon_data = carbon_data

def show_results():
    st.title(f"Your annual carbon footprint is about: {round(st.session_state.carbon_data['carbon_footprint'])} lb CO2")
    st.write("Globally, the average person's carbon emissions per year is around 11000 lbs.")
    if(round(st.session_state.carbon_data['carbon_footprint']) < 10000):
        st.write("Great work! You are below the global average :)")
    elif(round(st.session_state.carbon_data['carbon_footprint']) > 12000):
        st.write("You are above the global average..consider your footprint breakdown below and try more globally-friendly practices accordingly; the planet will thank you!")
    else:
        st.write("You are right about average, consider your footprint breakdown below where you could make some small changes :)")
    
    st.write("")
    st.write(f"Your Transportation Footprint: {round(st.session_state.carbon_data['transportation_footprint'])} lb CO2")
    st.write(f"Your Electricity Footprint: {round(st.session_state.carbon_data['electricity_footprint'])} lb CO2")
    st.write(f"Your Diet Footprint: {round(st.session_state.carbon_data['diet_footprint'])} lb CO2")
    st.write(f"Your Shopping Footprint: {round(st.session_state.carbon_data['shopping_footprint'])} lb CO2")
    st.write(f"Your Water Usage Footprint: {round(st.session_state.carbon_data['water_footprint'])} lb CO2")

# Render the appropriate page based on session state
if st.session_state.page == "intro":
    intro_page()
elif st.session_state.page == "question1":
    show_first_question()
elif st.session_state.page == "question1_part2":
    show_first_question_part2()
elif st.session_state.page == "question2":
    show_second_question()
elif st.session_state.page == "question3":
    show_third_question()
elif st.session_state.page == "question4":
    show_fourth_question()
elif st.session_state.page == "question5":
    show_fifth_question()
elif st.session_state.page == "results":
    show_results()
