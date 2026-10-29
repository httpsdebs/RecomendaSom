import html

import plotly.graph_objects as go
import streamlit as st

import recomendador as rec

st.set_page_config(page_title="RecomendaSom", page_icon="favicon.png", layout="wide")

FONTES_URL = ("https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900"
              "&family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;700&display=swap")

# CSS compartilhado: usado na página E dentro dos iframes dos players (garante fontes idênticas).
CSS_BASE = """
:root {
    --verde: #1ed760; --ciano: #22d3ee; --roxo: #8b5cf6;
    --fundo: #05060d; --painel: rgba(14, 18, 32, 0.92);
    --borda: rgba(130, 150, 210, 0.20); --texto: #e6eaf5; --texto-suave: #8f9bb8;
    --f-titulo: 'Orbitron', 'Segoe UI', sans-serif;
    --f-corpo: 'Space Grotesk', 'Segoe UI', sans-serif;
    --f-mono: 'JetBrains Mono', 'Consolas', monospace;
}

/* ---------- Cartões ---------- */
.cartao-musica {
    position: relative; overflow: hidden;
    background: linear-gradient(160deg, rgba(24, 30, 52, 0.95), rgba(8, 11, 21, 0.97));
    border: 1px solid var(--borda); border-radius: 14px;
    padding: 22px 20px 20px 22px; margin-bottom: 24px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.55);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    display: flex; flex-direction: column; gap: 8px;
    font-family: var(--f-corpo); color: var(--texto);
}
.cartao-musica::before {
    content: ""; position: absolute; left: 0; right: 0; top: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--verde), var(--ciano), transparent); opacity: 0.85;
}
.cartao-musica::after {
    content: ""; position: absolute; left: 0; top: 18px; bottom: 18px; width: 2px;
    background: linear-gradient(180deg, var(--verde), var(--ciano)); opacity: 0.55; border-radius: 2px;
}
.cartao-musica:hover {
    transform: translateY(-3px); border-color: rgba(30, 215, 96, 0.55);
    box-shadow: 0 0 22px rgba(30, 215, 96, 0.22), 0 16px 36px rgba(0, 0, 0, 0.7);
}
.cartao-topo { display: flex; align-items: center; justify-content: space-between; }
.rank {
    font-family: var(--f-titulo); font-weight: 900; font-size: 1.6rem; line-height: 1;
    color: transparent; -webkit-text-stroke: 1px rgba(34, 211, 238, 0.6);
}
.badge-genero {
    display: inline-block; font-family: var(--f-mono); font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.5px; color: var(--ciano);
    background: rgba(34, 211, 238, 0.08); border: 1px solid rgba(34, 211, 238, 0.35);
    border-radius: 6px; padding: 4px 10px;
}
.titulo-musica { font-family: var(--f-corpo); font-size: 1.15em; font-weight: 700; color: #fff; line-height: 1.25; }
.artista-musica { font-family: var(--f-corpo); font-size: 0.95em; color: var(--texto-suave); font-weight: 500; }
.similaridade {
    font-family: var(--f-mono); color: var(--verde); font-size: 0.74em; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;
}

/* ---------- Barras segmentadas (estilo HUD) ---------- */
.barra, .barra > span {
    -webkit-mask-image: repeating-linear-gradient(90deg, #000 0 7px, transparent 7px 9px);
            mask-image: repeating-linear-gradient(90deg, #000 0 7px, transparent 7px 9px);
}
.barra { height: 7px; background: #1a2135; overflow: hidden; border-radius: 2px; }
.barra > span { display: block; height: 100%; background: linear-gradient(90deg, var(--verde), var(--ciano)); }
.barra-sim { margin: 0 0 10px 0; }

.titulo-secao {
    font-family: var(--f-titulo); color: #fff; font-size: 1.05rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase; margin: 8px 0 2px 0;
}
.titulo-secao::before { content: ""; display: inline-block; width: 4px; height: 1em; margin-right: 10px;
    vertical-align: -2px; background: linear-gradient(180deg, var(--verde), var(--ciano)); border-radius: 2px; }
.legenda-secao { font-family: var(--f-corpo); color: var(--texto-suave); font-size: 0.92em; margin-bottom: 16px; }

/* ---------- Skeleton enquanto o player do Spotify carrega ---------- */
.player {
    min-height: 80px; border-radius: 12px; border: 1px solid var(--borda);
    background: linear-gradient(100deg, #0d1224 30%, #161d36 50%, #0d1224 70%) 0 0 / 220% 100%;
    animation: shimmer 1.4s linear infinite;
}
@keyframes shimmer { to { background-position: -220% 0; } }
"""

