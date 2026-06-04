import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sankey énergie",
    layout="wide"
)

st.title("Sankey interactif — réduire le flux carboné")

st.markdown(
    """
    Cette applet permet d’explorer comment réduire le flux d’énergie d’origine
    carbonée dans un système d’usages sociétaux.

    Les flux sont exprimés en **unités arbitraires**.  
    La contrainte imposée est la conservation :

    **flux entrants = flux sortants**
    """
)

st.info(
    "Question possible pour les élèves : comment faire pour réduire le flux "
    "d’énergie carbonée mobilisé par ce système ?"
)

# ------------------------------------------------------------
# Valeurs initiales
# ------------------------------------------------------------

if "utile" not in st.session_state:
    st.session_state.utile = 55.0

if "inutile" not in st.session_state:
    st.session_state.inutile = 45.0

if "uranium" not in st.session_state:
    st.session_state.uranium = 40.0

if "autres_decarbones" not in st.session_state:
    st.session_state.autres_decarbones = 25.0

if "objectif_carbone" not in st.session_state:
    st.session_state.objectif_carbone = 20.0


# ------------------------------------------------------------
# Zone de réglage horizontale
# ------------------------------------------------------------

st.subheader("Paramètres manipulables")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    utile = st.slider(
        "Taille du convertisseur",
        min_value=10.0,
        max_value=100.0,
        value=st.session_state.utile,
        step=1.0,
        help="Diminuer cette valeur revient à réduire le niveau global des usages sociétaux."
    )

with col2:
    inutile = st.slider(
        "Énergie inutile",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.inutile,
        step=1.0,
        help="Diminuer cette valeur revient à réduire l’énergie qui ne produit pas l’effet utile recherché."
    )

with col3:
    uranium = st.slider(
        "Uranium",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.uranium,
        step=1.0,
        help="Augmenter cette valeur revient à mobiliser davantage d’énergie issue de l’uranium."
    )

with col4:
    autres_decarbones = st.slider(
        "Autres sources décarbonées",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.autres_decarbones,
        step=1.0,
        help="Augmenter cette valeur revient à mobiliser davantage de sources décarbonées autres que l’uranium."
    )

with col5:
    objectif_carbone = st.slider(
        "Objectif maximal de flux carboné",
        min_value=0.0,
        max_value=60.0,
        value=st.session_state.objectif_carbone,
        step=1.0,
        help="L’objectif est atteint si le flux carboné calculé est inférieur ou égal à cette valeur."
    )

st.session_state.utile = utile
st.session_state.inutile = inutile
st.session_state.uranium = uranium
st.session_state.autres_decarbones = autres_decarbones
st.session_state.objectif_carbone = objectif_carbone


# ------------------------------------------------------------
# Calculs en unités arbitraires
# ------------------------------------------------------------

# À droite : le système produit de l'utile et de l'inutile.
flux_utile = utile
flux_inutile = inutile
total_entrant = flux_utile + flux_inutile
total_sortant = flux_utile + flux_inutile

# À gauche : l'utilisateur choisit deux contributions décarbonées.
# Elles sont mobilisées dans la limite du total entrant nécessaire.
flux_uranium = min(uranium, total_entrant)

reste_apres_uranium = max(0.0, total_entrant - flux_uranium)
flux_autres_decarbones = min(autres_decarbones, reste_apres_uranium)

# Le carboné est le résidu : ce qu'il reste à fournir.
flux_carbone = max(0.0, total_entrant - flux_uranium - flux_autres_decarbones)

# Si l'utilisateur propose plus de décarboné que nécessaire, on l'indique.
uranium_non_utilise = max(0.0, uranium - flux_uranium)
autres_decarbones_non_utilises = max(0.0, autres_decarbones - flux_autres_decarbones)
decarbone_non_utilise = uranium_non_utilise + autres_decarbones_non_utilises

flux_decarbone_total = flux_uranium + flux_autres_decarbones


# ------------------------------------------------------------
# Bilan synthétique
# ------------------------------------------------------------

st.subheader("Bilan")

b1, b2, b3, b4, b5 = st.columns(5)

with b1:
    st.metric("Total entrant", f"{total_entrant:.0f} unités")

with b2:
    st.metric("Énergie utile", f"{flux_utile:.0f} unités")

with b3:
    st.metric("Énergie inutile", f"{flux_inutile:.0f} unités")

with b4:
    st.metric("Flux carboné calculé", f"{flux_carbone:.0f} unités")

with b5:
    st.metric("Flux décarboné total", f"{flux_decarbone_total:.0f} unités")

if flux_carbone <= objectif_carbone:
    st.success("Objectif atteint : le flux carboné calculé est inférieur ou égal à l’objectif.")
else:
    st.warning("Objectif non atteint : il faut encore agir sur un ou plusieurs leviers.")

if decarbone_non_utilise > 0:
    st.caption(
        f"{decarbone_non_utilise:.0f} unités de sources décarbonées proposées ne sont pas mobilisées, "
        "car le besoin total du système est déjà couvert."
    )

st.caption("Conservation respectée : flux entrants = flux sortants.")

st.divider()


# ------------------------------------------------------------
# Sankey
# ------------------------------------------------------------

labels = [
    "Sources carbonées",
    "Uranium",
    "Autres sources décarbonées",
    "Convertisseur : usages sociétaux",
    "Énergie utile",
    "Énergie inutile"
]

source = [0, 1, 2, 3, 3]
target = [3, 3, 3, 4, 5]
value = [
    flux_carbone,
    flux_uranium,
    flux_autres_decarbones,
    flux_utile,
    flux_inutile
]

node_colors = [
    "rgba(210, 40, 40, 0.95)",     # sources carbonées
    "rgba(120, 120, 120, 0.90)",   # uranium
    "rgba(80, 150, 90, 0.90)",     # autres décarbonées
    "rgba(70, 110, 170, 0.95)",    # convertisseur
    "rgba(70, 150, 220, 0.95)",    # utile
    "rgba(170, 170, 170, 0.90)"    # inutile
]

link_colors = [
    "rgba(210, 40, 40, 0.55)",
    "rgba(120, 120, 120, 0.45)",
    "rgba(80, 150, 90, 0.45)",
    "rgba(70, 150, 220, 0.50)",
    "rgba(170, 170, 170, 0.50)"
]

fig = go.Figure(
    data=[
        go.Sankey(
            arrangement="snap",
            node=dict(
                pad=25,
                thickness=30,
                line=dict(width=0.8, color="rgba(80,80,80,0.6)"),
                label=labels,
                color=node_colors
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color=link_colors,
                hovertemplate="%{value:.1f} unités<extra></extra>"
            )
        )
    ]
)

fig.update_layout(
    title_text="Flux d’énergie associés aux usages sociétaux",
    font=dict(
        size=18,
        color="white",
        family="Arial"
    ),
    height=620,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------
# Lecture didactique
# ------------------------------------------------------------

st.markdown(
    """
    ### Lecture possible

    Dans cette version, le flux carboné n’est pas réglé directement par un curseur.
    Il est calculé comme ce qu’il reste à fournir une fois prises en compte les
    sources décarbonées mobilisées et le besoin total du système.

    Les élèves peuvent donc agir sur quatre leviers :

    - réduire la taille du convertisseur ;
    - réduire l’énergie inutile ;
    - augmenter le recours à l’uranium ;
    - augmenter le recours aux autres sources décarbonées.

    L’intérêt de la manipulation est de faire apparaître que la réduction du
    flux carboné peut résulter d’une combinaison de ces leviers, et pas seulement
    d’une substitution directe d’une source par une autre.
    """
)