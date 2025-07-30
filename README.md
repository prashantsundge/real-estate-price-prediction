
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

## 🔐 Environment Variables (.env)

Create a `.env` file in the **project root**:

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=real_estate_db
DB_USER=root
DB_PASSWORD=yourpassword
```

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
---

## 🌟 Author

Built with ❤️ by Prashant Sundge for real-world deployment.

---

---

### 🎯 Real Estate Price Prediction Project – Interview Question Bank

---

## 🕸️ **1. Web Scraping (Selenium, BeautifulSoup, Requests)**

**Basic**

* What is the difference between `Selenium` and `BeautifulSoup`?
* When would you use Selenium over Requests + BS4?
* How did you handle dynamic content loading on MagicBricks?
* How do you deal with JavaScript-heavy pages during scraping?

**Intermediate**

* How did you extract embedded JSON from MagicBricks cards?
* How do you handle pagination in Selenium?
* What are browser options in headless Chrome and why did you use them?
* How do you manage delays and ensure elements are loaded before scraping?

---

---

### 🔹 Q1: What is the difference between `Selenium` and `BeautifulSoup`?

**Answer:**
`Selenium` is a browser automation tool that can interact with websites like a human—click buttons, scroll pages, wait for JavaScript to load. It’s ideal for **dynamic pages**.

`BeautifulSoup` is a parsing library used to **extract data from static HTML**. It cannot render JavaScript or simulate browser actions.

✅ In my real estate project:

* I used **Selenium** because MagicBricks loads content dynamically via JavaScript.
* After loading the page, I used `BeautifulSoup` to parse the HTML or extract embedded `<script>` JSON blocks efficiently.

---

### 🔹 Q2: When would you use Selenium over Requests + BS4?

**Answer:**
Use **Selenium** when:

* The site is **JavaScript-heavy**.
* Content appears only **after page interactions** (e.g., clicking, scrolling).
* You need to **simulate user actions**.

Use **Requests + BS4** when:

* The content is fully available in the **initial HTML**.
* You want a **faster and lighter** scraping approach.

✅ I initially tested MagicBricks with `requests` but found the property cards didn’t load without JS. So I switched to Selenium for full-page rendering.

---

### 🔹 Q3: How did you handle dynamic content loading on MagicBricks?

**Answer:**
MagicBricks renders listings dynamically using JavaScript after the page loads. Here's how I handled it:

1. **Headless Chrome via Selenium**: Loaded the entire page like a real browser.
2. **Explicit Waits (`WebDriverWait`)**: Ensured key elements (e.g., card containers) loaded before scraping.
3. **Scroll simulation**: For infinite scrolling pages, I used JavaScript execution:

   ```python
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
   ```
4. **Throttling Requests**: Added `time.sleep()` and randomized delays to mimic human interaction.

---

### 🔹 Q4: How do you deal with JavaScript-heavy pages during scraping?

**Answer:**
For JS-heavy pages, you need tools that can **render the DOM after JS execution**. Approaches include:

* **Selenium** (used in my project): Automates real browsers (Chrome/Firefox).
* **Playwright / Puppeteer**: Headless browser automation tools.
* **API Reverse Engineering**: Check browser network tab for data APIs (if available).

✅ On MagicBricks, there was **embedded JSON** inside `<script>` tags. After JS rendered the page, I used BeautifulSoup to extract and clean this JSON.

---

### 🔹 Q5: How do you extract embedded JSON from MagicBricks cards?

**Answer:**
After the full page loaded with Selenium:

1. Got the full page source:

   ```python
   page_html = driver.page_source
   ```
2. Parsed it with BeautifulSoup:

   ```python
   soup = BeautifulSoup(page_html, 'html.parser')
   ```
3. Located the `<script>` tag with embedded data:

   ```python
   script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
   json_data = json.loads(script_tag.string)
   ```
4. Navigated the JSON structure to extract structured property data:

   ```python
   properties = json_data['props']['pageProps']['listings']
   ```

---

### 🔹 Q6: How do you handle pagination in Selenium?

**Answer:**
There are 3 ways depending on site structure:

1. **URL pattern change** (e.g., `page=2`): Increment page number in the URL.
2. **Next button**: Find and click the “Next” button element.
3. **Infinite scroll**: Scroll until no new content loads.

✅ In my case:

* MagicBricks used **URL-based pagination**, so I looped over URLs with increasing page numbers.
* For robustness, I also checked if the card count changes after each scroll to prevent duplicate scraping.

---

### 🔹 Q7: What are browser options in headless Chrome and why did you use them?

**Answer:**
Browser options customize how Chrome runs. I used:

```python
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")  # Run without opening a window
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("user-agent=Custom UA")
```

✅ These options helped me:

* Run the scraper **silently in the background** (ideal for servers).
* **Avoid detection** by using custom user-agent.
* Improve **stability and performance**.

---

### 🔹 Q8: How do you manage delays and ensure elements are loaded before scraping?

**Answer:**
Key techniques:

* **Explicit Waits**: Wait for specific elements to be present:

  ```python
  WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "property-card"))
  )
  ```
* **Implicit Waits**: Applies a general delay for element searches.
* **Time-based sleep**: Last resort fallback:

  ```python
  time.sleep(2)
  ```

✅ I used `WebDriverWait` to wait until all property cards were loaded before parsing the DOM. This made scraping more stable.

---


---

## 💾 **2. Data Storage (Raw HTML + JSON + MySQL)**

* Why did you choose to store raw HTML and JSON separately?
* How do you parse and clean the JSON into a DataFrame?
* What challenges did you face while parsing real-estate data?
* How did you handle missing or inconsistent values in scraped data?
* How do you design a table schema for unstructured scraped data?

---

# ✅ **2. Data Storage – Web Scraping to MySQL (Real Estate Project)**

---

### 🔹 Q1: Why did you choose to store raw HTML and JSON separately?

**Answer:**
I chose to store both **raw HTML** and **embedded JSON separately** to keep the architecture clean and future-proof:

✅ **Raw HTML**:

* Acts as a **backup** in case the JSON structure changes or breaks in future.
* Useful for extracting new fields later without re-scraping the site.

✅ **Embedded JSON**:

* Much **easier to parse** and clean compared to scraping text from HTML.
* Contains structured data like price, BHK, carpet area, location, etc.

✅ I saved them in:

* `html_cards/`: `.html` files (raw full DOM)
* `json_cards/`: `.json` files per listing page/card

This **dual storage** made the pipeline **modular and robust**.

---

### 🔹 Q2: How do you parse and clean the JSON into a DataFrame?

**Answer:**
I used a **dedicated parsing script** (`parse_clean_cards.py`) with the following steps:

1. **Read JSON files** from `json_cards/` using `os.listdir()` and `json.load()`.

2. **Normalize nested fields** using `pandas.json_normalize()`:

   ```python
   df = pd.json_normalize(json_data['props']['pageProps']['listings'])
   ```

3. **Selected required columns**: price, BHK, area, location, etc.

4. **Cleaned the data**:

   * Removed symbols (`₹`, `sq.ft`)
   * Converted strings to numeric types
   * Parsed possession dates and availability
   * Extracted BHK and bathroom count from title if missing

5. **Concatenated** all parsed files into one clean DataFrame.

✅ Output:
A well-structured `pandas DataFrame` ready to be pushed into MySQL.

---

### 🔹 Q3: What challenges did you face while parsing real-estate data?

**Answer:**
✅ The main challenges were:

1. **Inconsistent field formats**

   * Area could be in sq.ft or sq.m.
   * Price values sometimes included “Negotiable”, “Cr”, or “Lakh”.

2. **Missing or null values**

   * Some properties didn’t include number of bathrooms or parking info.
   * Titles were inconsistent, so I had to use regex patterns to extract values.

3. **Nested and redundant JSON structure**

   * The embedded JSON had deep nesting and redundant fields.
   * Required flattening using `json_normalize` and key filtering.

4. **Data duplication**

   * Some listings appeared in multiple pages — needed to apply deduplication based on `property_id`.

---

### 🔹 Q4: How did you handle missing or inconsistent values in scraped data?

**Answer:**
✅ I took a **context-aware approach**:

* **Price/BHK/Area**:
  If missing, I excluded those records from modeling (since they're critical features).

* **Bathroom/Parking**:
  If missing, I filled with **median values** grouped by BHK or locality.

* **Possession Date**:
  Standardized different formats (e.g., “Immediate”, “By Dec 2025”) using custom regex + datetime parsing.

* **Outliers**:
  I filtered out absurd prices or area values using statistical thresholds (IQR, Z-score).

---

### 🔹 Q5: How do you design a table schema for unstructured scraped data?

**Answer:**
Though JSON is flexible, SQL requires a fixed schema. So I designed a **normalized SQL schema** like this:

```sql
CREATE TABLE properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    location VARCHAR(255),
    price INT,
    bhk INT,
    area_sqft FLOAT,
    bathroom INT,
    parking INT,
    possession_date DATE,
    furnishing_status VARCHAR(50),
    property_type VARCHAR(50),
    source_url TEXT
);
```

✅ Design choices:

* Selected only **relevant features** used in modeling.
* Used `INT`, `FLOAT`, and `DATE` to ensure proper types.
* Added `source_url` to trace back to original listing.

---


---


## 🧹 **3. Data Cleaning / Preprocessing (Pandas, Regex, EDA)**

**Basic**

* How did you handle inconsistent formats in price, area, BHK, etc.?
* What was your process to convert possession dates to structured format?

**Advanced**

* How did you impute or deal with missing bathroom or parking info?
* What EDA insights did you discover from the real estate dataset?
* Which features did you engineer for modeling?

---

# ✅ **3. Data Cleaning / Preprocessing – Real Estate Project**

---

## 🔹 **Basic Questions**

---

### Q1: How did you handle inconsistent formats in price, area, BHK, etc.?

**Answer:**
The dataset had several **unstructured string fields**, so I used a combination of **regex, string parsing, and unit conversion**:

#### ✅ BHK:

* Extracted numeric values from titles like `"3 BHK Apartment"`:

  ```python
  df['bhk'] = df['title'].str.extract(r'(\d+)\s*BHK').astype(float)
  ```

#### ✅ Area:

* Standardized all area values to **square feet**:

  * If unit was `sq. yd`, I converted it:
    `1 sq. yd = 9 sq. ft`
  * Removed extra text:

    ```python
    df['area_sqft'] = df['area'].str.extract(r'(\d+\.?\d*)').astype(float)
    ```

#### ✅ Price per sqft:

* Removed words like `"per sqft"` or `"only"` and kept only numeric:

  ```python
  df['price_per_sqft'] = df['price_per_sqft'].str.extract(r'(\d+)').astype(float)
  ```

✅ These steps ensured all numerical columns were **clean, typed, and uniform**.

---

### Q2: What was your process to convert possession dates to structured format?

**Answer:**
The `possession` column had values like:

* `"Ready to Move"`
* `"By Dec 2025"`
* `"Immediate Possession"`

Rather than parsing actual dates, I **categorized them into buckets**:

| Raw Text                 | Category |
| ------------------------ | -------- |
| `"Ready to move"`        | `old`    |
| `"By Dec 2025"`          | `future` |
| `"Immediate Possession"` | `old`    |
| `"By Mar 2024"`          | `new`    |

✅ Final Column: `possession_status` → `["old", "new", "future"]`

This simplified modeling and captured the **urgency factor** of possession.

---

## 🔹 **Advanced Questions**

---

### Q3: How did you impute or deal with missing bathroom or parking info?

**Answer:**

#### ✅ Bathroom:

* If missing, I imputed based on **median bathroom count per BHK**:

  ```python
  df['bathroom'] = df.groupby('bhk')['bathroom'].transform(lambda x: x.fillna(x.median()))
  ```

#### ✅ Parking:

* Parking details came as text like `"1 Covered + 1 Open"`.
* I used regex to extract into two columns:

  * `covered_parking`
  * `open_parking`

  ```python
  df['covered_parking'] = df['parking'].str.extract(r'(\d+)\s*Covered').fillna(0).astype(int)
  df['open_parking'] = df['parking'].str.extract(r'(\d+)\s*Open').fillna(0).astype(int)
  ```
* If parking info was missing entirely, filled both with 0.

✅ This allowed the model to **differentiate between parking types** and learn preferences.

---

### Q4: What EDA insights did you discover from the real estate dataset?

**Answer:**
I performed detailed EDA using `seaborn`, `pandas-profiling`, and visual tools.

#### Key Insights:

* **Location matters most** — properties in core areas had up to 2–3× price per sqft.
* **Price vs Area** — weak linearity beyond a certain threshold; hence considered `price_per_sqft`.
* **BHK Distribution** — 2 and 3 BHK were most common; 1 BHK often in metro areas.
* **Possession Trend** — `Ready to move` properties were priced slightly higher than `future` ones.
* **Bathroom and Parking Impact** — Properties with 2+ bathrooms and covered parking had better prices.

✅ These insights helped guide feature selection and model tuning.

---

### Q5: Which features did you engineer for modeling?

**Answer:**
I created several derived features to improve model performance:

| Feature Name         | Description                                               |
| -------------------- | --------------------------------------------------------- |
| `price_per_sqft`     | Price ÷ Area — better than raw price alone                |
| `bhk_area_ratio`     | Area ÷ BHK — captures property spaciousness               |
| `possession_status`  | Categorical feature from possession date                  |
| `covered_parking`    | From parsed parking text                                  |
| `open_parking`       | From parsed parking text                                  |
| `location_encoded`   | Encoded using frequency or target encoding                |
| `furnishing_encoded` | Ordinal mapping from `"Unfurnished"`, `"Semi"`, `"Fully"` |
| `is_ready_to_move`   | Boolean derived from `possession_status`                  |

✅ These features helped the model learn location trends, space quality, parking preference, and time-to-possession effects on pricing.

---

---

## 📈 **4. Modeling (Scikit-Learn, XGBoost, Stacking, Hyperparameter Tuning)**

**Basic**

* Which models did you try for price prediction and why?
* How did you evaluate your models?

**Intermediate**

* What is RMSE and why did you choose it?
* How did you perform feature selection?

**Advanced**

* How did you do model ensembling and what was the gain?
* Explain your hyperparameter tuning approach.
* How did you track model experiments?

---


# 🧠 **4. Modeling (scikit-learn, XGBoost, Evaluation, Ensembling)**

---

## 🔹 **Basic Questions**

---

### Q1: Which models did you try for price prediction and why?

**Answer:**

I experimented with a combination of **regression algorithms** suitable for tabular structured data:

| Model                 | Reason                                                                    |
| --------------------- | ------------------------------------------------------------------------- |
| **Linear Regression** | Baseline model to establish initial performance                           |
| **Ridge / Lasso**     | To reduce overfitting and handle multicollinearity                        |
| **Random Forest**     | Tree-based model that handles non-linear relationships well               |
| **XGBoost Regressor** | Powerful gradient boosting model that often performs best on tabular data |

**Why?**

* Real estate price prediction involves **non-linear patterns**, **categorical variables**, and **feature interactions**, so tree-based models like **Random Forest and XGBoost** were ideal.

---

### Q2: How did you evaluate your models?

**Answer:**

I used the following metrics for regression:

* **RMSE** (Root Mean Squared Error) – primary metric
* **R² score** – to understand variance explained

I did **cross-validation (CV)** to avoid overfitting to a single train-test split:

```python
from sklearn.model_selection import cross_val_score
np.sqrt(-cross_val_score(model, X, y, scoring='neg_root_mean_squared_error'))
```

Also visualized:

* **Actual vs Predicted Scatter Plots**
* **Residual distribution**

✅ These evaluations helped select the best generalizing model.

---

## 🔹 **Intermediate Questions**

---

### Q3: What is RMSE and why did you choose it?

**Answer:**

* **RMSE (Root Mean Squared Error)** is the square root of the average of squared prediction errors.
* Formula:

  $$
  \text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}
  $$

**Why RMSE?**

* RMSE penalizes **large errors more** than MAE (Mean Absolute Error).
* Real estate prices can vary widely, and **we want to minimize high-magnitude errors** that could lead to bad investment decisions.

✅ It aligns well with business needs: avoid big price mistakes.

---

### Q4: How did you perform feature selection?

**Answer:**

I used both **domain knowledge** and **automated techniques**:

#### Manual Feature Engineering:

* Created domain-relevant features like `price_per_sqft`, `bhk_area_ratio`, `is_ready_to_move`.

#### Automated Selection:

* **Correlation matrix** to drop redundant variables
* **Feature importance from Random Forest or XGBoost**
* **Recursive Feature Elimination (RFE)** for ranking top features
* **Lasso regression** to shrink irrelevant features

✅ Only features improving CV score and interpretability were retained.

---

## 🔹 **Advanced Questions**

---

### Q5: How did you do model ensembling and what was the gain?

**Answer:**

I used a **simple stacking ensemble**:

| Component Model       | Method Used            |
| --------------------- | ---------------------- |
| Linear Regression     | Level 0                |
| XGBoost               | Level 0                |
| Random Forest         | Level 0                |
| Ridge Regression      | Level 0                |
| **Linear Regression** | Meta Learner (Level 1) |

Technique:

```python
from sklearn.ensemble import StackingRegressor

