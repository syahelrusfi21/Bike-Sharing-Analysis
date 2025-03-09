# 🚴‍♂️ Bike Sharing System Dashboard
The Bike Sharing System is an innovative automatic bike rental service that allows users to rent a bike at one location and return it at another. This system plays an important role in addressing traffic, environmental, and health issues. The analysis is based on the Bike Sharing dataset uploaded by Lakshmipathi N on the Kaggle website.

Link to the dataset: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset

🔹 The objectives of this analysis are to determine:
- Are there seasonal patterns in bike rentals?
- What are the rental trends over time?
- What are the rental trends for casual users versus registered users? Are there differences?
- Do environmental conditions such as temperature, humidity, etc., influence bike rentals?

# 🚀 Setup Environment
🔹 Menggunakan Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```
🔹 Menggunakan Shell/Terminal
```
# Create a project folder
mkdir data_analysis_project
cd data_analysis_project

# Install a virtual environment with pipenv
pipenv install
pipenv shell

# Install dependencies
pip install -r requirements.txt
```
# 🏃 Running a Streamlit Application
```
streamlit run bike_sharing_dashboard.py
```
# 📂 Project Folder Structure
```
bike-sharing-analysis/
│── dashboard/
│   ├── bike_sharing_dashboard.py  # Main Streamlit app
│   ├── bike_(preprocessed)_data.csv   # Preprocessed dataset
│   ├── image1.png   # Visualization image
|   ├──    .
|   ├──    .
│── dataset/
│   ├── day.csv  # Raw dataset
│   ├── hour.csv  # Raw dataset
│── requirements.txt
│── README.md
```
# 🛠 Deployment
The application can also be accessed directly via Streamlit Cloud: 🔗 https://bike-sharing-analysis-f2rdhrsjagjtt8iuwpchgd.streamlit.app/
