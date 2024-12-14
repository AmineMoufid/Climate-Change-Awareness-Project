import kaggle
import os

def fetch_data():
    dataset_url = 'goyaladi/climate-insights-dataset'
    data_dir = 'data'
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    kaggle.api.dataset_download_files(dataset_url, path=data_dir, unzip=True)
    print(f"Dataset downloaded and stored in: {data_dir}")

if __name__ == "__main__":
    fetch_data()
