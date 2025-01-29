import streamlit as st
from datetime import datetime
from fpdf import FPDF
import requests
import os


MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY") 
if not MISTRAL_API_KEY:
    raise ValueError("API key not found. Please set the MISTRAL_API_KEY environment variable.")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"


st.markdown("""
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #0D0D0D;
            color: #EAEAEA;
            margin: 0;
            padding: 0;
        }
        
        .header {
            font-size: 3rem;
            color: #00E5FF;
            font-weight: 700;
            text-align: center;
            margin-top: 40px;
            text-transform: uppercase;
        }

        .subheader {
            font-size: 1.5rem;
            color: #B0B0B0;
            margin-bottom: 40px;
            text-align: center;
        }

        .button {
            background-color: #00E5FF;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 1.2rem;
            border-radius: 50px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            margin-top: 30px;
        }

        .button:hover {
            background-color: #00B8D4;
            transform: scale(1.05);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
        }

        .step-container {
            background-color: #262626;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            width: 80%;
            margin: 0 auto;
            transition: all 0.4s ease;
        }

        .step-container:hover {
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
        }

        .input-field {
            background-color: #1E1E1E;
            border: 2px solid #333;
            border-radius: 12px;
            color: #EAEAEA;
            font-size: 1.2rem;
            padding: 12px 20px;
            width: 100%;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }

        .input-field:focus {
            border-color: #00E5FF;
            outline: none;
            box-shadow: 0 0 5px #00E5FF;
        }

        .select-field, .multi-select-field {
            background-color: #1E1E1E;
            border: 2px solid #333;
            border-radius: 12px;
            color: #EAEAEA;
            font-size: 1.2rem;
            padding: 12px 20px;
            width: 100%;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }

        .select-field:focus, .multi-select-field:focus {
            border-color: #00E5FF;
            outline: none;
            box-shadow: 0 0 5px #00E5FF;
        }

        .footer {
            font-size: 1rem;
            color: #B0B0B0;
            text-align: center;
            margin-top: 40px;
        }

        .step-indicator {
            width: 100%;
            height: 5px;
            background-color: #333;
            border-radius: 10px;
            margin: 20px 0;
        }

        .step-indicator-progress {
            width: 33%;
            height: 100%;
            background-color: #00E5FF;
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        /* Floating Action Button */
        .fab {
            position: fixed;
            right: 30px;
            bottom: 30px;
            background-color: #00E5FF;
            color: white;
            padding: 20px;
            border-radius: 50%;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            font-size: 2rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .fab:hover {
            background-color: #00B8D4;
            transform: scale(1.1);
        }
    </style>
""", unsafe_allow_html=True)