CSS_PAGINA = f"""
@import url('{FONTES_URL}');

html, body, .stApp, p, label, input, button, li, h1, h2, h3,
[data-baseweb="tab"], [data-baseweb="select"] div, [data-testid="stMarkdownContainer"] {{
    font-family: var(--f-corpo) !important;
}}

.stApp {{
    color: var(--texto);
    background:
        radial-gradient(900px 520px at 12% -8%, rgba(34, 211, 238, 0.13), transparent 60%),
        radial-gradient(900px 520px at 92% 0%, rgba(30, 215, 96, 0.12), transparent 60%),
        radial-gradient(700px 500px at 50% 110%, rgba(139, 92, 246, 0.10), transparent 60%),
        linear-gradient(rgba(255,255,255,0.028) 1px, transparent 1px) 0 0 / 46px 46px,
        linear-gradient(90deg, rgba(255,255,255,0.028) 1px, transparent 1px) 0 0 / 46px 46px,
        var(--fundo);
    background-attachment: fixed;
}}

#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
.block-container {{ max-width: 1100px; padding-top: 2.2rem; padding-bottom: 2rem; }}
iframe {{ border: none !important; outline: none !important; background-color: transparent !important; }}

/* ---------- Hero ---------- */
.hero {{ text-align: center; margin: 0 0 1.8rem 0; }}
.eq {{ display: flex; gap: 4px; justify-content: center; align-items: flex-end; height: 38px; margin-bottom: 14px; }}
.eq span {{ width: 4px; height: 100%; border-radius: 2px; background: linear-gradient(180deg, var(--ciano), var(--verde));
    transform-origin: bottom; animation: eq 1.2s ease-in-out infinite; box-shadow: 0 0 8px rgba(30,215,96,0.5); }}
.eq span:nth-child(1) {{ animation-delay: -0.9s; }} .eq span:nth-child(2) {{ animation-delay: -0.5s; }}
.eq span:nth-child(3) {{ animation-delay: -0.2s; }} .eq span:nth-child(4) {{ animation-delay: -0.7s; }}
.eq span:nth-child(5) {{ animation-delay: -0.35s; }} .eq span:nth-child(6) {{ animation-delay: -1s; }}
.eq span:nth-child(7) {{ animation-delay: -0.1s; }}
@keyframes eq {{ 0%, 100% {{ transform: scaleY(0.2); }} 50% {{ transform: scaleY(1); }} }}
.hero-eyebrow {{
    display: inline-flex; align-items: center; gap: 8px; font-family: var(--f-mono); font-size: 0.72rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase; color: var(--verde);
    border: 1px solid rgba(30, 215, 96, 0.4); background: rgba(30, 215, 96, 0.07);
    border-radius: 6px; padding: 5px 12px; margin-bottom: 16px;
}}
.hero-eyebrow::before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--verde);
    box-shadow: 0 0 8px var(--verde); animation: pisca 1.6s ease-in-out infinite; }}
@keyframes pisca {{ 50% {{ opacity: 0.25; }} }}
.hero h1 {{
    font-family: var(--f-titulo) !important; font-weight: 900 !important; font-size: 3.2rem !important;
    letter-spacing: 4px; margin: 0; padding: 0 0 0.3rem 0; text-transform: uppercase;
    background: linear-gradient(90deg, #ffffff 10%, var(--ciano) 55%, var(--verde) 95%);
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 18px rgba(34, 211, 238, 0.35));
}}
.hero p {{ color: var(--texto-suave); font-size: 1.05rem; max-width: 640px; margin: 8px auto 0 auto; line-height: 1.5; }}
@media (max-width: 640px) {{ .hero h1 {{ font-size: 2rem !important; letter-spacing: 2px; }} }}

/* ---------- Campos ---------- */
div[data-testid="stTextInput"] div {{ border-radius: 12px !important; background-color: transparent !important;
    border: none !important; box-shadow: none !important; }}
div[data-testid="stTextInput"] > div:nth-child(2) {{
    background: rgba(10, 14, 26, 0.9) !important; border: 1px solid var(--borda) !important;
    padding: 4px 16px !important; transition: all 0.25s ease !important; }}
div[data-testid="stTextInput"] > div:nth-child(2):focus-within {{
    border: 1px solid var(--verde) !important;
    box-shadow: 0 0 0 3px rgba(30, 215, 96, 0.15), 0 0 22px rgba(30, 215, 96, 0.35) !important; }}
.stTextInput input {{ color: #fff !important; -webkit-text-fill-color: #fff !important; padding-left: 5px !important;
    font-family: var(--f-mono) !important; font-size: 0.95rem !important; }}
.stTextInput input::placeholder {{ color: #5d6a88 !important; -webkit-text-fill-color: #5d6a88 !important; }}

div[data-testid="stSelectbox"] > div {{ background: rgba(10, 14, 26, 0.9) !important; border: 1px solid var(--borda) !important;
    border-radius: 12px !important; padding: 4px 16px !important; transition: all 0.25s ease !important; }}
div[data-testid="stSelectbox"] > div:focus-within {{ border: 1px solid var(--verde) !important;
    box-shadow: 0 0 22px rgba(30, 215, 96, 0.3) !important; }}
div[data-testid="stSelectbox"] * {{ border-color: transparent !important; box-shadow: none !important;
    outline: none !important; background-color: transparent !important; }}
div[data-testid="stSelectbox"] span {{ color: #fff !important; -webkit-text-fill-color: #fff !important; }}
div[data-testid="stSelectbox"] label p, .stTextInput label p {{ font-family: var(--f-mono) !important; font-size: 0.78rem;
    letter-spacing: 1px; text-transform: uppercase; color: var(--texto-suave); }}
.stTextInput, .stSelectbox {{ margin-bottom: 1.2rem; }}

/* ---------- Botões de exemplo ---------- */
div[data-testid="stButton"] > button {{
    width: 100%; border-radius: 10px; border: 1px solid var(--borda); background: rgba(10, 14, 26, 0.85);
    color: #c9d2ea; font-family: var(--f-mono) !important; font-size: 0.8rem; padding: 8px 10px; transition: all 0.2s ease;
}}
div[data-testid="stButton"] > button:hover {{
    border-color: var(--ciano); color: #fff; box-shadow: 0 0 16px rgba(34, 211, 238, 0.35); transform: translateY(-2px);
}}
div[data-testid="stButton"] > button:focus:not(:active) {{ border-color: var(--ciano); color: #fff; }}
.rotulo-exemplos {{ font-family: var(--f-mono); color: var(--texto-suave); font-size: 0.78rem; letter-spacing: 1px;
    text-transform: uppercase; margin: 4px 0 10px 2px; }}

/* ---------- Como funciona ---------- */
.passo {{ position: relative; background: linear-gradient(160deg, rgba(24, 30, 52, 0.9), rgba(8, 11, 21, 0.95));
    border: 1px solid var(--borda); border-radius: 14px; padding: 20px; height: 100%; overflow: hidden; }}
.passo::before {{ content: ""; position: absolute; left: 0; right: 0; top: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--ciano), transparent); opacity: 0.8; }}
.passo-num {{ font-family: var(--f-titulo); font-weight: 900; font-size: 1.7rem; color: transparent;
    -webkit-text-stroke: 1px rgba(30, 215, 96, 0.7); margin-bottom: 8px; }}
.passo-titulo {{ color: #fff; font-weight: 700; margin-bottom: 4px; font-size: 1.05rem; }}
.passo-texto {{ color: var(--texto-suave); font-size: 0.92rem; line-height: 1.5; }}

/* ---------- Painel da referência ---------- */
.medidor {{ margin-bottom: 11px; }}
.medidor-topo {{ display: flex; justify-content: space-between; font-family: var(--f-mono); font-size: 0.72rem;
    letter-spacing: 1px; text-transform: uppercase; color: var(--texto-suave); margin-bottom: 5px; }}
.medidor-topo b {{ color: var(--verde); font-weight: 700; }}
.chip-bpm {{ display: inline-block; font-family: var(--f-mono); font-size: 0.74rem; font-weight: 700; letter-spacing: 1px;
    color: var(--ciano); background: rgba(34, 211, 238, 0.08); border: 1px solid rgba(34, 211, 238, 0.35);
    border-radius: 6px; padding: 4px 12px; margin: 2px 6px 12px 0; }}

/* ---------- Abas ---------- */
button[data-baseweb="tab"] {{ color: var(--texto-suave); font-family: var(--f-mono) !important; font-weight: 700;
    font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color: #fff; text-shadow: 0 0 12px rgba(30, 215, 96, 0.6); }}
div[data-baseweb="tab-highlight"] {{ background-color: var(--verde) !important; box-shadow: 0 0 10px var(--verde); }}
div[data-baseweb="tab-border"] {{ background-color: rgba(130, 150, 210, 0.15) !important; }}
div[data-baseweb="tab-list"] {{ gap: 8px; }}

/* ---------- Rodapé ---------- */
.rodape {{ text-align: center; color: #5d6a88; font-family: var(--f-mono); font-size: 0.72rem; letter-spacing: 0.5px;
    line-height: 1.7; padding: 4px 0 20px 0; }}
.rodape b {{ color: var(--texto-suave); }}
"""

