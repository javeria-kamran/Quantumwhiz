from urllib import response
import streamlit as st
import pint 
import google.generativeai as genai
from dotenv import load_dotenv
import os

api_key = st.secrets["GEMINI"]["AIzaSyDwFPHkcbmGO7ynM4DSnrBmnCU-VqzSrpk"]
genai.configure(api_key=api_key)
ureg = pint.UnitRegistry()
def convert_units(value, from_unit, to_unit):
    try:
        if from_unit in ["celsius", "fahrenheit", "kelvin"] or to_unit in ["celsius", "fahrenheit", "kelvin"]:
            # Handle temperature conversions separately
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                result = value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                result = value - 273.15
            elif from_unit == "fahrenheit" and to_unit == "kelvin":
                result = (value - 32) * 5/9 + 273.15
            elif from_unit == "kelvin" and to_unit == "fahrenheit":
                result = (value - 273.15) * 9/5 + 32
            else:
                return "Invalid temperature conversion"
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        else:
            result = (value * ureg(from_unit)).to(to_unit)
            return f"{value} {from_unit} = {result}"
    except pint.DimensionalityError:
        return "Invalid conversion"
def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if response else "Error fetching data"
st.set_page_config(page_title="Unit Converter & AI Assistant", layout="wide")
st.sidebar.title("About This Project")
st.sidebar.markdown(
    """
    **Ultimate Unit Converter & AI Assistant**
    
    - Effortlessly convert between various unit categories like Length, Mass, Temperature, Volume, Speed, and Energy.
    - Supports intuitive unit conversion with real-time calculations.
    - Ask AI-powered questions for additional insights and guidance.
    - Powered by **Google Gemini AI** for intelligent responses.
    - Built using **Streamlit** for a sleek and interactive user experience.
    """
)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #008B8B !important;
        color: white !important;
        font-size: 16px !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: background-color 0.3s ease, transform 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #005F5F !important;
        transform: scale(1.05) !important;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border: 2px solid #008B8B !important;
        border-radius: 10px !important;
        padding: 10px !important;
        transition: border-color 0.3s ease !important;
        height: 50px !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #005F5F !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("The Unit Alchemist")
st.markdown("Effortless, Precision-Driven Unit Conversion Powered by Cutting-Edge Technology.")
unit_categories = {
    "Length": ["meter", "foot", "inch", "mile", "kilometer", "light_year"],
    "Mass": ["kilogram", "gram", "pound", "ounce", "ton"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Volume": ["liter", "gallon", "cubic_meter", "cubic_inch"],
    "Speed": ["meter_per_second", "kilometer_per_hour", "mile_per_hour"],
    "Energy": ["joule", "calorie", "electron_volt"],
}
st.subheader("Enter Your Conversion")

col1, col2, col3 = st.columns(3)

with col1:
    value = st.number_input("Enter value:", value=1.0, step=0.1)

with col2:
    category = st.selectbox("Select unit category:", list(unit_categories.keys()))

with col3:
    from_unit = st.selectbox("Select from unit:", unit_categories[category])

target_unit = st.selectbox("Select target unit:", unit_categories[category])

if st.button("Convert"):
    with st.spinner("Converting..."):
        result = convert_units(value, from_unit, target_unit)
        if "Invalid" not in result:
            st.success(f"✅ {result}")
        else:
            st.error("❌ Invalid conversion. Please check your units.")
st.subheader("💬 Ask AI (Powered By Gemini)")
user_query = st.text_area("Enter Your Question:")

if st.button("Generate"):
    if user_query:
        ai_response = ask_gemini(user_query)
        st.info(f"To the best of my knowledge: {ai_response}")
    else:
        st.warning("⚠️ Please enter a question.")

st.markdown("---")
st.markdown("🚀 Powered by **Google Gemini AI & Streamlit**")
