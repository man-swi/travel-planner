# Travel Planner with Mistral AI

## Overview
This project is a web-based travel planner application built using Streamlit. It leverages the Mistral AI API to generate personalized travel itineraries based on user input. The app guides the user through collecting basic travel details, preferences, and generating a personalized itinerary.

Additionally, users can download their personalized itinerary as a PDF for easy reference.

## Features
- Collect travel details from users (destination, travel dates, budget, purpose).
- Collect user preferences (dietary preferences, activity level, accommodation type, special interests).
- Generate a detailed travel itinerary using the Mistral AI API.
- Option to download the generated itinerary as a PDF.

## Prerequisites
To run this project locally, you will need:
- Python 3.7+
- A Mistral API key

## Installation and Running the Application

### Step 1: Clone the Repository
Clone the project repository to your local machine using the following command:

bash
git clone https://github.com/yourusername/travel-planner.git


### Step 2: Install Required Dependencies
Navigate to the project folder and install the required Python libraries:

bash
cd travel-planner
pip install -r requirements.txt


The requirements.txt should include:
txt
streamlit==1.20.0
fpdf==1.7.2
requests==2.28.2


### Step 3: Set up Mistral API Key
Ensure that you have an API key from Mistral AI. Set your API key as an environment variable:

- *On Windows:*
  bash
  set MISTRAL_API_KEY=your-api-key-here
  

- *On macOS/Linux:*
  bash
  export MISTRAL_API_KEY=your-api-key-here
  

### Step 4: Run the Application
Once the dependencies are installed and the environment variable is set, you can run the app using:

bash
streamlit run app.py


The application will launch in your default web browser.

## How to Use

### Step 1: Collect Basic Travel Information
When you first open the app, you'll be prompted to provide basic information about your trip. This includes:
- *Destination*: Enter the city, country, or region where you'd like to travel.
- *Travel Dates*: Select your travel start and end dates.
- *Budget*: Choose your budget level from the options (Budget, Moderate, Luxury).
- *Purpose*: Select the purpose of your trip (e.g., Sightseeing, Adventure, Relaxation, etc.).

Once you have entered this information, click *Continue to Preferences* to proceed to the next step.

### Step 2: Collect Travel Preferences
Next, the app will ask for more detailed preferences to tailor your itinerary:
- *Dietary Preferences*: Select any dietary restrictions or preferences (e.g., Vegetarian, Vegan, Halal, Gluten-free, or None).
- *Activity Level*: Choose your preferred activity level (e.g., Very Light, Light, Moderate, Active, Very Active).
- *Accommodation Preferences*: Choose your accommodation type (e.g., Hotel, Hostel, Resort, Apartment, Boutique Hotel).
- *Special Interests*: Select any special interests or activities you would like to pursue (e.g., History, Art, Nature, Photography, Hiking, etc.).

Once all preferences are filled in, click *Generate Itinerary* to generate your personalized itinerary.

### Step 3: Generate Itinerary with Mistral AI
After you have filled in your preferences, the app will use the Mistral AI API to generate a detailed travel itinerary. This itinerary will provide day-by-day activity suggestions, places to visit, and other recommendations based on your input.

Once the itinerary is generated, you will see it displayed on the screen. You also have the option to download the itinerary as a *PDF* by clicking the *Download Itinerary PDF* button.

## Example Screenshot

![Travel Planner App](![Image](https://github.com/user-attachments/assets/c8c2ea2d-4304-4738-bace-d86d2310a07b))

## Deployed Application
You can try the app live here: [Personalized AI Travel Planner](https://personalized-ai-travel-planner.streamlit.app/)

## Troubleshooting
- *API Key Issues*: If you encounter errors related to the Mistral API, ensure that your API key is correctly set as an environment variable.
- *Package Installation Errors*: Ensure that you are using a virtual environment and that all dependencies are installed correctly.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- This project uses the [Mistral AI](https://mistral.ai) API to generate travel itineraries based on user input.
- The app is built using [Streamlit](https://streamlit.io) for easy deployment of web apps.
