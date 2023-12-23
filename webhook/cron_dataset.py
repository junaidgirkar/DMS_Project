import requests

def download_dataset(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print("Dataset downloaded successfully.")
    else:
        print("Failed to download dataset.")

if __name__ == "__main__":
    dataset_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1703281431"
    file_path = "/home/junaidgirkar/DMS_Project/webhook/data/zillow_data.csv"
    download_dataset(dataset_url, file_path)
