import json
import numpy as np
import tensorflow as tf
from pathlib import Path

# pobiera dane z pliku json
file_path = Path("music_recomendation/datas/results/result2.json")
with file_path.open(mode="r") as f:
    data = json.load(f)

# wczytuje siec neuronowa
model = tf.keras.models.load_model(
    "music_recomendation/neural_network/neural_network.h5"
)
# dane wejsciowe
X = np.array(
    [
        [
            data["tempo"],
            data["valence"],
            data["loudness"],
            data["energy"],
            data["time_signature"],
            data["danceability"],
            data["speechiness"],
            data["mode"],
            data["key"],
            data["instrumentalness"],
            data["popularity"],
        ]
        for i in range(len(data))
    ]
)
# dane wyjsciowe maja byc zblizone do wejsciowych
Y = X.copy()

# minimalna i maksymalna roznica wartosci
min_vals = np.array(
    [
        [
            data["tempo"] - 5,
            data["valence"] - 0.1,
            data["loudness"] - 1,
            data["energy"] - 0.1,
            data["time_signature"],
            data["danceability"] - 0.1,
            data["speechiness"] - 0.05,
            data["mode"] - 0,
            data["key"] - 0,
            data["instrumentalness"] - 0.01,
            data["popularity"] - 1,
        ]
        for i in range(len(data))
    ]
)
max_vals = np.array(
    [
        [
            data["tempo"] + 5,
            data["valence"] + 0.1,
            data["loudness"] + 1,
            data["energy"] + 0.1,
            data["time_signature"],
            data["danceability"] + 0.1,
            data["speechiness"] + 0.05,
            data["mode"] + 0,
            data["key"] + 0,
            data["instrumentalness"] + 0.01,
            data["popularity"] + 1,
        ]
        for i in range(len(data))
    ]
)

# normalizacja danych
a = 0
b = 1
min_vals += 0.001
max_vals -= 0.001
X_norm = ((X - min_vals) / (max_vals - min_vals)) * (b - a) + a

# przetwarzanie danych i trening na nowych danych
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(256, activation="relu", input_shape=(11,)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(11, activation="linear"),
    ]
)

model.compile(optimizer="adam", loss="mean_squared_error")

model.fit(X_norm, Y, epochs=120, batch_size=16)

# nadpisanie modelu po kolejnej przetworzonej piosence dzieki
# temu uczy sie z kazdym uzyciem
model.save("music_recomendation/neural_network/neural_network.h5")

# wyciagniecie i zapisanie nowych danych piosenki
results = []
for i in range(len(X)):
    prediction = model.predict(X_norm[i].reshape(1, 11))
    results.append(prediction.tolist()[0])


results_dict = {
    "tempo": round(np.mean([result[0] for result in results]), 3),
    "valence": round(np.mean([result[1] for result in results]), 3),
    "loudness": round(np.mean([result[2] for result in results]), 3),
    "energy": round(np.mean([result[3] for result in results]), 3),
    "time_signature": int(round(np.mean([result[4] for result in results]), 0)),
    "danceability": int(round(np.mean([result[5] for result in results]), 0)),
    "speechiness": int(round(np.mean([result[6] for result in results]), 0)),
    "mode": int(round(np.mean([result[7] for result in results]), 0)),
    "key": int(round(np.mean([result[8] for result in results]), 0)),
    "instrumentalness": int(round(np.mean([result[9] for result in results]), 0)),
    "popularity": int(round(np.mean([result[10] for result in results]), 0)),
}

file_path = Path("music_recomendation/dataas/results/result3.json")
with file_path.open(mode="w") as f:
    json.dump(results_dict, f, indent=2, ensure_ascii=False)
