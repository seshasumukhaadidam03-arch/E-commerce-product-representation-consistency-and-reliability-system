import os
import urllib.request
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Add parent directory to path to import feature_extractor
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper.feature_extractor import PhishingFeatureExtractor

def download_dataset():
    """
    Downloads a baseline phishing/benign URL dataset.
    We will use a public dataset from GitHub containing raw URLs and labels.
    """
    url = "https://raw.githubusercontent.com/gangeshbaskerr/Phishing-Website-Detection/master/5.urldata.csv"
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    csv_path = os.path.join(data_dir, "urldata.csv")
    if not os.path.exists(csv_path):
        print(f"Downloading dataset from {url}...")
        urllib.request.urlretrieve(url, csv_path)
        print("Download complete.")
    else:
        print("Dataset already downloaded.")
    return csv_path

def build_feature_dataset(csv_path, num_samples=300):
    """
    Reads the raw URL dataset, samples a balanced set of URLs, and extracts features.
    We sample a smaller subset (e.g., 300) to keep the extraction time quick for the initial setup.
    """
    print(f"Loading raw URL dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # The dataset has columns: 'url' and 'label' (where 1 is phishing, 0 is benign)
    # Let's verify the columns
    if 'url' not in df.columns or 'label' not in df.columns:
        # Fallback/rename if columns are named differently
        df.columns = ['url', 'label']
        
    print(f"Total dataset shape: {df.shape}")
    print(f"Label distribution:\n{df['label'].value_counts()}")
    
    # Sample balanced dataset
    phishing_df = df[df['label'] == 1].sample(n=num_samples // 2, random_state=42)
    benign_df = df[df['label'] == 0].sample(n=num_samples // 2, random_state=42)
    sampled_df = pd.concat([phishing_df, benign_df]).reset_index(drop=True)
    
    extractor = PhishingFeatureExtractor(timeout=1.0) # Short timeout for speed
    
    feature_list = []
    labels = []
    
    print(f"Extracting features from {num_samples} URLs. This may take a minute...")
    for idx, row in sampled_df.iterrows():
        url = row['url']
        label = row['label']
        if idx % 50 == 0:
            print(f"Processed {idx}/{num_samples} URLs...")
            
        try:
            # For faster training dataset generation, we can choose to extract URL lexical & SSL features only,
            # or extract DOM features. Here, we extract all, but the short timeout will handle dead links.
            feats = extractor.extract_all(url)
            feature_list.append(feats)
            labels.append(label)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            
    features_df = pd.DataFrame(feature_list)
    features_df['label'] = labels
    
    # Save processed features to CSV for inspection/reuse
    processed_path = os.path.join(os.path.dirname(csv_path), "processed_features.csv")
    features_df.to_csv(processed_path, index=False)
    print(f"Features saved to {processed_path}")
    
    return features_df

def train_and_save():
    csv_path = download_dataset()
    
    # Extract features (adjust num_samples to scale the training set size)
    features_df = build_feature_dataset(csv_path, num_samples=400)
    
    # Prepare training data
    X = features_df.drop(columns=['label'])
    y = features_df['label']
    
    # Handle any NaN values by filling with -1 (common fallback in our extractor)
    X = X.fillna(-1)
    
    feature_cols = list(X.columns)
    print(f"Features list: {feature_cols}")
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model and feature columns
    model_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(model_dir, "phishing_model.pkl")
    
    save_data = {
        'model': model,
        'feature_cols': feature_cols
    }
    
    joblib.dump(save_data, model_path)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train_and_save()
