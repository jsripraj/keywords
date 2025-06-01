# Keyword Analyzer

## Purpose
This application is designed to help people who are determining keywords and topics to study. I thought it might be useful for prospective students who are choosing a school and/or topics of study. The widgets in my application can provide some interesting information that these prospective students can use to guide their decisions. 

## Demo 
https://mediaspace.illinois.edu/media/t/1_0mie6m3h

## Installation
Clone the repository, then use ```pip install -r requirements.txt``` to install the necessary packages. Ensure the given datasets are available in Neo4j and MySQL. Then run ```python3 app.py``` and go to https://127.0.0.1:8050/ to view the UI.

## Usage
First, search for and select a keyword in the first dropdown menu under the title. This keyword will be used in several of the widgets. Some of the widgets have their own inputs that modify their output along with the selected keyword.

## Design
The layout of the app is contained in app.py. In files ending with widget.py, I put the callbacks that handle user input. These callbacks generally call functions in the files ending with utils.py, which connect to their respective databases, execute queries, and process query results.

## Implementation
I used Dash, and the MySQL Python Connector and the Neo4j Python driver to connect to the databases. For Dash, I mostly used Dash Core and HTML Components. I also used Dash Cytoscape to show a network of nodes and edges.

## Database Techniques
I did not use any of the database techniques for credit :(

## Extra-Credit Capabilities
None

## Contributions
I worked alone, and I spent maybe 30-40 hours on this before I ran out of time.