stack_model = StackingRegressor(
    estimators=[('xgb', xgb_model), ('rf', rf_model)],
    final_estimator=LinearRegression()
)
```

**Result**:
✅ Gained **\~3–5% lower RMSE** vs. best single model
✅ Better generalization on unseen data

---

### Q6: Explain your hyperparameter tuning approach.

**Answer:**

I used **GridSearchCV** and **RandomizedSearchCV** for tuning:

* **RandomizedSearchCV** for wide exploration across many parameters
* **GridSearchCV** for fine-tuning around promising zones

For XGBoost, tuned:

```python
params = {
  "n_estimators": [100, 300, 500],
  "max_depth": [3, 5, 7],
  "learning_rate": [0.01, 0.05, 0.1],
  "subsample": [0.6, 0.8, 1.0],
  "colsample_bytree": [0.6, 0.8, 1.0]
}
```

Used **cross-validation RMSE** as scoring metric.

✅ This significantly improved model performance and reduced overfitting.

---

### Q7: How did you track model experiments?

**Answer:**

I used **MLflow** to manage experiments:

| Component          | Tool Used                                       |
| ------------------ | ----------------------------------------------- |
| Model Runs         | `mlflow.start_run()`                            |
| Metrics Tracked    | RMSE, R², training time                         |
| Parameters Tracked | `max_depth`, `n_estimators`, `alpha`, etc.      |
| Model Versioning   | Logged models with `mlflow.sklearn.log_model()` |

MLflow helped me:

* Compare models systematically
* Reproduce results
* Version the best performing models for deployment

✅ This gave me full control over the **ML lifecycle**, from training to deployment.

---


---

## ⚙️ **5. ML Pipeline (Modularization, Reproducibility, Pydantic)**

* How did you modularize your codebase (data\_loader, preprocess, predict)?
* What role does Pydantic play in your pipeline?
* How did you ensure data schema validation before predictions?

---

## 🧪 **6. Model Tracking (MLflow)**

* What is MLflow and how did you use it in your project?
* How did you track your experiments, parameters, and metrics?
* Can you explain the MLflow UI structure?

---


## ⚙️ **5. ML Pipeline (Modularization, Reproducibility, Pydantic)**

---

### Q1: How did you modularize your codebase (data\_loader, preprocess, predict)?

**Answer:**

I followed a **modular architecture**, separating the project into the following logical components for **clean code, reusability**, and **CI/CD readiness**:

| Module                | Responsibility                                                       |
| --------------------- | -------------------------------------------------------------------- |
| `data_loader.py`      | Loads cleaned data from MySQL using SQLAlchemy / Pandas              |
| `preprocess_input.py` | Handles input transformation for inference (e.g., encoding, scaling) |
| `predict_model.py`    | Loads trained model, processes request, returns prediction           |
| `train_model.py`      | Training logic, hyperparameter tuning, model saving                  |
| `schemas.py`          | Pydantic models for validating input/output schemas                  |
| `main.py` (FastAPI)   | API entry point; uses the above modules for prediction               |

✅ This structure ensured each file had a **single responsibility** and was easy to test, maintain, and deploy.

---

### Q2: What role does Pydantic play in your pipeline?

**Answer:**

Pydantic is used within **FastAPI** to:

1. **Validate request data** (e.g., property features input)
2. **Enforce type checking** at runtime
3. **Auto-generate API docs** using OpenAPI/Swagger
4. **Prevent bad inputs** from reaching the prediction model

Example:

```python
from pydantic import BaseModel

