import pandas as pd
import matplotlib.pyplot as plt
import re

# === Parâmetros de estilo ===
FONT_FAMILY = "Times New Roman"
FONT_TITLE = 15
FONT_AXIS_LABEL = 20
FONT_TICK = 18
FONT_BUBBLE_TEXT = 15

plt.rcParams["font.family"] = FONT_FAMILY
plt.rcParams["axes.unicode_minus"] = False

# === Ler dados ===
df = pd.read_excel("dataSynthesis-LLM4Novice.xlsx", sheet_name="Q1-Q4")

# Corrigir valores não numéricos
df["number-of-reviews"] = df["number-of-reviews"].replace({">= 3": 4}).astype(int)

# === Categorizar ===
def categorize_reviews(x):
    if x == 0:
        return "None"
    elif x == 1:
        return "1"
    elif x == 2:
        return "2"
    elif x == 3:
        return "3"
    else:
        return "more than 3"

df["review-category"] = df["number-of-reviews"].apply(categorize_reviews)

# === Ordenar IDs ===
def sort_participants(ids):
    def extract_number(pid):
        match = re.search(r'\d+', str(pid))
        return int(match.group()) if match else 0
    ids_sorted = sorted(ids, key=extract_number)
    return ", ".join(ids_sorted)

# === Agrupar ===
grouped = (
    df.groupby(["area-of-expertise", "review-category"])
    .agg({
        "Participant ID": lambda x: sort_participants(list(x)),
        "participant-name": "count"
    })
    .reset_index()
    .rename(columns={"participant-name": "count"})
)

# === Ordem personalizada ===
order = ["None", "1", "2", "3", "more than 3"]
grouped["review-category"] = pd.Categorical(grouped["review-category"], categories=order, ordered=True)
grouped = grouped.sort_values("review-category")

# === Criar gráfico ===
plt.figure(figsize=(10, 6))

# 👇 garantir bolhas visíveis mesmo com count = 1
sizes = grouped["count"].clip(lower=1) * 800

plt.scatter(
    grouped["review-category"],
    grouped["area-of-expertise"],
    s=sizes,
    alpha=0.4,
    color="lightgray",
    edgecolor="black",
    linewidth=1
)

# === Adicionar texto dentro das bolhas ===
for _, row in grouped.iterrows():
    plt.text(
        row["review-category"],
        row["area-of-expertise"],
        row["Participant ID"],
        ha="center", va="center",
        fontsize=FONT_BUBBLE_TEXT,
        color="black",
        fontweight="medium"
    )

# === Aparência geral ===
plt.xlabel("Number of Reviews", fontsize=FONT_AXIS_LABEL)
plt.ylabel("Expertise Area", fontsize=FONT_AXIS_LABEL)
plt.xticks(order, rotation=30, ha="right", color="black", fontsize=FONT_TICK)
plt.yticks(color="black", fontsize=FONT_TICK)

# === Linhas de grade e estilo ===
plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.4, color='lightgray')
plt.minorticks_on()
plt.grid(True, which='minor', axis='both', linestyle=':', linewidth=0.3, color='lightgray')

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_color('black')
plt.gca().spines['bottom'].set_color('black')

plt.margins(x=0.1, y=0.2)
plt.tight_layout()
plt.show()
