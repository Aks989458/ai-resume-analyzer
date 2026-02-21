import pandas as pd
import re 
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report


DATA_PATH = "data/resume_dataset.csv"
MODEL_PATH = "models/role_classifier.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"\s+"," ",text)
    text = re.sub(r"[^a-z0-9\s\+\#\.]"," ",text)
    return text.strip()

def main():
    print("Loading Dataset ...")
    df = pd.read_csv(DATA_PATH)

    df = df.dropna(subset=["Category","Resume"])
    df["Resume"] = df["Resume"].apply(clean_text)

    X = df["Resume"]
    y = df["Category"]

    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

    print("Creating TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=30000,
        ngram_range=(1,2)
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Logistic Regression Model...")
    model = LogisticRegression(max_iter=2000)
    model.fit(X_train_vec,y_train)

    predictions = model.predict(X_test_vec)

    print("\nAccuracy:",accuracy_score(y_test,predictions))
    print("\nClassification Report:\n")
    print(classification_report(y_test,predictions))

    joblib.dump(model,MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("\nModel saved successfully!")


if __name__ == "__main__":
    main()