class PropertyInput(BaseModel):
    location: str
    bhk: int
    area_sqft: float
    possession_status: str
    covered_parking: int
    open_parking: int
```

✅ This made the API **robust**, **secure**, and **developer-friendly**.

---

### Q3: How did you ensure data schema validation before predictions?

**Answer:**

Using **Pydantic's schema definition** within the FastAPI request handler, I ensured:

* Any invalid or missing fields (like null BHK or wrong data types) triggered a 422 error before reaching the ML model
* I used constraints like:

  ```python
  from pydantic import Field
  bhk: int = Field(gt=0)
  area_sqft: float = Field(gt=100)
  ```
* This protected the ML model from garbage inputs and kept predictions reliable.

✅ Schema validation with Pydantic made the system **production-ready** and **fail-safe**.

---

## 🧪 **6. Model Tracking (MLflow)**

---

### Q1: What is MLflow and how did you use it in your project?

**Answer:**

MLflow is an **open-source platform** to manage the **end-to-end machine learning lifecycle**.

In my project, I used it for:

| Feature                   | Usage                                              |
| ------------------------- | -------------------------------------------------- |
| **Tracking**              | Log training runs, metrics, parameters, tags       |
| **Model Registry**        | Save versioned models (`mlflow.sklearn.log_model`) |
| **Experiment comparison** | Easily compare RMSE across different experiments   |

✅ This gave full **visibility, reproducibility**, and helped with **model versioning** during CI/CD.

---

### Q2: How did you track your experiments, parameters, and metrics?

**Answer:**

Using `mlflow` APIs inside `train_model.py`:

```python
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    mlflow.log_param("model_type", "XGBoost")
    mlflow.log_params(best_params)
    mlflow.log_metric("rmse", rmse_score)
    mlflow.sklearn.log_model(model, "real_estate_model")
