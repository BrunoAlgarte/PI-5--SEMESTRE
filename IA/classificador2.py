import pandas as pd

# Funções de pontuação específicas por posição na base (PG, SG, SF, PF, C)
#(PG, SG)
def pontuacao_armador(row):
    return (row['PPG'] * 0.25 +
            row['APG'] * 0.35 +
            row['PER'] * 0.15 +
            row['BPM'] * 0.10 +
            row['TS%'] * 0.10 -
            row['TPG'] * 0.05)

#Ala (SF, PF)
def pontuacao_ala(row):
    return (row['PPG'] * 0.3 +
            row['RPG'] * 0.2 +
            row['PER'] * 0.15 +
            row['BPM'] * 0.10 +
            row['SPG'] * 0.1 +
            row['BPG'] * 0.1 +
            row['FG%'] * 0.05)

#Pivô (C)
def pontuacao_pivo(row):
    return (row['RPG'] * 0.3 +
            row['BPG'] * 0.25 +
            row['PPG'] * 0.2 +
            row['PER'] * 0.1 +
            row['BPM'] * 0.1 +
            row['FG%'] * 0.05)

# Função para gerar a pontuação baseada na posição
def gerar_pontuacao(row):
    pos = row['Pos']
    if 'PG' in pos or 'SG' in pos:
        return pontuacao_armador(row)
    elif 'SF' in pos or 'PF' in pos:
        return pontuacao_ala(row)
    elif 'C' in pos:
        return pontuacao_pivo(row)
    else:
        return 0

# Função para gerar a classificação baseada no Score
def classificar_por_pontuacao(score):
    if score >= 20:
        return 'Superstar'
    elif score >= 15:
        return 'All-Star'
    elif score >= 10:
        return 'Role Player'
    else:
        return 'Reserva'

# Exemplo de uso
def classificar_jogador(stats):
    """
    Recebe um dicionário de estatísticas e retorna a classificação do jogador.
    """
    df = pd.DataFrame([stats])

    # Gerar o Score baseado na posição
    df['Score'] = df.apply(gerar_pontuacao, axis=1)

    # Classificar com base no Score
    df['Label'] = df['Score'].apply(classificar_por_pontuacao)

    return df[['Score', 'Label']]

# Exemplo de chamada:
exemplo_jogador = {
    'Pos': 'PG',  # posição
    'PPG': 25,    # pontos por jogo
    'APG': 8,     # assistências por jogo
    'RPG': 4,     # rebotes por jogo
    'BPG': 0.5,   # tocos por jogo
    'SPG': 1.5,   # roubos por jogo
    'TPG': 2.5,   # turnovers por jogo
    'PER': 24,    # eficiência
    'TS%': 0.58,  # aproveitamento real
    'BPM': 5,     # box plus-minus
    'FG%': 0.48   # aproveitamento de arremessos
}

resultado = classificar_jogador(exemplo_jogador)
print(resultado)
