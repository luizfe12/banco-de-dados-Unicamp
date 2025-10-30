
# --- Célula 1: Importações Essenciais ---
import polars as pl
from plotnine import (
    ggplot, aes, geom_point, labs, theme_bw,
    scale_x_log10, scale_y_log10, facet_wrap,
    scale_color_brewer, facet_grid
)
from datetime import datetime
import warnings


print("Bibliotecas importadas com sucesso.")


# --- Célula 2: Carregamento dos Dados ---
# (Sem alterações)
# Importa o conjunto de dados 'diamonds' a partir da URL fornecida.
try:
    diamonds_pl = pl.read_csv("https://me315-unicamp.github.io/dados/diamonds.csv.gz")
    print(f"Dados carregados com sucesso. Total de linhas: {len(diamonds_pl)}")
except Exception as e:
    print(f"Erro ao carregar os dados: {e}")
    # Se o carregamento falhar, o script não continuará
    diamonds_pl = pl.DataFrame() # Cria um DataFrame vazio para evitar erros


# --- Célula 3: Preparação dos Dados (CORRIGIDA) ---
# O erro ocorreu aqui. A sintaxe 'pl.Categorical(categories=...)'
# não é a forma correta de definir o *tipo* para o 'cast'.
# Usamos 'pl.Enum(categories=...)' que define um tipo categórico
# que respeita a ordem física da lista fornecida.

if not diamonds_pl.is_empty():
    # Definindo a ordem lógica correta
    cut_order = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
    color_order = ['J', 'I', 'H', 'G', 'F', 'E', 'D'] # Do Pior (J) para o Melhor (D)
    clarity_order = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'] # Do Pior (I1) para o Melhor (IF)

    # *** LINHAS CORRIGIDAS ***
    # Aplicando a ordenação usando pl.Enum
    diamonds = diamonds_pl.with_columns([
        pl.col('cut').cast(pl.Enum(categories=cut_order)),
        pl.col('color').cast(pl.Enum(categories=color_order)),
        pl.col('clarity').cast(pl.Enum(categories=clarity_order))
    ])

    print("Variáveis categóricas ('cut', 'color', 'clarity') foram ordenadas (usando pl.Enum).")
    print(diamonds.head())
else:
    print("DataFrame vazio. Pulando preparação.")


# --- Célula 4: Atividade 2 - Associação entre 'carat' e 'price' ---
# (Sem alterações)

if not diamonds_pl.is_empty():
    print("\n--- Gerando Gráfico da Atividade 2 ---")
    
    # Criando a visualização
    p2 = (
        ggplot(diamonds, aes(x='carat', y='price'))
        
        # Ação 1: Usar 'alpha' (transparência)
        # Com 54.000 pontos, a sobreposição (overplotting) é severa.
        # 'alpha=0.05' torna os pontos transparentes, e áreas densas ficam mais escuras.
        + geom_point(alpha=0.05)
        
        # Ação 2: Usar escala logarítmica (log-log)
        # A relação parece exponencial. O log lineariza a relação,
        # facilitando a interpretação e "espalhando" os pontos que
        # estavam amassados no canto inferior esquerdo.
        + scale_x_log10(name="Peso (Carat) - Escala Log")
        + scale_y_log10(name="Preço (USD) - Escala Log")
        
        + labs(
            title="Relação entre Preço e Peso (Carat) dos Diamantes",
            caption="Gráfico em escala log-log com alpha=0.05 para reduzir overplotting."
        )
        + theme_bw() # Tema limpo (preto e branco)
    )

    # Exibe o gráfico
    print(p2)


    # --- Achados da Atividade 2 (Texto solicitado) ---
    # O texto abaixo é o parágrafo de achados solicitado na atividade
    print("""
    Achados (Atividade 2):
    Existe uma forte associação positiva entre o peso (carat) e o preço (price) do diamante: 
    quanto mais pesado, mais caro. Para garantir um gráfico de boa qualidade com 53.940 pontos, 
    duas ações principais foram tomadas: 1) Foi aplicado um baixo nível de transparência 
    (alpha=0.05) aos pontos, permitindo identificar áreas de alta densidade onde muitos 
    diamantes de preço e peso similares se acumulam. 2) Foi utilizada uma escala 
    logarítmica para ambos os eixos (log-log). Isso linearizou a relação (que originalmente 
    é exponencial) e expandiu a visualização dos dados no canto inferior esquerdo, que 
    estava severamente sobreposto. O gráfico em log-log revela uma clara tendência linear 
    positiva, embora com uma variabilidade (dispersão) considerável, indicando que, 
    embora o peso seja um preditor dominante do preço, outros fatores também 
    influenciam significativamente.
    """)


# --- Célula 5: Atividade 3 - Relação por 'cut' (Corte) ---
# (Sem alterações)

