import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def analisy_univariate(data, features, histoplot=True, barplot=False, mean=None, text_y=0.5, outliers=False, kde=False, color=None, figsize=(24, 12)):
    num_features = len(features)
    num_rows = num_features // 3 + (num_features % 3 > 0)

    fig, axes = plt.subplots(num_rows, 3, figsize=figsize)

    for i, feature in enumerate(features):  
        row = i // 3
        col = i % 3

        ax = axes[row, col] if num_rows > 1 else axes[col]

        if barplot:
            if mean:
                data_grouped = data.groupby([feature])[[mean]].mean().reset_index()
                data_grouped[mean] = round(data_grouped[mean], 2)
                bars = ax.barh(y=data_grouped[feature], width=data_grouped[mean], color=color)
                for index, value in enumerate(data_grouped[mean]):
                    ax.text(value + text_y, index, f'{value: .1f}', va='center', fontsize=15)
            else:
                data_grouped = data.groupby([feature])[[feature]].count().rename(columns={feature: 'count'}).reset_index()
                data_grouped['pct'] = round(data_grouped['count'] / data_grouped['count'].sum() * 100, 2)
                bars = ax.barh(y=data_grouped[feature], width=data_grouped['pct'], color=color)
                for index, value in enumerate(data_grouped['pct']):
                    ax.text(value + text_y, index, f'{value:.1f}%', va='center', fontsize=15)

            ax.set_yticks(ticks=range(data_grouped[feature].nunique()), labels=data_grouped[feature].tolist(), fontsize=15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.grid(False)
            ax.get_xaxis().set_visible(False)

        elif outliers:
            sns.boxplot(data=data, x=feature, ax=ax, color=color)
        else:
            sns.histplot(data=data, x=feature, kde=kde, ax=ax, color=color, stat='percent')

        ax.set_title(feature)
        ax.set_xlabel('')

    if num_features < len(axes.flat):
        for j in range(num_features, len(axes.flat)):
            fig.delaxes(axes.flat[j])

    plt.tight_layout()
    return fig


def wo_discretize(df, var_discretize, target):
    # Concatenar as colunas relevantes
    df = pd.concat([df[var_discretize], target], axis=1)
    
    # Agrupar e calcular contagem e média
    df_count = df.groupby(df.columns[0], as_index=False)[df.columns[1]].count()
    df_mean = df.groupby(df.columns[0], as_index=False)[df.columns[1]].mean()
    
    # Concatenar os resultados
    df = pd.concat([df_count, df_mean[df_mean.columns[1]]], axis=1)
    
    # Renomear as colunas
    df.columns = [df.columns[0], 'n_obs', 'prop_good']
    
    # Calcular proporções e números
    df['prop_n_obs'] = df['n_obs'] / df['n_obs'].sum()
    df['n_good'] = df['prop_good'] * df['n_obs']
    df['n_bad'] = (1 - df['prop_good']) * df['n_obs']
    df['prop_n_good'] = df['n_good'] / df['n_good'].sum()
    df['prop_n_bad'] = df['n_bad'] / df['n_bad'].sum()
    
    # Calcular WoE (Weight of Evidence)
    df['woe'] = np.log(df['prop_n_good'] / df['prop_n_bad'])
    
    # Ordenar e resetar o índice
    df = df.sort_values(['woe']).reset_index(drop=True)
    
    # Calcular diferenças
    df['diff_prop_good'] = df['prop_good'].diff().abs()
    df['diff_woe'] = df['woe'].diff().abs()
    
    # Calcular IV (Information Value)
    df['iv'] = (df['prop_n_good'] - df['prop_n_bad']) * df['woe']
    df['total_iv'] = df['iv'].sum()
    
    return df

def plot_woe(df_woe, rotation_axis=0):
        x = np.array(df_woe.iloc[: , 0].apply(str))
        y = df_woe['woe']

        plt.figure(figsize = (18, 6))
        plt.plot(x, y, marker='o', linestyle='--', color = 'k')
        plt.xlabel(df_woe.columns[0])
        plt.ylabel('Peso das evidencias')
        plt.title(str('Peso das evidencas' + df_woe.columns[0]))
        plt.xticks(rotation = rotation_axis)