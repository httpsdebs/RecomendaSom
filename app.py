import html

import plotly.graph_objects as go
import streamlit as st

import recomendador as rec

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
    
    .titulo-secao {
        font-family: 'Montserrat', sans-serif;
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 800;
        margin: 8px 0 2px 0;
    }

    .legenda-secao {
        color: #8a8a9d;
        font-size: 0.9em;
        margin-bottom: 16px;
    }

    .similaridade {
        color: #1DB954;
        font-size: 0.85em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    /* ---------- Layout geral ---------- */
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
    .block-container { max-width: 1100px; padding-top: 2.2rem; padding-bottom: 2rem; }

    /* ---------- Hero ---------- */
    .hero { text-align: center; margin: 0 0 1.6rem 0; }
    .hero-eyebrow {
        display: inline-block; font-size: 0.75rem; font-weight: 800; letter-spacing: 2px;
        text-transform: uppercase; color: #1DB954; border: 1px solid rgba(29,185,84,0.4);
        background: rgba(29,185,84,0.08); border-radius: 30px; padding: 5px 14px; margin-bottom: 14px;
    }
    .hero h1 { margin: 0; }
    .hero p { color: #a0a0b0; font-size: 1.05rem; max-width: 620px; margin: 6px auto 0 auto; }

    /* ---------- Botões de exemplo (pílulas) ---------- */
    div[data-testid="stButton"] > button {
        width: 100%; border-radius: 50px; border: 1px solid #3a3a4e;
        background: linear-gradient(145deg, #1a1a24, #121218); color: #d0d0e0;
        font-size: 0.85rem; padding: 6px 10px; transition: all 0.2s ease;
    }
    div[data-testid="stButton"] > button:hover {
        border-color: #1DB954; color: #ffffff; box-shadow: 0 0 12px rgba(29,185,84,0.35);
        transform: translateY(-2px);
    }
    div[data-testid="stButton"] > button:focus:not(:active) { border-color: #1DB954; color: #fff; }
    .rotulo-exemplos { color: #8a8a9d; font-size: 0.85rem; margin: 4px 0 8px 4px; }

    /* ---------- Como funciona ---------- */
    .passo {
        background: linear-gradient(145deg, #181820, #0f0f15); border: 1px solid #2a2a38;
        border-radius: 16px; padding: 20px; height: 100%;
    }
    .passo-num {
        display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px;
        border-radius: 50%; background: rgba(29,185,84,0.15); color: #1DB954; font-weight: 800; margin-bottom: 10px;
    }
    .passo-titulo { color: #fff; font-weight: 800; margin-bottom: 4px; }
    .passo-texto { color: #a0a0b0; font-size: 0.92rem; line-height: 1.45; }

    /* ---------- Painel da referência ---------- */
    .medidor { margin-bottom: 10px; }
    .medidor-topo { display: flex; justify-content: space-between; font-size: 0.8rem; color: #a0a0b0; margin-bottom: 4px; }
    .medidor-topo b { color: #fff; font-weight: 700; }
    .barra { height: 6px; border-radius: 6px; background: #22222e; overflow: hidden; }
    .barra > span { display: block; height: 100%; border-radius: 6px; background: linear-gradient(90deg, #1DB954, #6ee7a0); }
    .chip-bpm {
        display: inline-block; font-size: 0.78rem; font-weight: 700; color: #d0d0e0; background: #1f1f28;
        border: 1px solid #4a4a5e; border-radius: 30px; padding: 3px 12px; margin: 2px 6px 10px 0;
    }

    /* ---------- Cartões: ranking e barra de similaridade ---------- */
    .cartao-topo { display: flex; align-items: center; justify-content: space-between; }
    .rank { color: #5a5a6e; font-family: 'Montserrat', sans-serif; font-weight: 900; font-size: 1.4rem; }
    .barra-sim { margin: 2px 0 10px 0; }
    .barra-sim .barra { height: 5px; }

    /* ---------- Abas ---------- */
    button[data-baseweb="tab"] { color: #a0a0b0; font-weight: 700; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #ffffff; }
    div[data-baseweb="tab-highlight"] { background-color: #1DB954 !important; }
    div[data-baseweb="tab-border"] { background-color: #2a2a38 !important; }
    div[data-baseweb="tab-list"] { gap: 6px; }
</style>
"""
st.markdown(css_customizado, unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    return rec.carregar_dados("dataset/dataset.csv")


@st.cache_resource
def treinar_modelo(_dados):
    knn, scaler, X = rec.treinar_modelo(_dados)
    return knn, X


df = carregar_dados()
knn_model, X_norm = treinar_modelo(df)


EXEMPLOS = ["Master of Puppets", "Blinding Lights", "Bohemian Rhapsody",
            "Smells Like Teen Spirit", "Someone Like You", "Faroeste Caboclo"]

MEDIDORES = [("danceability", "Dançabilidade"), ("energy", "Energia"),
             ("valence", "Positividade"), ("acousticness", "Acústico")]


def usar_exemplo(nome):
    st.session_state["busca"] = nome


def html_iframe(track_id, altura):
    return (f'<iframe style="border-radius:12px; background-color: transparent;" '
            f'src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0" '
            f'width="100%" height="{altura}" frameBorder="0" loading="lazy" '
            f'allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>')


def html_medidor(rotulo, valor):
    pct = max(0, min(100, valor * 100))
    return (f'<div class="medidor"><div class="medidor-topo"><span>{rotulo}</span><b>{pct:.0f}%</b></div>'
            f'<div class="barra"><span style="width:{pct:.0f}%"></span></div></div>')


def mostrar_cartoes(recomendacoes, inicio=1):
    if recomendacoes.empty:
        st.info("Não encontramos faixas suficientes neste grupo.")
        return
    cols = st.columns(2)
    for n, (_, r) in enumerate(recomendacoes.iterrows()):
        genero = html.escape(str(r["track_genre"]).title())
        html_cartao = (
            '<div class="cartao-musica">'
            f'<div class="cartao-topo"><span class="badge-genero">{genero}</span><span class="rank">{n + inicio:02d}</span></div>'
            f'<div class="titulo-musica">{html.escape(str(r["track_name"]))}</div>'
            f'<div class="artista-musica">{html.escape(str(r["artists"]))}</div>'
            f'<div class="similaridade">Similaridade acústica: {r["similaridade"]:.1f}%</div>'
            f'<div class="barra-sim"><div class="barra"><span style="width:{r["similaridade"]:.0f}%"></span></div></div>'
            f'{html_iframe(r["track_id"], 80)}'
            '</div>'
        )
        with cols[n % 2]:
            st.markdown(html_cartao, unsafe_allow_html=True)


def grafico_radar(pos_ref, nome_ref, posicoes_rec):
    perfil_ref, perfil_rec = rec.perfil_normalizado(X_norm, df, pos_ref, posicoes_rec)
    rotulos = rec.FEATURES + [rec.FEATURES[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=perfil_ref + perfil_ref[:1], theta=rotulos, fill="toself",
        name=f"Referência: {nome_ref}", line_color="#1DB954"))
    fig.add_trace(go.Scatterpolar(
        r=perfil_rec + perfil_rec[:1], theta=rotulos, fill="toself",
        name="Média das recomendações", line_color="#a8a8b3"))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 1])),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e0e0e0"),
        legend=dict(orientation="h", y=-0.1), margin=dict(t=30, b=30))
    return fig


# ---------------------------- Interface ----------------------------
st.markdown(
    '<div class="hero"><span class="hero-eyebrow">Descoberta musical por áudio</span>'
    '<h1>RecomendaSom</h1>'
    '<p>Escolha uma música e encontre faixas com a mesma batida, energia e clima, '
    'dentro do mesmo estilo ou em gêneros que você ainda não explorou.</p></div>',
    unsafe_allow_html=True)

busca = st.text_input(
    "Música de referência", key="busca", label_visibility="collapsed",
    placeholder="🔎  Digite o nome da música ou do artista...")

if not busca:
    st.markdown('<div class="rotulo-exemplos">Sem ideia? Experimente uma destas:</div>', unsafe_allow_html=True)
    cols_ex = st.columns(3)
    for i, nome in enumerate(EXEMPLOS):
        with cols_ex[i % 3]:
            st.button(nome, key=f"ex_{i}", on_click=usar_exemplo, args=(nome,))

    st.markdown("<br>", unsafe_allow_html=True)
    passos = [("1", "Escolha a base", "Busque uma música que você gosta. Se houver várias versões, é só selecionar a certa."),
              ("2", "Comparamos o som", "Analisamos dançabilidade, energia, clima, ritmo e mais 6 características de áudio."),
              ("3", "Ouça e descubra", "Receba 10 sugestões: 5 do mesmo gênero e 5 de outros estilos, com player do Spotify.")]
    for col, (num, titulo, texto) in zip(st.columns(3), passos):
        col.markdown(f'<div class="passo"><div class="passo-num">{num}</div>'
                     f'<div class="passo-titulo">{titulo}</div><div class="passo-texto">{texto}</div></div>',
                     unsafe_allow_html=True)
else:
    resultados_busca = df[df['nome_exibicao'].str.contains(busca, case=False, na=False, regex=False)]

    if resultados_busca.empty:
        st.warning("Não encontramos essa música. Tente outro nome ou o nome do artista!")
    else:
        # ordena por popularidade para a versão mais conhecida aparecer primeiro
        resultados_busca = resultados_busca.sort_values("popularity", ascending=False).head(20)
        opcoes = dict(zip(resultados_busca['nome_exibicao'], resultados_busca.index))

        musica_selecionada = st.selectbox(
            f"{len(opcoes)} resultado(s). Selecione a versão exata:", options=list(opcoes))

        if musica_selecionada:
            pos_ref = opcoes[musica_selecionada]
            musica_ref = df.iloc[pos_ref]
            genero_ref = str(musica_ref['track_genre']).title()

            # ---- painel da referência: player + perfil sonoro
            st.markdown(f'<div class="titulo-secao">🎶 Referência</div>'
                        f'<div class="legenda-secao">{html.escape(str(musica_ref["track_name"]))} · '
                        f'{html.escape(str(musica_ref["artists"]))} · Gênero: {html.escape(genero_ref)}</div>',
                        unsafe_allow_html=True)
            col_player, col_perfil = st.columns([3, 2])
            with col_player:
                st.markdown(html_iframe(musica_ref['track_id'], 152), unsafe_allow_html=True)
            with col_perfil:
                medidores = "".join(html_medidor(nome, musica_ref[c]) for c, nome in MEDIDORES)
                st.markdown(f'<span class="chip-bpm">♩ {musica_ref["tempo"]:.0f} BPM</span>' + medidores,
                            unsafe_allow_html=True)

            recomendacoes = rec.recomendar_hibrido(pos_ref, df, knn_model, X_norm)
            mesmo = recomendacoes[recomendacoes["grupo"] == "mesmo"]
            outros = recomendacoes[recomendacoes["grupo"] == "outros"]

            st.markdown("<br>", unsafe_allow_html=True)
            aba_mesmo, aba_outros, aba_perfil = st.tabs(
                [f"🔥 Mesmo gênero ({len(mesmo)})", f"🧭 Outros gêneros ({len(outros)})", "📊 Perfil acústico"])

            with aba_mesmo:
                st.markdown(f'<div class="legenda-secao">As faixas mais parecidas dentro de {html.escape(genero_ref)}.</div>',
                            unsafe_allow_html=True)
                mostrar_cartoes(mesmo)

            with aba_outros:
                st.markdown('<div class="legenda-secao">Mesma pegada sonora, mas de estilos diferentes. Bom para sair da bolha.</div>',
                            unsafe_allow_html=True)
                mostrar_cartoes(outros)

            with aba_perfil:
                st.markdown('<div class="legenda-secao">Quanto mais as duas áreas se sobrepõem, mais coesas são as recomendações.</div>',
                            unsafe_allow_html=True)
                st.plotly_chart(
                    grafico_radar(pos_ref, musica_ref['track_name'], recomendacoes["pos"].tolist()),
                    use_container_width=True)

st.markdown("---")
rodape_html = """
<div style="text-align: center; color: #8a8a9d; font-family: 'Montserrat', sans-serif; font-size: 0.85em; padding-bottom: 20px;">
    <p>Desenvolvido por <b>Deborah Silvério Alves Morales</b> • Dados e players fornecidos por <b>Spotify</b>. O conteúdo musical pertence aos respectivos artistas e gravadoras.</p>
</div>
"""
st.markdown(rodape_html, unsafe_allow_html=True)