class TravelPlanner:
    def __init__(self):
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 1
        if 'user_inputs' not in st.session_state:
            st.session_state.user_inputs = {}

    def collect_basic_info(self):
        """Collect basic travel information"""
        st.markdown('<p class="header">Welcome to Your Travel Planner!</p>', unsafe_allow_html=True)

        # Destination input
        destination = st.text_input(
            "Where would you like to travel? 🌎",
            help="Enter city, country, or region"
        )

        # Date selection
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date 📅",
                min_value=datetime.now().date(),
                help="Select your travel start date"
            )
        with col2:
            end_date = st.date_input(
                "End Date 📅",
                min_value=start_date,
                help="Select your travel end date"
            )

        # Budget selection
        budget_options = ["Budget", "Moderate", "Luxury"]
        budget = st.select_slider(
            "What's your budget level? 💰",
            options=budget_options,
            value="Moderate",
            help="Select your preferred budget level"
        )

        # Travel purpose
        purpose = st.multiselect(
            "What's the purpose of your trip? 🎯",
            ["Sightseeing", "Adventure", "Relaxation", "Culture", "Food", "Shopping"],
            help="Select all that apply"
        )

        if st.button("Continue to Preferences ➡"):
            if not destination:
                st.error("Please enter a destination.")
                return False
            if not purpose:
                st.error("Please select at least one purpose for your trip.")
                return False

            st.session_state.user_inputs.update({
                "destination": destination,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "duration": (end_date - start_date).days + 1,
                "budget": budget,
                "purpose": purpose
            })
            st.session_state.current_step = 2
            st.rerun()

        return True

    def collect_preferences(self):
        """Collect detailed preferences using Mistral AI for refinement"""
        st.markdown("### 🎯 Travel Preferences")

        # Dietary preferences
        dietary_prefs = st.multiselect(
            "Do you have any dietary preferences? 🍽",
            ["Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-free", "None"],
            help="Select all that apply"
        )

        # Activity preferences
        activity_level = st.select_slider(
            "What's your preferred activity level? 🏃‍♂",
            options=["Very Light", "Light", "Moderate", "Active", "Very Active"],
            value="Moderate",
            help="Select your preferred activity level"
        )

        # Accommodation preferences
        accommodation_prefs = st.multiselect(
            "What are your accommodation preferences? 🏨",
            ["Hotel", "Hostel", "Resort", "Apartment", "Boutique Hotel"],
            help="Select all that apply"
        )

        # Special interests
        special_interests = st.multiselect(
            "Any special interests? ⭐",
            ["History", "Art", "Nature", "Photography", "Local Markets", "Museums", 
             "Nightlife", "Live Music", "Water Sports", "Hiking"],
            help="Select all that apply"
        )

        if st.button("Generate Itinerary ✨"):
            if not accommodation_prefs:
                st.error("Please select at least one accommodation preference.")
                return False

            st.session_state.user_inputs.update({
                "dietary_preferences": dietary_prefs,
                "activity_level": activity_level,
                "accommodation_preferences": accommodation_prefs,
                "special_interests": special_interests
            })
            st.session_state.current_step = 3
            st.rerun()

        return True

    def generate_itinerary_with_mistral(self, user_inputs):
        """Generate a personalized itinerary using Mistral AI"""
        prompt = f"""
        Generate a detailed, day-by-day travel itinerary for a trip to {user_inputs['destination']}.
        The trip duration is {user_inputs['duration']} days, from {user_inputs['start_date']} to {user_inputs['end_date']}.
        The user's preferences are:
        - Budget: {user_inputs['budget']}
        - Purpose: {', '.join(user_inputs['purpose'])}
        - Dietary Preferences: {', '.join(user_inputs.get('dietary_preferences', []))}
        - Activity Level: {user_inputs['activity_level']}
        - Accommodation Preferences: {', '.join(user_inputs['accommodation_preferences'])}
        - Special Interests: {', '.join(user_inputs.get('special_interests', []))}

        Provide a detailed itinerary with morning, afternoon, and evening activities for each day.
        """
        return self.call_mistral_api(prompt)

    def call_mistral_api(self, prompt):
        """Call Mistral AI API to refine inputs or generate suggestions"""
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-tiny",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.error("Failed to call Mistral AI API. Please check your API key and try again.")
            return None

def generate_pdf(user_inputs, itinerary):
    """Generate a PDF version of the itinerary"""
    pdf = FPDF()
    pdf.add_page()

    # Setting up the PDF
    pdf.set_font('Arial', 'B', 16)

    # Title
    pdf.cell(190, 10, f'Travel Itinerary - {user_inputs["destination"].title()}', ln=True, align='C')
    pdf.ln(10)

    # Trip Details
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'Trip Details:', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(190, 10, f'Dates: {user_inputs["start_date"]} to {user_inputs["end_date"]}', ln=True)
    pdf.cell(190, 10, f'Duration: {user_inputs["duration"]} days', ln=True)
    pdf.cell(190, 10, f'Budget Level: {user_inputs["budget"]}', ln=True)
    pdf.ln(5)

    # Preferences
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'Preferences:', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(190, 10, f'Purpose: {", ".join(user_inputs["purpose"])}', ln=True)
    pdf.cell(190, 10, f'Activity Level: {user_inputs["activity_level"]}', ln=True)
    pdf.cell(190, 10, f'Accommodation: {", ".join(user_inputs["accommodation_preferences"])}', ln=True)
    if user_inputs["special_interests"]:
        pdf.cell(190, 10, f'Special Interests: {", ".join(user_inputs["special_interests"])}', ln=True)
    pdf.ln(10)

    # Itinerary
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(190, 10, 'Daily Itinerary', ln=True)
    pdf.ln(5)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(190, 10, itinerary)

    return pdf.output(dest='S').encode('latin1')

def display_itinerary(planner, user_inputs):
    """Display the travel itinerary with Mistral AI"""
    st.markdown("<p class='header'>Your Travel Itinerary</p>", unsafe_allow_html=True)

    # Generating itinerary using Mistral AI
    itinerary = planner.generate_itinerary_with_mistral(user_inputs)
    if itinerary:
        st.write(itinerary)

        # Generating and downloading PDF
        itinerary_pdf = generate_pdf(user_inputs, itinerary)
        st.download_button(
            label="Download Itinerary PDF",
            data=itinerary_pdf,
            file_name="travel_itinerary.pdf",
            mime="application/pdf"
        )

def main():
    """Main function to run the app"""
    planner = TravelPlanner()
    if st.session_state.current_step == 1:
        planner.collect_basic_info()
    elif st.session_state.current_step == 2:
        planner.collect_preferences()
    elif st.session_state.current_step == 3:
        display_itinerary(planner, st.session_state.user_inputs)

if __name__ == "__main__":
    main()
