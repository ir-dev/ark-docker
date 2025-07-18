# ark-plotly-docker

-----

# `immanuelraj/ark-plotly-app:latest` - Plotly Reporting Microservice

This repository contains the necessary files to build and publish a Docker image that serves as a microservice for generating Plotly-based gauge and other interactive reports. This service is designed to be easily consumed by developers through its Dockerized deployment.

## Table of Contents

  - [Features](https://www.google.com/search?q=%23features)
  - [Getting Started](https://www.google.com/search?q=%23getting-started)
      - [Prerequisites](https://www.google.com/search?q=%23prerequisites)
      - [Running the Docker Image](https://www.google.com/search?q=%23running-the-docker-image)
  - [Usage](https://www.google.com/search?q=%23usage)
      - [API Endpoints](https://www.google.com/search?q=%23api-endpoints)
      - [Example Usage (Python)](https://www.google.com/search?q=%23example-usage-python)
  - [Building the Docker Image (Optional)](https://www.google.com/search?q=%23building-the-docker-image-optional)
  - [Contributing](https://www.google.com/search?q=%23contributing)
  - [License](https://www.google.com/search?q=%23license)

-----

## Features

  * **Plotly Integration:** Leverages the powerful Plotly library for creating dynamic and interactive visualizations, including gauges, bar charts, line charts, and more.
  * **Dockerized Deployment:** Packaged as a Docker image for easy distribution, consistent environments, and seamless integration into existing workflows.
  * **Microservice Architecture:** Designed to be a standalone service, accessible via API calls, allowing for decoupled development and deployment.
  * **Image Generation:** Generates images (e.g., PNG, JPEG, SVG) of the Plotly reports, making them suitable for embedding in other applications or documents.
  * **Docker Hub Publication:** Publicly available on Docker Hub as `immanuelraj/ark-plotly-app:latest`.

-----

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You'll need **Docker** installed on your system.

  * [Install Docker](https://docs.docker.com/get-docker/)

### Running the Docker Image

The easiest way to get started is by pulling and running the pre-built Docker image from Docker Hub:

```bash
docker pull immanuelraj/ark-plotly-app:latest
docker run -p 8000:8000 immanuelraj/ark-plotly-app:latest
```

This command will:

1.  **Pull** the `immanuelraj/ark-plotly-app:latest` image from Docker Hub.
2.  **Run** the container, mapping port `8000` on your host to port `8000` inside the container.

Once running, the service will be accessible at `http://localhost:8000`.

-----

## Usage

The Plotly reporting microservice exposes an API endpoint for generating reports.

### API Endpoints

The primary endpoint for generating a gauge report is:

  * **`POST /generate_gauge`**
      * **Description:** Generates a Plotly gauge chart based on the provided data and returns it as an image.
      * **Request Body (JSON):**
        ```json
        {
            "value": 75,
            "title": "Sales Performance",
            "ranges": [
                {"range": [0, 50], "color": "lightgray"},
                {"range": [50, 75], "color": "gray"},
                {"range": [75, 100], "color": "darkgray"}
            ],
            "suffix": "%"
        }
        ```
          * `value` (required, int/float): The current value for the gauge.
          * `title` (optional, string): The title of the gauge.
          * `ranges` (optional, list of dict): A list of dictionaries defining the gauge's color ranges. Each dictionary should have `"range": [start, end]` and `"color": "color_name_or_hex"`.
          * `suffix` (optional, string): A suffix to display after the gauge value (e.g., "%", "units").
      * **Response:** An image file (e.g., PNG) of the generated gauge chart.

### Example Usage (Python)

Here's an example of how to interact with the service using Python's `requests` library:

```python
import requests

PLOTLY_SERVICE_URL = "http://localhost:8000" # Or the IP address where your Docker container is running

def generate_gauge_report(value, title=None, ranges=None, suffix=None):
    """
    Calls the Plotly service to generate a gauge report and saves it as an image.
    """
    payload = {
        "value": value
    }
    if title:
        payload["title"] = title
    if ranges:
        payload["ranges"] = ranges
    if suffix:
        payload["suffix"] = suffix

    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{PLOTLY_SERVICE_URL}/generate_gauge", json=payload, headers=headers)

    if response.status_code == 200:
        with open("gauge_report.png", "wb") as f:
            f.write(response.content)
        print("Gauge report generated successfully: gauge_report.png")
    else:
        print(f"Error generating gauge report: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Example 1: Basic gauge
    generate_gauge_report(
        value=65,
        title="Project Completion",
        suffix="%"
    )

    # Example 2: Gauge with custom ranges
    custom_ranges = [
        {"range": [0, 30], "color": "red"},
        {"range": [30, 70], "color": "orange"},
        {"range": [70, 100], "color": "green"}
    ]
    generate_gauge_report(
        value=88,
        title="Customer Satisfaction",
        ranges=custom_ranges,
        suffix="%"
    )
```

-----

## Building the Docker Image (Optional)

If you wish to modify the application or build the Docker image yourself, follow these steps:

1.  **Clone this repository:**

    ```bash
    git clone https://github.com/immanuelraj/ark-plotly-app.git # Replace with your actual repo URL if different
    cd ark-plotly-app
    ```

2.  **Build the Docker image:**

    ```bash
    docker build -t immanuelraj/ark-plotly-app:latest .
    ```

    This command will build a Docker image named `immanuelraj/ark-plotly-app` with the tag `latest` from the `Dockerfile` in the current directory.

3.  **Run the newly built image:**

    ```bash
    docker run -p 8000:8000 immanuelraj/ark-plotly-app:latest
    ```

-----

## Contributing

Contributions are welcome\! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

-----

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
