"""Lógica de recomendação do RecomendaSom (sem dependência do Streamlit)."""
import re

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

# 'key' ficou de fora: é categórica (0-11) e a distância de cosseno sobre ela não faz sentido.
FEATURES = [
    "danceability", "energy", "loudness", "mode", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
]

N_BUSCA = 1000  # vizinhos consultados, para sobrar candidatos após filtrar duplicatas


def _normalizar_titulo(titulo: str) -> str:
    """'Song - Remastered 2011' / 'Song (Live)' -> 'song', para barrar versões da mesma faixa."""
    t = str(titulo).lower()
    t = re.sub(r"\(.*?\)|\[.*?\]", " ", t)
    t = t.split(" - ")[0]
    return re.sub(r"\s+", " ", t).strip()


def carregar_dados(caminho: str = "dataset/dataset.csv") -> pd.DataFrame:
    df = pd.read_csv(caminho)
    df = df.dropna(subset=["track_name", "track_id", "artists", "track_genre"] + FEATURES)
    df = df.drop_duplicates(subset=["track_name", "artists"])
    df["nome_exibicao"] = df["track_name"] + " - " + df["artists"]
    df["titulo_norm"] = df["track_name"].map(_normalizar_titulo)
    return df.reset_index(drop=True)


def treinar_modelo(df: pd.DataFrame):
    scaler = MinMaxScaler()
    X = scaler.fit_transform(df[FEATURES])
    knn = NearestNeighbors(n_neighbors=N_BUSCA, metric="cosine", algorithm="brute")
    knn.fit(X)
    return knn, scaler, X


def recomendar_hibrido(pos: int, df, knn, X, n_mesmo_genero: int = 5, n_outros: int = 5) -> pd.DataFrame:
    """Recomenda n músicas do mesmo gênero da referência + n de outros gêneros.

    `pos` é a posição (0..len(df)-1) da música de referência.
    Retorna um DataFrame com coluna 'grupo' ('mesmo' ou 'outros') e 'similaridade'.
    Se faltar candidato num grupo, completa com o que sobrou do outro.
    """
    ref = df.iloc[pos]
    distancias, indices = knn.kneighbors(X[pos : pos + 1], n_neighbors=min(N_BUSCA, len(df)))

    vistos = {ref["titulo_norm"]}
    mesmo, outros = [], []
    for dist, i in zip(distancias[0], indices[0]):
        if i == pos:
            continue
        rec = df.iloc[i]
        if rec["titulo_norm"] in vistos:
            continue
        vistos.add(rec["titulo_norm"])
        item = {
            "track_id": rec["track_id"],
            "track_name": rec["track_name"],
            "artists": rec["artists"],
            "track_genre": rec["track_genre"],
            "similaridade": round((1 - dist) * 100, 1),
            "pos": int(i),
        }
        if rec["track_genre"] == ref["track_genre"]:
            mesmo.append(item)
        else:
            outros.append(item)
        if len(mesmo) >= n_mesmo_genero + n_outros and len(outros) >= n_mesmo_genero + n_outros:
            break

    sel_mesmo, sel_outros = mesmo[:n_mesmo_genero], outros[:n_outros]
    total = n_mesmo_genero + n_outros
    falta = total - len(sel_mesmo) - len(sel_outros)
    if falta > 0:  # fallback: completa com sobras de qualquer grupo
        sobras = mesmo[n_mesmo_genero:] + outros[n_outros:]
        sobras.sort(key=lambda d: -d["similaridade"])
        extra = sobras[:falta]
        sel_mesmo += [e for e in extra if e["track_genre"] == ref["track_genre"]]
        sel_outros += [e for e in extra if e["track_genre"] != ref["track_genre"]]

    out = pd.DataFrame(
        [dict(d, grupo="mesmo") for d in sel_mesmo] + [dict(d, grupo="outros") for d in sel_outros]
    )
    return out


def perfil_normalizado(X, df, pos_ref: int, posicoes_rec) -> tuple[list[float], list[float]]:
    """Perfil acústico (0-1) da referência e média das recomendações, na ordem de FEATURES."""
    ref = X[pos_ref]
    media = X[list(posicoes_rec)].mean(axis=0)
    return ref.tolist(), media.tolist()
