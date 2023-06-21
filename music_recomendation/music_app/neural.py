import json
import numpy as np
import tensorflow as tf
from pathlib import Path

PARAMETERS = (
    "tempo",
    "valence",
    "loudness",
    "energy",
    "danceability",
    "speechiness",
    "time_signature",
    "mode",
    "key",
    "instrumentalness",
    "popularity",
)


DIFFRENCE_LIMIT = (5, 0.1, 1, 0.1, 0, 0.1, 0.05, 0, 0, 0.01, 1)


# pobiera dane z pliku json
def neural() -> None:
    file_path = Path("music_recomendation/datas/results/result2.json")
    with file_path.open(mode="r") as f:
        data = json.load(f)

    # wczytuje siec neuronowa
    model = tf.keras.models.load_model(
        "music_recomendation/neural_network/neural_network.h5"
    )
    # dane wejsciowe
    x = np.array([[data[key] for key in PARAMETERS] for _ in range(len(data))])
    # dane wyjsciowe maja byc zblizone do wejsciowych
    y = x.copy()

    # minimalna i maksymalna roznica wartosci
    min_vals = np.array(
        [
            [data[key] - offset for key, offset in zip(PARAMETERS, DIFFRENCE_LIMIT)]
            for _ in range(len(data))
        ]
    )

    max_vals = np.array(
        [
            [data[key] + offset for key, offset in zip(PARAMETERS, DIFFRENCE_LIMIT)]
            for _ in range(len(data))
        ]
    )

    # normalizacja danych
    a = 0
    b = 1
    min_vals += 0.001
    max_vals -= 0.001
    x_norm = ((x - min_vals) / (max_vals - min_vals)) * (b - a) + a

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

    model.fit(x_norm, y, epochs=120, batch_size=16)

    # nadpisanie modelu po kolejnej przetworzonej piosence dzieki
    # temu uczy sie z kazdym uzyciem
    model.save("music_recomendation/neural_network/neural_network.h5")

    # wyciagniecie i zapisanie nowych danych piosenki
    results = []
    for _ in range(len(x)):
        prediction = model.predict(x_norm[_].reshape(1, 11))
        results.append(prediction.tolist()[0])

    results_dict = {
        key: round(np.mean([r[i] for r in results]), None if i > 5 else 3)
        for i, key in enumerate(PARAMETERS)
    }

    file_path = Path("music_recomendation/datas/results/result3.json")
    with file_path.open(mode="w") as f:
        json.dump(results_dict, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    neural()