st.markdown(f"<style>{CSS_BASE}{CSS_PAGINA}</style>", unsafe_allow_html=True)


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


SCRIPT_PLAYERS = """
<script>
(function () {
  // Registro compartilhado entre todos os blocos de players da página (mesma origem do app).
  var reg;
  try { reg = window.parent.__rsPlayers = window.parent.__rsPlayers || {lista: [], atual: null}; }
  catch (e) { reg = window.__rsPlayers = window.__rsPlayers || {lista: [], atual: null}; }

  window.onSpotifyIframeApiReady = function (API) {
    document.querySelectorAll('.player').forEach(function (el) {
      API.createController(el,
        {uri: 'spotify:track:' + el.dataset.id, width: '100%', height: parseInt(el.dataset.h, 10)},
        function (ctrl) {
          reg.lista.push(ctrl);
          ctrl.addListener('playback_update', function (e) {
            if (!e.data || e.data.isPaused) return;
            if (reg.atual && reg.atual !== ctrl) { try { reg.atual.pause(); } catch (err) {} }
            reg.atual = ctrl;
          });
        });
    });
  };

  // Plano B: se a API do Spotify não carregar, mostra os players comuns.
  setTimeout(function () {
    document.querySelectorAll('.player').forEach(function (el) {
      var f = document.createElement('iframe');
      f.src = 'https://open.spotify.com/embed/track/' + el.dataset.id + '?utm_source=generator&theme=0';
      f.width = '100%'; f.height = el.dataset.h; f.frameBorder = 0; f.loading = 'lazy';
      f.allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture';
      f.style.borderRadius = '12px';
      el.replaceWith(f);
    });
  }, 8000);
})();
</script>
<script src="https://open.spotify.com/embed/iframe-api/v1" async></script>
"""

