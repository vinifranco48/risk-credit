import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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