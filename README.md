# real-estate-price-prediction
real-estate-price-prediction


# Real Estate Price Prediction - End-to-End ML Project

## 🌟 Project Overview

This project aims to build a **production-grade, scalable, and real-time real estate price prediction system**. It leverages data scraped from MagicBricks, stores it in MySQL, and uses Machine Learning for price forecasting, deployed via FastAPI and tracked with MLflow.

---

## 📊 Project Pipeline

### 1. **Web Scraping**

* Source: [MagicBricks](https://www.magicbricks.com/)
* Scraped both HTML and embedded JSON data for properties
* Stored raw HTML and JSON files:

  * `data/raw/extracted_html/`
  * `data/raw/extracted_json/`
* Technologies: `Selenium`, `BeautifulSoup`

### 2. **Data Parsing**

* Parsed relevant fields from HTML (e.g., price, area, furnishing, transaction type, possession date, society name)
* Parsed JSON fields as bonus (optional for now)
* Saved structured data into CSV:

  * Output: `data/processed/html_data.csv`

### 3. **Database Integration**

* Used **MySQL** (future-ready for PostgreSQL)
* Loaded parsed data from CSV to MySQL
* `.env` file contains DB credentials (placed in project root directory)

### 4. **Data Cleaning & Feature Engineering** *(Next Step)*

* Handle missing/nulls
* Convert text to numeric (e.g., price, area)
* Create derived fields:

  * `price_per_sqft`
  * `bhk_count`
  * `is_under_construction`, `is_furnished`, etc.
* Encode categorical variables (one-hot or label encoding)

### 5. **Exploratory Data Analysis (EDA)**

* Visualizations using PowerBI
* Identify trends, outliers, price patterns, and hot locations

### 6. **Machine Learning Pipeline**

* Algorithms: Linear Regression, XGBoost, Random Forest
* Evaluation: RMSE, MAE
* Pipeline: `sklearn.pipeline`, `StandardScaler`, `OneHotEncoder`
* Model saved with `joblib` or `MLflow`

### 7. **MLflow Integration**

* Log:

  * Parameters
  * Metrics
  * Models
* MLflow tracking UI for versioning and reproducibility

### 8. **Model Deployment with FastAPI**

* Pydantic-based schema for input/output
* Endpoints:

  * `/predict`
  * `/health`
  * `/retrain` *(optional)*
* Dockerized and production-ready

### 9. **CI/CD + Docker**

* GitHub Actions for:

  * Code linting
  * Unit testing
  * Build & push Docker image
* Deployed to:

  * DockerHub or AWS ECR

### 10. **Reporting with PowerBI**

* Connected to MySQL
* Built dashboards:

  * Price trends
  * Avg. BHK price
  * Top societies
  * Hot areas

---

## 🚀 Technology Stack

* **Scraping**: Selenium, BeautifulSoup
* **Data**: Pandas, MySQL
* **ML**: scikit-learn, XGBoost, MLflow
* **API**: FastAPI, Pydantic
* **DevOps**: Docker, GitHub Actions
* **Visualization**: PowerBI

---

## 📌 To-Do (Next Steps)

* [ ] Data Cleaning & Feature Engineering Script
* [ ] ML Model Training and Evaluation
* [ ] Integrate MLflow for experiment tracking
* [ ] FastAPI Deployment
* [ ] PowerBI Dashboard Design

---

## 🔐 Environment Variables (.env)

Create a `.env` file in the **project root**:

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=real_estate_db
DB_USER=root
DB_PASSWORD=yourpassword
```

---

## 🌟 Author

Built with ❤️ by Veera and Team for real-world deployment.

---

## 📅 Timeline

| Step                | Status        |
| ------------------- | ------------- |
| Scraping HTML/JSON  | ✅ Completed   |
| HTML Parsing to CSV | ✅ Completed   |
| MySQL Integration   | ✅ Completed   |
| Data Cleaning       | ⏳ In Progress |
| ML Pipeline         | ⏳ Pending     |
| Deployment          | ⏳ Pending     |




---

### ✅ **Objective: Scrape all MagicBricks property listings and save**

* **Full HTML page**
* **Embedded JSON data**

---

### 🔁 **Strategy**

MagicBricks uses **infinite scroll**, so we’ll use **Selenium** to:

* Scroll the page repeatedly until no new properties load.
* Extract each property’s container block.

Then for each property:

* **Save full HTML** of the listing.
* **Extract embedded JSON (`<script type="application/ld+json">`)** if available.
* Save JSON separately.

---

### 💡 Suggested Folder Structure

Under `src/scraping/`:

```
src/
 └── scraping/
     ├── scroll_magicbricks.py          ← handles scrolling and listing URL extraction
     ├── save_property_html.py          ← saves raw HTML of each listing
     ├── extract_json_from_html.py      ← parses and saves JSON
     ├── scrape_all_properties.py       ← orchestrator to run all steps
     └── utils/
         ├── file_utils.py              ← write_html(), write_json()
         ├── driver_setup.py            ← Selenium WebDriver setup
```

---

### 📁 Output Storage

```
artifacts/
 ├── raw_html/
 │    ├── property_001.html
 │    ├── ...
 └── json_data/
      ├── property_001.json
      ├── ...
```

---

### ⚙️ Tools & Tech Stack

* **Selenium** (for scroll and dynamic loading)
* **BeautifulSoup** (for HTML parsing)
* **`json` module** (for JSON parsing)
* **Logging** and **Exception Handling** as per your base setup

---

### 🔍 HTML vs JSON — What to Extract?

| Field Type         | Extract From |
| ------------------ | ------------ |
| Title              | HTML         |
| Price              | Both         |
| Location           | JSON         |
| Society            | HTML         |
| Size (sqft)        | HTML         |
| Bedrooms/Bathrooms | HTML         |
| Coordinates        | JSON         |
| Owner/Agent Name   | JSON         |

---