CSS_PLAYERS = """
<style>
    body { margin: 0; padding: 6px 2px 0 2px; background: transparent; font-family: var(--f-corpo); }
    .grade { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 20px; }
    @media (max-width: 640px) { .grade { grid-template-columns: minmax(0, 1fr); } }
    .cartao-musica { min-width: 0; }
    .titulo-musica, .artista-musica { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>
"""

ALTURA_CARTAO = 318  # altura de um cartão + espaçamento (px)


def html_player(track_id, altura):
    return f'<div class="player" data-id="{track_id}" data-h="{altura}"></div>'


def renderizar_html(conteudo, altura):
    """Mostra HTML com JavaScript. Usa st.iframe (Streamlit recente) ou components.html (antigo)."""
    pagina = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<link rel='preconnect' href='https://fonts.googleapis.com'>"
        "<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
        "<link rel='preconnect' href='https://open.spotify.com'>"
        f"<link rel='stylesheet' href='{FONTES_URL}'>"
        f"<style>{CSS_BASE}</style>{CSS_PLAYERS}</head><body>{conteudo}{SCRIPT_PLAYERS}</body></html>"
    )
    if hasattr(st, "iframe"):
        st.iframe(pagina, height=altura)
    else:
        import streamlit.components.v1 as components
        components.html(pagina, height=altura)


def html_medidor(rotulo, valor):
    pct = max(0, min(100, valor * 100))
    return (f'<div class="medidor"><div class="medidor-topo"><span>{rotulo}</span><b>{pct:.0f}%</b></div>'
            f'<div class="barra"><span style="width:{pct:.0f}%"></span></div></div>')


def mostrar_cartoes(recomendacoes, inicio=1):
    if recomendacoes.empty:
        st.info("Não encontramos faixas suficientes neste grupo.")
        return
    cartoes = []
    for n, (_, r) in enumerate(recomendacoes.iterrows()):
        genero = html.escape(str(r["track_genre"]).title())
        cartoes.append(
            '<div class="cartao-musica">'
            f'<div class="cartao-topo"><span class="badge-genero">{genero}</span><span class="rank">{n + inicio:02d}</span></div>'
            f'<div class="titulo-musica">{html.escape(str(r["track_name"]))}</div>'
            f'<div class="artista-musica">{html.escape(str(r["artists"]))}</div>'
            f'<div class="similaridade">Similaridade acústica: {r["similaridade"]:.1f}%</div>'
            f'<div class="barra-sim"><div class="barra"><span style="width:{r["similaridade"]:.0f}%"></span></div></div>'
            f'{html_player(r["track_id"], 80)}'
            '</div>'
        )
    linhas = (len(cartoes) + 1) // 2
    renderizar_html(f'<div class="grade">{"".join(cartoes)}</div>', linhas * ALTURA_CARTAO + 12)


