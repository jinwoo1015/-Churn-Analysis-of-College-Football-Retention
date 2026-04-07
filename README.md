# 🏈 Predictive Roster Management: Transfer Portal Risk Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://jinwoo1015--churn-analysis-of-college-football-reten-app-i3o8uv.streamlit.app/)

**Live Demo:** [Click here to view the live dashboard](https://jinwoo1015--churn-analysis-of-college-football-reten-app-i3o8uv.streamlit.app/)

## 📌 Project Overview
In modern college football, roster retention is just as critical as recruiting. This project translates raw GPS/Catapult physical data into an actionable "flight risk" metric, helping coaching staffs proactively identify players who are statistically highly likely to enter the transfer portal. 

Rather than stopping at a Jupyter Notebook, this project includes a fully deployed interactive web application built with Streamlit, demonstrating an end-to-end machine learning lifecycle from data ingestion to stakeholder delivery.

## 🚀 Key Features
* **XGBoost Predictive Engine:** A machine learning model trained to identify non-linear relationships between physical exertion, geographical distance from home, and the likelihood of transferring.
* **Interactive Roster Dashboard:** A clean, automated UI that sorts the current roster from highest risk to lowest risk.
* **Actionable "Why" Metrics:** The dashboard isolates the specific driver of a player's risk score (e.g., highlighting if their `Avg_Player_Load_Per_Min` is dangerously high), allowing strength and conditioning staff to intervene immediately.
* **Handled Class Imbalance:** Utilized SMOTE (Synthetic Minority Over-sampling Technique) to ensure the model accurately detects the minority class (players who transfer) without bias.

## 🛠️ Tech Stack
* **Language:** Python
* **Machine Learning:** `xgboost`, `scikit-learn`, `imbalanced-learn`
* **Data Manipulation:** `pandas`, `numpy`
* **Frontend/Deployment:** `streamlit`

## 🧠 Model Architecture & Data
The core model is an XGBoost Classifier integrated into a Scikit-Learn Pipeline. 
* **Scaling:** `StandardScaler` applied to normalize varying units of measurement.
* **Imbalance Handling:** `SMOTE` applied to the training data to synthesize examples of the minority class (transfers), improving the model's recall.
* **Key Features:**
  * `Avg_Player_Load_Per_Min`: A measure of physical intensity during practice/games.
  * `Season_Max_Velocity`: The player's top speed recorded.
  * `homeLatitude`: Used as a geographical proxy for the player's distance from their hometown.

## 💻 How to Run Locally

If you would like to run this application on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
   ```
2.  **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
4. **View the app:**
Open your browser and navigate to http://localhost:8501

## 📁 Project Structure
├── app.py                 # The main Streamlit application script
├── transfer_model.pkl     # The serialized, pre-trained XGBoost pipeline
├── chunn_model_data_repo.csv  # The cleaned dataset used for dashboard population
├── catapult.csv  # Original dataset for the analysis and modeling
├── roster_data.csv  # Original dataset for the analysis and modeling
├── portal_data.csv  # Original dataset for the analysis and modeling
├── catapult.csv  # Original dataset for the analysis and modeling
├── model_training.qmd   # Jupyter notebook containing EDA, SMOTE, and model training
└── README.md              # Project documentation

## 📬 Contact
### Jinwoo Choi
* LinkedIn: [[LinkedIn link](https://www.linkedin.com/in/jinwoochoi1015/)]
* GitHub: [[GitHub link](https://github.com/jinwoo1015)]
