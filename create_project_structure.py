
import os 


#define folder structure 

folders = [

    "data/raw",
    "data/processed",
    "notebooks",
    "src/scraping",
    "src/sql",
    "src/ml_pipeline",
    "src/utils",
    "mlflow",
    ".github/workflows",
    "docker",
    "dashboards",


]
starter_files = [
    "README.md",
    "requirements.txt",
    ".gitignore",
    "app.py",
    ".github/workflows/ci-cd.yml"

]


def create_folders_and_files():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created Folder : {folder}")

    
    for file in starter_files:
        if not os.path.exists(file):
            with open(file , 'w') as f:
                f.write("")
            print(f"Created file : {file}")

if __name__ =="__main__":
    create_folders_and_files()