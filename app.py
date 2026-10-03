import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

st.set_page_config(page_title="RecomendaSom", page_icon="🎵", layout="wide")

css_customizado = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 0%, #1c1c26 0%, #050508 100%);
        color: #e0e0e0;
    }
    
    h1 {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 3.2rem !important;
        background: linear-gradient(180deg, #ffffff 20%, #8a8a9d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 20px rgba(255, 255, 255, 0.15);
        padding-bottom: 0.3rem;
    }

    h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        background: linear-gradient(180deg, #ffffff 30%, #9a9aac 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    div[data-testid="stTextInput"] div {
        border-radius: 50px !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    div[data-testid="stTextInput"] > div:nth-child(2) {
        background: linear-gradient(145deg, #1a1a24, #121218) !important;
        border: 2px solid #3a3a4e !important;
        padding: 4px 16px !important;
        box-shadow: inset 3px 3px 6px rgba(0,0,0,0.8) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stTextInput"] > div:nth-child(2):focus-within {
        border: 2px solid #1DB954 !important;
        box-shadow: 0 0 15px rgba(29, 185, 84, 0.5), inset 3px 3px 6px rgba(0,0,0,0.8) !important;
    }

    .stTextInput input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        padding-left: 5px !important;
    }

    div[data-testid="stSelectbox"] {
        border-radius: 50px !important;
    }

    div[data-testid="stSelectbox"] > div {
        background: linear-gradient(145deg, #1a1a24, #121218) !important;
        border: 2px solid #3a3a4e !important;
        border-radius: 50px !important;
        padding: 4px 16px !important;
        box-shadow: inset 3px 3px 6px rgba(0,0,0,0.8) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stSelectbox"] > div:focus-within {
        border: 2px solid #1DB954 !important;
        box-shadow: 0 0 15px rgba(29, 185, 84, 0.5), inset 3px 3px 6px rgba(0,0,0,0.8) !important;
    }

    div[data-testid="stSelectbox"] * {
        border-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
        background-color: transparent !important;
    }

    div[data-testid="stSelectbox"] span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    iframe {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
    }

    .stTextInput, .stSelectbox {
        margin-bottom: 1.5rem;
    }
    
    .cartao-musica {
        background: linear-gradient(145deg, #181820, #0f0f15);
        border: 1px solid #333344;
        border-top: 1px solid #a8a8b3;
        border-radius: 16px; 
        padding: 24px 20px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        transition: transform 0.2s ease-in-out;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .cartao-musica:hover {
        transform: translateY(-5px);
        border-top: 1px solid #e0e0e5;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8);
    }
    
    .badge-genero {
        display: inline-block;
        background: linear-gradient(145deg, #2a2a35, #1f1f28);
        color: #d0d0e0;
        padding: 4px 14px;
        border-radius: 30px; 
        font-size: 0.75em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid #4a4a5e;
        margin-bottom: 4px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    
    .titulo-musica {
        font-size: 1.2em;
        font-weight: 800;
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
        line-height: 1.2;
    }
    
    .artista-musica {
        font-size: 0.95em;
        color: #a0a0b0;
        font-weight: 500;
        margin-bottom: 2px;
    }
    
    .similaridade {
        color: #1DB954;
        font-size: 0.85em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
</style>
"""
st.markdown(css_customizado, unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    df = pd.read_csv("dataset/dataset.csv") 
    df = df.dropna(subset=['track_name', 'track_id', 'artists', 'track_genre'])
    
    df = df.drop_duplicates(subset=['track_name', 'artists'])
    df['nome_exibicao'] = df['track_name'] + " - " + df['artists']
    df = df.reset_index(drop=True)
    return df

df = carregar_dados()

@st.cache_resource
def treinar_modelo(dados):
    features = ['danceability', 'energy', 'valence', 'acousticness', 
                'instrumentalness', 'tempo', 'loudness', 'speechiness']
    
    scaler = MinMaxScaler()
    dados_normalizados = scaler.fit_transform(dados[features])
    
    knn = NearestNeighbors(n_neighbors=6, metric='cosine')
    knn.fit(dados_normalizados)
    
    return knn, scaler, features

knn_model, scaler_model, colunas_features = treinar_modelo(df)


st.title("Sistema de Recomendação de Músicas")
st.write("Digite uma música de referência para descobrir faixas com batida e energia semelhantes.")

busca = st.text_input("Qual música você quer usar como base? (Digite o nome ou artista)")

if busca:
    resultados_busca = df[df['nome_exibicao'].str.contains(busca, case=False, na=False)]
    
    if resultados_busca.empty:
        st.warning("Não encontramos essa música. Tente outro nome!")
    else:
        opcoes_leves = resultados_busca['nome_exibicao'].head(20).tolist()
        
        musica_selecionada = st.selectbox("Selecione a versão exata:", options=opcoes_leves)
        
        if musica_selecionada:
            musica_ref = df[df['nome_exibicao'] == musica_selecionada].iloc[0]
            
            genero_ref = str(musica_ref['track_genre']).title()
            
            st.subheader(f"🎶 Referência: {musica_ref['track_name']} - {musica_ref['artists']} | Gênero: {genero_ref}")
            
            iframe_ref = f"""
            <iframe style="border-radius:12px; background-color: transparent;" 
                    src="https://open.spotify.com/embed/track/{musica_ref['track_id']}?utm_source=generator&theme=0" 
                    width="100%" height="152" frameBorder="0" 
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
            </iframe>
            """
            st.markdown(iframe_ref, unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("🔥 Recomendações Baseadas na Similaridade de Áudio:")
            
            vetor_ref = musica_ref[colunas_features].values.reshape(1, -1)
            vetor_ref_normalizado = scaler_model.transform(vetor_ref)
            distancias, indices = knn_model.kneighbors(vetor_ref_normalizado)
            
            cols = st.columns(2)
            
            for i in range(1, 6):
                idx_recomendacao = indices[0][i]
                similaridade = (1 - distancias[0][i]) * 100
                musica_rec = df.iloc[idx_recomendacao]
                genero_rec = str(musica_rec['track_genre']).title()
                
                html_cartao = f"""
                <div class="cartao-musica">
                    <span class="badge-genero">{genero_rec}</span>
                    <div class="titulo-musica">{musica_rec['track_name']}</div>
                    <div class="artista-musica">{musica_rec['artists']}</div>
                    <div class="similaridade">Similaridade acústica: {similaridade:.1f}%</div>
                    <iframe style="border-radius:12px; background-color: transparent;" 
                            src="https://open.spotify.com/embed/track/{musica_rec['track_id']}?utm_source=generator&theme=0" 
                            width="100%" height="80" frameBorder="0" 
                            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
                    </iframe>
                </div>
                """
                
                with cols[(i - 1) % 2]:
                    st.markdown(html_cartao, unsafe_allow_html=True)

st.markdown("---")
rodape_html = """
<div style="text-align: center; color: #8a8a9d; font-family: 'Montserrat', sans-serif; font-size: 0.85em; padding-bottom: 20px;">
    <p>Desenvolvido por <b>Deborah Silvério Alves Morales</b> • Dados e players fornecidos por <b>Spotify</b>. O conteúdo musical pertence aos respectivos artistas e gravadoras.</p>
</div>
"""
st.markdown(rodape_html, unsafe_allow_html=True)