def grafico_radar(pos_ref, nome_ref, posicoes_rec):
    perfil_ref, perfil_rec = rec.perfil_normalizado(X_norm, df, pos_ref, posicoes_rec)
    rotulos = rec.FEATURES + [rec.FEATURES[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=perfil_ref + perfil_ref[:1], theta=rotulos, fill="toself",
        name=f"Referência: {nome_ref}", line=dict(color="#1ed760", width=2), fillcolor="rgba(30,215,96,0.18)"))
    fig.add_trace(go.Scatterpolar(
        r=perfil_rec + perfil_rec[:1], theta=rotulos, fill="toself",
        name="Média das recomendações", line=dict(color="#22d3ee", width=2), fillcolor="rgba(34,211,238,0.15)"))
    grade = "rgba(130,150,210,0.18)"
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(visible=True, range=[0, 1], gridcolor=grade, linecolor=grade,
                                   tickfont=dict(size=9, color="#5d6a88")),
                   angularaxis=dict(gridcolor=grade, linecolor=grade)),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c9d2ea", family="Space Grotesk, sans-serif"),
        legend=dict(orientation="h", y=-0.1), margin=dict(t=30, b=30))
    return fig


# ---------------------------- Interface ----------------------------
st.markdown(
    '<div class="hero"><div class="eq">' + '<span></span>' * 7 + '</div>'
    '<span class="hero-eyebrow">Descoberta musical por áudio</span>'
    '<h1>RecomendaSom</h1>'
    '<p>Escolha uma música e encontre faixas com a mesma batida, energia e clima, '
    'dentro do mesmo estilo ou em gêneros que você ainda não explorou.</p></div>',
    unsafe_allow_html=True)

busca = st.text_input(
    "Música de referência", key="busca", label_visibility="collapsed",
    placeholder="Digite o nome da música ou do artista...")

if not busca:
    st.markdown('<div class="rotulo-exemplos">Sem ideia? Experimente uma destas:</div>', unsafe_allow_html=True)
    cols_ex = st.columns(3)
    for i, nome in enumerate(EXEMPLOS):
        with cols_ex[i % 3]:
            st.button(nome, key=f"ex_{i}", on_click=usar_exemplo, args=(nome,))

    st.markdown("<br>", unsafe_allow_html=True)
    passos = [("01", "Escolha a base", "Busque uma música que você gosta. Se houver várias versões, é só selecionar a certa."),
              ("02", "Comparamos o som", "Analisamos dançabilidade, energia, clima, ritmo e mais 6 características de áudio."),
              ("03", "Ouça e descubra", "Receba 10 sugestões: 5 do mesmo gênero e 5 de outros estilos, com player do Spotify.")]
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
            st.markdown(f'<div class="titulo-secao">Referência</div>'
                        f'<div class="legenda-secao">{html.escape(str(musica_ref["track_name"]))} · '
                        f'{html.escape(str(musica_ref["artists"]))} · Gênero: {html.escape(genero_ref)}</div>',
                        unsafe_allow_html=True)
            col_player, col_perfil = st.columns([3, 2])
            with col_player:
                renderizar_html(html_player(musica_ref['track_id'], 152), 160)
            with col_perfil:
                medidores = "".join(html_medidor(nome, musica_ref[c]) for c, nome in MEDIDORES)
                st.markdown(f'<span class="chip-bpm">{musica_ref["tempo"]:.0f} BPM</span>' + medidores,
                            unsafe_allow_html=True)

            recomendacoes = rec.recomendar_hibrido(pos_ref, df, knn_model, X_norm)
            mesmo = recomendacoes[recomendacoes["grupo"] == "mesmo"]
            outros = recomendacoes[recomendacoes["grupo"] == "outros"]

            st.markdown("<br>", unsafe_allow_html=True)
            aba_mesmo, aba_outros, aba_perfil = st.tabs(
                [f"Mesmo gênero ({len(mesmo)})", f"Outros gêneros ({len(outros)})", "Perfil acústico"])

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

st.markdown(
    '<div class="rodape">Desenvolvido por <b>Deborah Silvério Alves Morales</b><br>'
    'Dados e players fornecidos por <b>Spotify</b>. O conteúdo musical pertence aos respectivos artistas e gravadoras.</div>',
    unsafe_allow_html=True)
