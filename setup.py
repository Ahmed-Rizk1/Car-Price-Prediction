from setuptools import setup, find_packages

setup(
    name="car_price_prediction",
    version="1.0.0",
    description="A modular machine learning project for car price prediction",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.37.1",
        "numpy>=1.26.4",
        "pandas>=2.2.2",
        "scikit-learn>=1.5.1",
        "pyyaml>=6.0",
    ],
)
