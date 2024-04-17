# AskPayChatbot

## Setup project locally
1. Download git repo `git@github.com:JessicaLiVndly/AskPayChatbot.git`
2. Create a virtual env and install requirements `pip install -r requirements.txt`
3. Get the slack data JSON file and place it under `slack_data` folder
4. Run script `python santize_data.py <filename>`
5. Run script `python create_chroma_db.py`

## How to Run this project
1. Run `chroma run --path ./chroma` which will run the chroma db server
2. Then the app can be run via the script `streamlit run app.py`