```

✅ This allowed:

* Tracking multiple runs and parameters
* Keeping historical records for audit
* Reusing the best model in production

---

### Q3: Can you explain the MLflow UI structure?

**Answer:**

Yes. The MLflow UI has:

| Section            | Purpose                                                  |
| ------------------ | -------------------------------------------------------- |
| **Experiments**    | High-level grouping of runs (e.g., "Real Estate Models") |
| **Runs**           | Individual training jobs with unique ID                  |
| **Parameters**     | Hyperparameters like `max_depth`, `n_estimators`, etc.   |
| **Metrics**        | RMSE, R², training time                                  |
| **Artifacts**      | Model files, plots, pickles                              |
| **Model Registry** | Shows production-ready models and their versions         |

✅ Using this UI, I could **filter by RMSE**, **compare runs**, and **deploy the best version** confidently.

---
---

## ⚡ **7. Backend API (FastAPI + MySQL + Pydantic)**

**Basic**

* Why did you choose FastAPI over Flask or Django?
* How does FastAPI handle asynchronous requests?

**Intermediate**

* How did you connect FastAPI to your MySQL database?
* How do you handle input validation using Pydantic?

**Advanced**

* How did you integrate the trained ML model into FastAPI?
* How did you handle prediction requests in production?
* What are FastAPI dependencies and how did you use them?

---
Absolutely Prashant! Here's your full **interview-ready Q\&A** for:

---

# ⚡ **7. Backend API (FastAPI + MySQL + Pydantic)**
---

## **Basic**

---

### Q1: Why did you choose FastAPI over Flask or Django?

**Answer:**

I chose **FastAPI** because it offers:

| Feature                    | Reason                                                    |
| -------------------------- | --------------------------------------------------------- |
| 🚀 **High performance**    | Built on Starlette + Pydantic; async-ready and super fast |
| 🧠 **Auto validation**     | Built-in Pydantic models for request/response validation  |
| 📄 **Swagger UI / ReDoc**  | Automatic API documentation generation                    |
| 💡 **Minimal boilerplate** | Cleaner and more Pythonic compared to Django              |

✅ It gave me the **perfect balance** of **speed**, **developer productivity**, and **modern API design** needed for a **production ML API**.

---

### Q2: How does FastAPI handle asynchronous requests?

**Answer:**

FastAPI is built on **ASGI (Asynchronous Server Gateway Interface)**, allowing you to write non-blocking I/O code using Python’s `async`/`await`.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/predict")
async def predict():
    # This can be an async DB or model call
    return {"message": "Fast & Async"}
```