if not diamonds_pl.is_empty():
    print("\n--- Gerando Gráfico da Atividade 3 ---")

    # A melhor forma de comparar a relação entre subgrupos é usar "facetas"
    p3 = (
        ggplot(diamonds, aes(x='carat', y='price'))
        + geom_point(alpha=0.05) # Manter alpha baixo
        + scale_x_log10(name="Peso (Carat) - Escala Log")
        + scale_y_log10(name="Preço (USD) - Escala Log")
        
        # Ação: Usar 'facet_wrap' para criar um mini-gráfico para cada 'cut'.
        # A ordenação feita na Célula 3 garante que 'Fair' venha primeiro e 'Ideal' por último.
        + facet_wrap('~cut', ncol=3) 
        
        + labs(
            title="Relação Preço vs. Peso (Log-Log) por Qualidade de Corte (Cut)",
            subtitle="A relação positiva se mantém, mas a qualidade do corte eleva o preço."
        )
        + theme_bw()
    )

    # Exibe o gráfico
    print(p3)

    # --- Conclusão da Atividade 3 (Texto solicitado) ---
    # O texto abaixo é o parágrafo de conclusão solicitado na atividade
    print("""
    Conclusão (Atividade 3):
    Sim, a relação positiva fundamental entre peso e preço (em escala log-log) se 
    mantém em todos os cinco tipos de corte (cut). No entanto, a relação não é idêntica. 
    Observando os painéis lado a lado (graças ao 'facet_wrap'), fica claro que, para um 
    mesmo peso (carat), diamantes com cortes de melhor qualidade (como 'Premium' e 'Ideal') 
    tendem a ter preços mais altos do que diamantes com cortes de qualidade inferior 
    (como 'Fair' e 'Good'). Visualmente, a "nuvem" de pontos para 'Ideal' está 
    ligeiramente deslocada para cima em comparação com a nuvem de 'Fair', indicando 
    que a qualidade do corte atua como um multiplicador de valor.
    """)


# --- Célula 6: Atividade 4 - Relação por 'cut', 'color' e 'clarity' ---
# (Sem alterações)

if not diamonds_pl.is_empty():
    print("\n--- Gerando Gráfico da Atividade 4 ---")
    
    # Esta atividade é complexa devido à alta dimensionalidade (5 variáveis).
    # Abordagem: Filtrar para um 'cut' (ex: 'Ideal') e usar facetas para 'color'
    # e mapear 'clarity' para a cor dos pontos.
    
    diamonds_ideal = diamonds.filter(pl.col('cut') == 'Ideal')
    print(f"Filtrando dados. Usando apenas corte 'Ideal' ({len(diamonds_ideal)} linhas) para análise.")

    p4 = (
        ggplot(diamonds_ideal, aes(x='carat', y='price', color='clarity')) # 'clarity' mapeada para a cor
        + geom_point(alpha=0.4) # Alpha um pouco maior para a cor ser visível
        + scale_x_log10(name="Peso (Carat) - Escala Log")
        + scale_y_log10(name="Preço (USD) - Escala Log")
        
        # Facetas para 'color' (dentro do corte 'Ideal')
        + facet_wrap('~color', ncol=4) 
        
        + labs(
            title="Preço vs. Peso (Log-Log) para Diamantes de Corte 'Ideal'",
            subtitle="Facetado por Cor (J-D) e Colorido por Clareza (I1-IF)",
            color="Clareza (Clarity)"
        )
        # Usar uma escala de cores que funcione bem para variáveis ordinais
        # 'RdYlBu' (Vermelho-Amarelo-Azul) é boa para "pior" vs "melhor"
        + scale_color_brewer(type='div', palette='RdYlBu', direction=-1)
        # Ajustar o tamanho da legenda e tema
        + theme_bw() 
    )

    # Exibe o gráfico
    print(p4)

    # --- Análise da Atividade 4 (Texto solicitado) ---
    # O texto abaixo é a análise solicitada na atividade
    print("""
    Análise (Atividade 4):
    
    Dificuldades Encontradas: A principal dificuldade é a alta dimensionalidade dos dados. 
    Tentar visualizar 5 variáveis (2 numéricas e 3 categóricas) simultaneamente é um 
    desafio. Mapear 'carat' para X, 'price' para Y, e usar facetas para 'cut' (5 níveis), 
    'color' (7 níveis) e 'clarity' (8 níveis) exigiria 280 gráficos distintos, o que 
    é visualmente impraticável. A abordagem adotada foi filtrar os dados para um 
    único corte ('Ideal') e, em seguida, usar facetas para 'color' e mapear 'clarity' 
    para a cor dos pontos, tornando a análise viável.

    A Relação é a Mesma? Não. A relação base (preço sobe com o peso) é universal, 
    mas o *nível* dessa relação (o preço específico para um dado peso) muda 
    drasticamente dependendo das outras 3Cs. O gráfico demonstra que, mesmo dentro do 
    corte 'Ideal' e para uma 'Cor' específica (ex: painel 'G'), os diamantes com 
    melhor clareza (ex: 'IF', 'VVS1', em tons de azul) estão consistentemente na 
    parte superior da nuvem de pontos (preços mais altos), enquanto diamantes com 
    clareza inferior (ex: 'SI1', 'SI2', em tons de vermelho/laranja) estão na 
    parte inferior, para o *mesmo peso*. Portanto, a relação preço-peso é, na 
    verdade, uma "família" de relações paralelas (em escala log-log) onde os 
    interceptos são definidos pelas qualidades de 'cut', 'color' e 'clarity'.
    """)


# --- Célula 7: Hora de Execução ---
# (Sem alterações)
# Código para mostrar a hora em que foi gerado/executado

# Obtém a data e hora atuais
hora_atual = datetime.now()

# Mostra o resultado formatado
print(f"\n--- Fim do Script ---")
print(f"Este código foi executado em: {hora_atual.strftime('%Y-%m-%d %H:%M:%S')}")