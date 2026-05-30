import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

data = pd.read_csv("training_data.csv")

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(
    data["Description"]
)

y = data["Category"]

model = MultinomialNB()

model.fit(X, y)


def predict_category(description):

    transformed = vectorizer.transform(
        [description]
    )

    prediction = model.predict(
        transformed
    )

    return prediction[0]