✅ This makes FastAPI **scalable under high load**, especially when handling **multiple user prediction requests concurrently**.

---

## **Intermediate**

---

### Q3: How did you connect FastAPI to your MySQL database?

**Answer:**

I used the **`SQLAlchemy` ORM** with `mysql-connector-python` to connect FastAPI to MySQL.

Steps:

1. **Setup DB URI** in a `.env` file:

```bash
MYSQL_URL = "mysql+mysqlconnector://user:pass@host:3306/db"
```

2. **Create SQLAlchemy session**:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

3. **Use dependency injection** to provide DB session:

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

✅ This made data ingestion and logging **safe, persistent, and scalable**.

---

### Q4: How do you handle input validation using Pydantic?

**Answer:**

FastAPI natively integrates **Pydantic** for type-safe input validation.

Example:

```python
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    location: str
    bhk: int = Field(gt=0)
    area_sqft: float = Field(gt=100)
```

✅ Invalid inputs like strings in numeric fields automatically return **422 errors** with clear messages — no manual checks required.

---

## **Advanced**

---

### Q5: How did you integrate the trained ML model into FastAPI?

**Answer:**

Steps I followed:

1. **Trained model** was saved using `joblib` or `mlflow.sklearn.log_model`
2. **Model loaded** in `predict_model.py` during API startup or lazy-load

