# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# We'll install NumPy and Pandas separately with specific versions
RUN pip install --no-cache-dir numpy==1.23.5 pandas==1.5.3
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable for FRED API key
ENV FRED_API_KEY=your_api_key_here

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]