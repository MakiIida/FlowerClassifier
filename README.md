# FlowerClassifier

### Dataset
This project uses the [Flower Dataset](https://www.kaggle.com/datasets/abhayayare/flower-dataset) from Kaggle. The dataset is licensed under [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/), allowing for unrestricted use.

1. Siirry projektikansioon: cd ~/code/FlowerClassifier

2. Aktivoi virtuaaliympäristö: source .venv/Scripts/activate

3. Käynnistä projektin kontit Dockerilla: docker-compose -f docker-compose-flower.yml up --build

TAI: streamlit run app.py

4. Streamlit-sivusto osoitteessa: http://localhost:8501

5. Sammuta kontit: docker-compose -f docker-compose-flower.yml down