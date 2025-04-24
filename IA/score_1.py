import pandas as pd

df = pd.read_csv("seasons_stats.csv", encoding='ISO-8859-1')

# Filtrar dados a partir de 1990
df_filtered = df[df['Year'] >= 1990].copy()

# Evitar divisões por zero
df_filtered = df_filtered[df_filtered['G'] > 0]

# Criar estatísticas por jogo
df_filtered['PPG'] = df_filtered['PTS'] / df_filtered['G']
df_filtered['APG'] = df_filtered['AST'] / df_filtered['G']
df_filtered['RPG'] = df_filtered['TRB'] / df_filtered['G']
df_filtered['BPG'] = df_filtered['BLK'] / df_filtered['G']
df_filtered['SPG'] = df_filtered['STL'] / df_filtered['G']
df_filtered['TPG'] = df_filtered['TOV'] / df_filtered['G']

selected_columns = [
    'Player', 'Year', 'Pos', 'G', 'MP',
    'PPG', 'APG', 'RPG', 'BPG', 'SPG', 'TPG',
    'PER', 'TS%', 'BPM',
    '3PAr', 'TRB', 'TRB%', 'ORB', 'DRB',
    'AST', 'AST%', 'STL', 'STL%',
    'BLK', 'BLK%', 'FG%', 'eFG%', 'FT%'
]

df_features = df_filtered[selected_columns].copy()

def pontuacao_armador(row):
    return (row['PPG'] * 0.25 +
            row['APG'] * 0.35 +
            row['PER'] * 0.15 +
            row['BPM'] * 0.10 +
            row['TS%'] * 0.10 -
            row['TPG'] * 0.05)

def pontuacao_ala(row):
    return (row['PPG'] * 0.3 +
            row['RPG'] * 0.2 +
            row['PER'] * 0.15 +
            row['BPM'] * 0.10 +
            row['SPG'] * 0.1 +
            row['BPG'] * 0.1 +
            row['FG%'] * 0.05)

def pontuacao_pivo(row):
    return (row['RPG'] * 0.3 +
            row['BPG'] * 0.25 +
            row['PPG'] * 0.2 +
            row['PER'] * 0.1 +
            row['BPM'] * 0.1 +
            row['FG%'] * 0.05)

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

def classificar_por_pontuacao(score):
    if score >= 20:
        return 'Superstar'
    elif score >= 15:
        return 'All-Star'
    elif score >= 10:
        return 'Role Player'
    else:
        return 'Reserva'

# Gerar a pontuação com base na posição
df_features['Score'] = df_features.apply(gerar_pontuacao, axis=1)

# Aplicar a classificação final
df_features['Label'] = df_features['Score'].apply(classificar_por_pontuacao)

# Separar os dados de entrada (X) e saída (y)
X = df_features.drop(columns=['Player', 'Year', 'Pos', 'Label', 'Score'])
y = df_features['Label']

X = X.fillna(0)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

from sklearn.ensemble import RandomForestClassifier

# Criar o modelo
model = RandomForestClassifier(class_weight='balanced', random_state=42)

# Treinar o modelo
model.fit(X_train, y_train)

from sklearn.metrics import classification_report, confusion_matrix

# Fazer previsões
y_pred = model.predict(X_test)

# Relatório de desempenho
print("Relatório de Classificação:\n")
print(classification_report(y_test, y_pred))

# Matriz de confusão
print("Matriz de Confusão:\n")
print(confusion_matrix(y_test, y_pred))

df_features.to_csv("nba_classificada.csv", index=False)