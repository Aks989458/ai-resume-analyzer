import joblib
import re 

MODEL_PATH = "models/role_classifier.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"\s+"," ",text)
    text = re.sub(r"[^a-z0-9\s\+\#\.]"," ",text)
    return text.strip()

class MLRoleClassifier:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.vectorizer = joblib.load(VECTORIZER_PATH)

    def predict(self, resume_text):
        resume_text = clean_text(resume_text)

        X = self.vectorizer.transform([resume_text])

        predicted = self.model.predict(X)[0]

        probabilities = self.model.predict_proba(X)[0]
        classes = self.model.classes_

        top = sorted(
            zip(classes, probabilities),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        top_roles = [
            {"role": role, "confidence": round(float(prob) * 100, 2)}
            for role, prob in top
        ]

        return {
            "predicted_role": predicted,
            "top_roles": top_roles
        }