```python
model = joblib.load("model.pkl")

@app.post("/predict")
def predict_price(input: PredictRequest):
    df = preprocess_input(input)
    prediction = model.predict(df)
    return {"predicted_price": prediction[0]}
```

✅ The ML model was treated as a **shared global object** for performance.

---

### Q6: How did you handle prediction requests in production?

**Answer:**

* Inputs came via **POST requests** with JSON
* Input validation via **Pydantic**
* Processing through **preprocess pipeline**
* Model prediction returned as JSON response
* Handled edge cases like:

  * Missing values
  * Incorrect datatypes
  * Unexpected locations

Deployed with **Docker + Gunicorn + Uvicorn**, which gave:

* Production reliability
* Auto-scaling
* Logging & error handling

---

### Q7: What are FastAPI dependencies and how did you use them?

**Answer:**

**Dependencies** in FastAPI are functions injected automatically into routes using `Depends()` — great for:

* Reusable logic (e.g., DB sessions, auth)
* Centralized error handling
* Cleaner code

Example: Injecting DB session

```python
from fastapi import Depends

@app.get("/records")
def read_records(db: Session = Depends(get_db)):
    return db.query(PropertyTable).all()
```

✅ Dependencies allowed **separation of concerns** and **easy unit testing**.

---


---
## 🌐 **8. Frontend UI (Streamlit)**

* Why did you use Streamlit for the frontend?
* How did you send inputs to the FastAPI backend from Streamlit?
* How did you display predicted results and EDA charts?

---

---

## 🐳 **9. Docker (FastAPI + Streamlit Images)**

* Why is Docker important in deployment?
* How did you create Dockerfiles for both backend and frontend?
* How did you push your images to Docker Hub?

---

## 🔁 **10. CI/CD (GitHub Actions)**

* What CI/CD strategy did you implement?
* How did you automate Docker image builds and pushes?
* What challenges did you face while automating secrets for Docker login?

