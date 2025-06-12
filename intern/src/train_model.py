from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle

# Sample training
data = pd.read_csv("data/training_dataset.csv")  # must contain 'AnswerText' and 'Marks'
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['AnswerText'])
y = data['Marks']

model = LinearRegression()
model.fit(X, y)

with open("src/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("src/ml_model.pkl", "wb") as f:
    pickle.dump(model, f)
