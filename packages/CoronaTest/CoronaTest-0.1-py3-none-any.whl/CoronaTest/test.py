import pickle
from pathlib import Path
script_location = Path(__file__).absolute().parent
model_loc = script_location / "risk_analysis_model"
scaler_loc = script_location / "scaler"

with open(model_loc, 'rb') as p:
    classifier = pickle.load(p)
with open(scaler_loc, 'rb') as p:
    sc = pickle.load(p)

def get_prob(test_data):
    # Making the probability 
    x_test = [test_data]
    x_test = sc.transform(x_test)
    pobs = classifier.predict_proba(x_test)
    probs = pobs[:, 1]

    probs = probs * 100
    return probs