---
Certainly Prashant — here's the **interview-ready, detailed + trust-building answer sheet** for:

## 🌐 **8. Frontend UI (Streamlit)**

## 🐳 **9. Docker (FastAPI + Streamlit Images)**

## 🔁 **10. CI/CD (GitHub Actions)**

---

## 🌐 **8. Frontend UI (Streamlit)**

### 🔹 Why did you use Streamlit for the frontend?

**Answer:**
I chose **Streamlit** because:

* It enables fast development of data-driven UIs with minimal boilerplate.
* Integrates natively with Python, which allowed me to reuse preprocessing and prediction functions.
* Has built-in support for plotting libraries like Matplotlib, Plotly, and Seaborn for EDA.
* It was perfect for an internal-facing or proof-of-concept tool where **quick iteration** was key.

---

### 🔹 How did you send inputs to the FastAPI backend from Streamlit?

**Answer:**
I built a **RESTful POST request** in Streamlit using Python’s `requests` library:

```python
import requests

payload = {
    "location": location,
    "area_sqft": area,
    "bhk": bhk,
    "bathrooms": bathrooms,
    "covered_parking": covered,
    "open_parking": open_,
    "status": possession_status
}

response = requests.post("http://fastapi-backend:8000/predict", json=payload)
prediction = response.json()["price_prediction"]
```

* **Streamlit** served as the frontend UI for users to input data.
* These inputs were validated client-side and sent to **FastAPI**, which performed inference using the trained model.

---

### 🔹 How did you display predicted results and EDA charts?

**Answer:**

* I used **Streamlit widgets** like `st.text_input`, `st.slider`, `st.selectbox` for input collection.
* Prediction results were shown using `st.success()` and formatted with currency symbols for clarity.
* For EDA:

  * Used `st.pyplot()` and `st.plotly_chart()` to show price distributions, area histograms, and correlation heatmaps.
  * Loaded the cleaned dataset dynamically to reflect up-to-date trends.

---

## 🐳 **9. Docker (FastAPI + Streamlit Images)**

### 🔹 Why is Docker important in deployment?

**Answer:**
Docker helps solve **“it works on my machine”** problems by ensuring consistent environments. It's important because:

* Creates **lightweight, reproducible containers** for both backend and frontend.
* Easy to deploy across any environment: local, staging, or cloud (AWS ECS, GCP Cloud Run, etc.).
* Encourages microservice separation: my FastAPI and Streamlit apps run in separate containers.
* Works seamlessly with **CI/CD pipelines**.

---

### 🔹 How did you create Dockerfiles for both backend and frontend?

**Answer:**

✅ **FastAPI Dockerfile:**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

✅ **Streamlit Dockerfile:**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

* Both had minimal base images to reduce size.
* Used separate ports: `8000` (FastAPI) and `8501` (Streamlit).

---

### 🔹 How did you push your images to Docker Hub?

**Answer:**

1. Logged in via terminal or GitHub Actions using:

   ```bash
   docker login -u <username> -p <token>
   ```

2. Tagged and pushed:

   ```bash
   docker build -t prashant/realestate-backend .
   docker push prashant/realestate-backend
   ```

3. Did the same for frontend.

In CI/CD, I automated this using **`docker/login-action`** and **`docker/build-push-action`** in `main.yml`.

---

## 🔁 **10. CI/CD (GitHub Actions)**

### 🔹 What CI/CD strategy did you implement?

**Answer:**
I implemented a **push-based CI/CD pipeline** using GitHub Actions. The goal was:

* On every push to `main` branch,
* Automatically **build Docker images** for backend and frontend,
* **Login to Docker Hub**, and
* **Push the latest images**.

This made deployment reproducible, hands-free, and production-grade.

---

### 🔹 How did you automate Docker image builds and pushes?

**Answer:**
Here’s a sample `main.yml` I used in `.github/workflows`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and Push Backend
      uses: docker/build-push-action@v3
      with:
        context: ./backend
        push: true
        tags: prashant/realestate-backend:latest

    - name: Build and Push Frontend
      uses: docker/build-push-action@v3
      with:
        context: ./frontend
        push: true
        tags: prashant/realestate-frontend:latest
