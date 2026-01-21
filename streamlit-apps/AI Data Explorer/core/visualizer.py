import seaborn as sns
import matplotlib.pyplot as plt

def plot_numeric_distributions(df):
    #avoid too big text on the plots
    plt.rcParams.update({'font.size': 10})
    plots = []
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f'Distribution of {col}')
        plots.append(fig)
    return plots