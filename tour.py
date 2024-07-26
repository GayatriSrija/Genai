import google.generativeai as genai
import json
import streamlit as st

def generate_tour(place, destination, days, budget):

    try:
        # Configure API key
        genai.configure(api_key="AIzaSyDi8q4yXoeMZGWlhQU3vFH3xE2K4KBjaXc")

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are a GenExplorer. Create an best and efficient  tour plans based on the user's needs, including place, destination, number of days, and budget.",
        )

        # Construct the prompt
        prompt = f"Create a tour plan for a trip from {place} to {destination} for {days} days with a budget of {budget} dollars. Include a detailed itinerary with activities, accommodation options and food recommendations."

        # Generate the tour plan
        response = model.generate_content(prompt)
        tour_plan_text = response.text

        # Basic tour plan formatting (you can enhance this)
        tour_plan_dict = {"itinerary": [], "accommodation": [], "food": []}
        current_section = "itinerary"
        for line in tour_plan_text.split("\n"):
            if line.startswith("Itinerary:"):
                current_section = "itinerary"
            elif line.startswith("Accommodation:"):
                current_section = "accommodation"
            elif line.startswith("Food:"):
                current_section = "food"
            else:
                tour_plan_dict[current_section].append(line)

        return tour_plan_dict

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Streamlit application
st.title("Tour Plan Generator")

place = st.text_input("Enter the starting place:")
destination = st.text_input("Enter the destination:")
days = st.number_input("Enter the number of days:", min_value=1, step=1)
budget = st.number_input("Enter the budget:", min_value=0.0, step=100.0)

if st.button("Generate Tour Plan"):
    if place and destination and days > 0 and budget >= 0:
        tour_plan = generate_tour_plan(place, destination, days, budget)
        if tour_plan:
            st.subheader("Itinerary")
            for item in tour_plan["itinerary"]:
                st.write(item)
                
            st.subheader("Accommodation")
            for item in tour_plan["accommodation"]:
                st.write(item)

            st.subheader("Food")
            for item in tour_plan["food"]:
                st.write(item)
        else:
            st.error("Failed to generate the tour plan.")
    else:
        st.error("Please provide valid inputs.")