```

---

### 🔹 What challenges did you face while automating secrets for Docker login?

**Answer:**
One key challenge was **Docker login failing** due to missing or misconfigured secrets. I solved this by:

* Creating Docker Hub secrets (`DOCKER_USERNAME`, `DOCKER_PASSWORD`) in GitHub → Settings → Secrets → Actions.
* Ensuring that these were passed securely to the `login-action`.
* Verified image pushes by checking [Docker Hub Repositories](https://hub.docker.com/).

I also added error logging and fallback logic to alert if image build fails.

---


---


## 🤖 **13. Real-World Project Questions**

* Walk me through your project from data collection to deployment.
* What was the biggest challenge you faced and how did you solve it?
* How would you scale this app if the data volume increases 10x?
* If you had to monetize or productize this, what would you do?

---

## 🤖 **13. Real-World Project Questions (Trust-Builder Answers)**

---

### 🔹 Walk me through your project from data collection to deployment.

**Answer:**
Sure. This was a full-cycle real estate price prediction project that I built to simulate a real-world production system. The workflow followed these stages:

1. **🕸 Web Scraping:**

   * I used **Selenium** to automate real-time scraping of MagicBricks listings.
   * Each card's full HTML and embedded JSON were extracted and saved in separate folders.

2. **💾 Raw Storage:**

   * Stored raw HTML + JSON separately to preserve full fidelity.
   * Saved structured property details into **MySQL**, ensuring it was ingestion-ready.

3. **🧹 Cleaning & Parsing:**

   * Cleaned inconsistencies like:

     * Area in sq. yards → sq. ft.
     * Prices like “6,000/sqft” → numeric only
     * Parsed BHK from listing titles (e.g., “2 BHK Builder Floor” → 2)
   * Created engineered features: possession status, structured parking columns, etc.

4. **📊 EDA & Preprocessing:**

   * Performed thorough EDA to understand regional trends, outliers, and distribution of price per sqft.
   * Standardized and imputed missing values using statistical and domain-aware logic.

5. **📈 Modeling:**

   * Trained multiple regressors: Linear, Decision Tree, XGBoost, and a voting ensemble.
   * Used RMSE as the main metric; tracked model experiments via **MLflow**.

6. **⚙️ Modular Pipeline:**

   * Codebase was modularized into:

     * `data_loader.py`, `preprocess_input.py`, `predict_model.py`
   * Schema validated with **Pydantic** for robustness.

7. **🚀 Deployment:**

   * Built a **FastAPI backend** to serve the model.
   * Integrated prediction API with a **Streamlit frontend**.
   * Dockerized both apps, pushed to **Docker Hub**, and wired up **CI/CD with GitHub Actions**.

---

### 🔹 What was the biggest challenge you faced and how did you solve it?

**Answer:**
The biggest challenge was **data inconsistency** in the scraped real estate listings. Since user-generated listings have varying formats, units, and missing values, the preprocessing layer had to be bulletproof.

For example:

* Area was in sq. yards, sq. ft., acres—so I built a converter that normalized all to sq. ft.
* Parking info came as free text like "1 Covered + 1 Open" — used regex to split into two numerical columns.
* Possession dates were like "Ready to Move" or "Possession by Dec 2025" — I bucketed them into `old`, `new`, and `future`.

I tackled this by building **custom transformation functions with unit tests**, and using **Pydantic schema checks** at every pipeline stage. This gave me confidence in data quality downstream.

---

### 🔹 How would you scale this app if the data volume increases 10x?

**Answer:**
Great question. Scalability can be addressed at multiple layers:

1. **Scraping Layer:**

   * Use **headless browser pools** or tools like **Scrapy + Splash** to scrape in parallel.
   * Rotate IPs with proxies or services like BrightData to avoid bans.

2. **Storage:**

   * Move from local MySQL to **RDS/Aurora** (for relational) or **MongoDB** (if data gets more semi-structured).
   * Archive raw HTML/JSON in **AWS S3** and only store structured data in MySQL.

3. **Model Inference:**

   * Deploy the model as a **REST API behind a load balancer**, using **FastAPI + Uvicorn + Gunicorn**.
   * Use **caching** (Redis) for repeated queries.
   * If needed, move to **async batch inference** for high-throughput scoring.

4. **Monitoring & Logging:**

   * Add logging via **Loguru** or **Sentry** and monitor latency, failure rates, input drift.

---

### 🔹 If you had to monetize or productize this, what would you do?

**Answer:**
This project has clear business potential, especially in real estate analytics. Here's how I would productize it:

1. **Product Direction:**

   * Build a **price intelligence dashboard** for homeowners, brokers, and investors.
   * Use prediction + actual market data to show **“Is this listing overpriced?”** insights.

2. **Monetization Models:**

   * **B2B SaaS** for brokerages: pay to get prediction APIs or analytics dashboards.
   * **Freemium Model**: limited free predictions, paid for full property reports or data exports.

3. **Tech Stack:**

   * Host on **AWS/GCP**, database in **PostgreSQL + S3**, model serving via **FastAPI + Docker**.
   * Use **PowerBI or Superset** for visualizations.
   * Offer access via API or Web portal.

4. **Compliance & Scale:**

   * Ensure scraped data usage complies with ToS.
   * Add user authentication, rate limiting, and access control.

This approach would make it both technically scalable and commercially viable.

---

---
