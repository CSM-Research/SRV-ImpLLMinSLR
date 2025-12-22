import pandas as pd
import matplotlib.pyplot as plt

# Caminho para o arquivo Excel
file_path = "dataSynthesis-LLM4Novice.xlsx"

# Ler a planilha "RQ2"
df = pd.read_excel(file_path, sheet_name="Q6")

# Limpar e encurtar nomes das colunas
df.columns = [col.split('[')[-1].replace(']', '').strip() for col in df.columns]

# Traduzir respostas
translation_map = {
    "Já usei": "Have used",
    "Não usei": "Have not used",
    "Não sei o que é": "Don't know what it is"
}
df = df.replace(translation_map)

# Contagem das respostas
summary = df.apply(pd.Series.value_counts).T.fillna(0).astype(int)

# Remover a coluna "ID" (ou qualquer coluna sem relação)
summary = summary.drop(index=["ID"], errors="ignore")

# Garantir ordem de colunas
order = ["Have used", "Have not used", "Don't know what it is"]
summary = summary[[col for col in order if col in summary.columns]]

# Definir fonte e estilo em tons de cinza
plt.rcParams.update({
    "font.family": "Times New Roman",
    "text.color": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black"
})

# Tons de cinza bem contrastantes
grayscale_colors = ["#1a1a1a", "#808080", "#e0e0e0"]

# Criar gráfico de barras empilhadas
ax = summary.plot(
    kind="barh",
    stacked=True,
    figsize=(12, 10),
    color=grayscale_colors,
    edgecolor="black"
)

# Aplicar padrões (hatching)
#hatches = ['////', '\\\\\\\\', '....']
#for bars, hatch in zip(ax.containers, hatches):
#    for bar in bars:
#        bar.set_hatch(hatch)

# Inverter a ordem dos itens no eixo Y
ax.invert_yaxis()

# Personalizar o gráfico
plt.xlabel("Number of participants", fontsize=14)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=20)

# Legenda horizontal abaixo do gráfico
plt.legend(
    title="Legend",
    loc="upper center",
    bbox_to_anchor=(0.5, -0.08),
    ncol=3,
    fontsize=18,
    title_fontsize=15,
    frameon=False
)

plt.tight_layout()
plt.show()
