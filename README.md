# Containerized Web Scraper

## Description
This is a containerized web scraper that scrapes data from the Wikipedia page of the largest companies in the United States by revenue. The data is then cleaned and stored in a Pandas DataFrame.

## Build
To build the Docker image, run the following command in the terminal: docker build -t us-company-scraper .

## Usage
To run the script, run the following command in the terminal: docker run -t -i us-company-scraper
The script will provide you with a random company from the web-scraped list and ask you if you want to see another company. If you answer yes, the script will provide you with another company. If you answer no, the script will exit.