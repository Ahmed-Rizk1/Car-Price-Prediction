import streamlit as st
import pandas as pd
from src.config import config
from src.data.loader import load_dataset
from src.model.predictor import CarPricePredictor
from src.utils.logging import setup_logger

# Setup logging
logger = setup_logger("streamlit_app")

# Page config
st.set_page_config(
    page_title=config.get("app.name", "Car Price Prediction"),
    layout="centered",
    page_icon="🚗"
)

def main():
    try:
        # Title and subtitle
        st.title(f"🚗 {config.get('app.name', 'Car Price Prediction')}")
        st.markdown("Predict the **price of your car** based on its features! (Production Ready 🚀)")

        # Load Data
        df = load_dataset()
        
        # Load Model
        predictor = CarPricePredictor()

        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            location = st.selectbox("📍 Location", df["Location"].unique())
            year = st.slider("📅 Year", 1995, 2019, 2015)
            km = st.slider("🛣️ Kilometers Driven", 150, 300000, 50000)
            brand = st.selectbox("🏷️ Brand", df["Brand"].unique())
            # Filter models by brand
            df_brand = df[df["Brand"] == brand]
            model_name = st.selectbox("🚘 Model", df_brand["Model"].unique())

        with col2:
            # Filter further by model to get specific specs if needed, or just general lists
            # The original code filtered by model for the next options, which is good UX
            df_model = df[df["Model"] == model_name]
            
            # Fallback if filter result is empty (shouldn't happen with valid data)
            if df_model.empty:
                df_model = df_brand
            
            fuel = st.selectbox("⛽ Fuel Type", df_model["Fuel_Type"].unique())
            transmission = st.selectbox("⚙️ Transmission", df_model["Transmission"].unique())
            owner = st.selectbox("👤 Owner Type", df["Owner_Type"].unique())
            
            # numeric defaults
            min_mileage = float(df_model["Mileage"].min()) if not df_model.empty else 0.0
            
            mileage = st.slider("📏 Mileage (km/l)", min_mileage, 500.0, 25.0)
            engine = st.slider("🔧 Engine (CC)", 500, 6000, 1500)
            power = st.slider("💪 Power (bhp)", 50, 500, 100)

        # Collect Features
        features = pd.DataFrame({
            "Location": [location],
            "Year": [year],
            "Kilometers_Driven": [km],
            "Fuel_Type": [fuel],
            "Transmission": [transmission],
            "Owner_Type": [owner],
            "Mileage": [mileage],
            "Engine": [engine],
            "Power": [power],
            "Brand": [brand],
            "Model": [model_name]
        })

        # Predict button
        st.markdown("---")
        if st.button("🔮 Predict Price", type="primary"):
            with st.spinner("Calculating value..."):
                prediction = predictor.predict(features)
                st.success(f"💵 Predicted Price: **$ {prediction:,.2f}**")
                
                # Optional: Add some analytics or debug info if needed
                logger.info(f"User predicted price for {brand} {model_name}: {prediction}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"App error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
