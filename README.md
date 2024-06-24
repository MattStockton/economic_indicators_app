# AI-Generated Economic Indicators and Stock Market Dashboard

**IMPORTANT NOTE**: This project, including all code, documentation, and this README.md file, was generated almost entirely by Claude 3.5 Sonnet, an AI language model. Only very minor manual tweaks were made to the code to ensure functionality. This project serves as an experiment to explore the capabilities of AI in software development, from conception to near-complete implementation.

## Project Overview

This application is a Streamlit-based dashboard that visualizes economic indicators alongside stock market data. It was created as an experiment to see if a fully functional application could be developed primarily using an AI language model, with minimal human intervention.

## AI-Generated Components with Minimal Manual Tweaks

- Python application code (app.py)
- Dockerfile
- requirements.txt
- This README.md

All components were initially generated based on prompts and interactions with Claude 3.5 Sonnet. Very minor manual tweaks were then made to ensure the code functioned as intended. The goal was to test the limits of AI-assisted software development and to showcase the current capabilities and limitations of large language models in creating functional applications with minimal human intervention.

## Features

- Display stock prices for any company in the S&P 500
- Show economic indicators from FRED (Federal Reserve Economic Data)
- Interactive charts combining stock prices and economic data
- Year-over-Year (YoY) change calculations for economic indicators
- Raw data display for both stock and economic data

## Prerequisites

- Python 3.9 or higher
- Docker (optional, for running in a container)
- FRED API key (obtainable from https://fred.stlouisfed.org/docs/api/api_key.html)

## Installation and Running Locally

### Option 1: Running directly with Python

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set your FRED API key as an environment variable:
   ```
   export FRED_API_KEY=your_api_key_here
   ```

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

5. Open your web browser and navigate to `http://localhost:8501`

### Option 2: Running with Docker

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Build the Docker image:
   ```
   docker build -t economic-dashboard .
   ```

3. Run the Docker container:
   ```
   docker run -p 8501:8501 -e FRED_API_KEY=your_api_key_here economic-dashboard
   ```

4. Open your web browser and navigate to `http://localhost:8501`

## Usage

1. Select any S&P 500 stock from the dropdown menu in the sidebar.
2. Check the economic indicators you want to display.
3. The main chart will show the selected company's stock price alongside the Year-over-Year changes of the selected economic indicators.
4. Individual charts for each selected economic indicator will be displayed below the main chart.
5. Raw data for both stock prices and economic indicators can be found at the bottom of the page.

## Note

Make sure to replace `your_api_key_here` with your actual FRED API key when running the application.

## Dependencies

- streamlit==1.22.0
- yfinance==0.2.18
- plotly==5.14.1
- fredapi==0.5.1
- numpy==1.23.5
- pandas==1.5.3
- requests==2.26.0
- beautifulsoup4==4.10.0

For the full list of dependencies, see the `requirements.txt` file.

## Contributing

As this project is primarily an AI-generation experiment, contributions should be focused on improving the AI-generation process or expanding the project's scope using AI assistance. Please feel free to submit a Pull Request with AI-generated improvements or extensions, noting any manual tweaks that were necessary.

## License

[Specify the license here, e.g., MIT, GPL, etc.]

## Disclaimer

This project is an experiment in AI-generated software development with minimal human intervention. While efforts have been made to ensure functionality and accuracy, including minor manual tweaks, the code and documentation may still contain errors or inefficiencies. Use this application with caution and verify its output independently for critical use cases.