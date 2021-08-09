# eu-youthcard-gr
A tool to scrap the European Youth Card offers. The site itself
(europeanyouthcard.gr) is quite difficult to navigate and detect all the offers.
The goal is to scrap the offers from the original site and serve the data via an
a intuitive and user-friendly UI.

## Instructions

1. Make a Python virtual environment within the repo:
    ```
    $ virtualenv venv
    ```
2. Activate the virtual environment:
    ```
    $ source venv/bin/activate
    ```
2. Install required packages:
    ```
    $ python -m pip install -r requirements.txt
    ```
3. Execute the script:
    ```
    $ python scapper.py
    ```
