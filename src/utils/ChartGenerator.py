import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import tempfile
from datetime import datetime



COLORS = {
    "Primary": "#2E86AB",
    "Secondary": "#06A77D",
    "Accent": "#F18F01",
    "Dark": "#1B263B",
    "Light": "#E8F4F8",
    "Success": "#06A77D",
    "Warning": "#F18F01",
}


def _setup_style():
    plt.style.use('dark_background')
    plt.rcParams['figure.facecolor'] = COLORS["Dark"]
    plt.rcParams['axes.facecolor'] = COLORS["Dark"]
    plt.rcParams['axes.edgecolor'] = COLORS["Light"]
    plt.rcParams['axes.labelcolor'] = COLORS["Light"]
    plt.rcParams['xtick.color'] = COLORS["Light"]
    plt.rcParams['ytick.color'] = COLORS["Light"]
    plt.rcParams['text.color'] = COLORS["Light"]
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.family'] = 'sans-serif'


def create_line_chart(data, title, xlabel, ylabel, save_path, dates=None):
    _setup_style() # configure graph to fit a certain pre-defined style
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLORS["Dark"])
    
    if dates:
        x_labels = [datetime.strptime(d[:10], "%Y-%m-%d").strftime("%m/%d") for d in dates]
        ax.plot(range(len(data)), data, color=COLORS["Secondary"], linewidth=2, marker='o', markersize=4)
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(x_labels, rotation=45, ha='right')
    else:
        ax.plot(data, color=COLORS["Secondary"], linewidth=2, marker='o', markersize=4)
    
    ax.set_title(title, color=COLORS["Light"], fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, color=COLORS["Light"], fontsize=11)
    ax.set_ylabel(ylabel, color=COLORS["Light"], fontsize=11)
    ax.grid(True, alpha=0.3, color=COLORS["Light"])
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=100, bbox_inches='tight', facecolor=COLORS["Dark"])
    plt.close()
    return save_path


def create_bar_chart(data_dict, title, xlabel, ylabel, save_path):
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLORS["Dark"])
    
    labels = list(data_dict.keys())
    values = list(data_dict.values())
    
    bars = ax.bar(labels, values, color=COLORS["Primary"], edgecolor=COLORS["Light"], linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', color=COLORS["Light"], fontweight='bold')
    
    ax.set_title(title, color=COLORS["Light"], fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, color=COLORS["Light"], fontsize=11)
    ax.set_ylabel(ylabel, color=COLORS["Light"], fontsize=11)
    ax.grid(True, alpha=0.3, color=COLORS["Light"], axis='y')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(save_path, dpi=100, bbox_inches='tight', facecolor=COLORS["Dark"])
    plt.close()
    return save_path


def create_pie_chart(data_dict, title, save_path):
    _setup_style()
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=COLORS["Dark"])
    
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())
    
    colors_list = [COLORS["Primary"], COLORS["Secondary"], COLORS["Accent"], COLORS["Success"]]
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                      colors=colors_list[:len(labels)],
                                      startangle=90, textprops={'color': COLORS["Light"], 'fontsize': 11})
    
    for autotext in autotexts:
        autotext.set_color(COLORS["Light"])
        autotext.set_fontweight('bold')
    
    ax.set_title(title, color=COLORS["Light"], fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=100, bbox_inches='tight', facecolor=COLORS["Dark"])
    plt.close()
    return save_path


def create_multi_line_chart(data_dict, title, xlabel, ylabel, save_path, dates=None):
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLORS["Dark"])
    
    colors_list = [COLORS["Secondary"], COLORS["Primary"], COLORS["Accent"], COLORS["Success"]]
    
    for idx, (series_name, data) in enumerate(data_dict.items()):
        color = colors_list[idx % len(colors_list)]
        if dates:
            x_labels = [datetime.strptime(d[:10], "%Y-%m-%d").strftime("%m/%d") for d in dates]
            ax.plot(range(len(data)), data, label=series_name, color=color, 
                   linewidth=2, marker='o', markersize=4)
            if idx == 0:  # Set x-axis labels only once
                ax.set_xticks(range(len(data)))
                ax.set_xticklabels(x_labels, rotation=45, ha='right')
        else:
            ax.plot(data, label=series_name, color=color, linewidth=2, marker='o', markersize=4)
    
    ax.set_title(title, color=COLORS["Light"], fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, color=COLORS["Light"], fontsize=11)
    ax.set_ylabel(ylabel, color=COLORS["Light"], fontsize=11)
    ax.legend(loc='best', facecolor=COLORS["Dark"], edgecolor=COLORS["Light"], 
             labelcolor=COLORS["Light"])
    ax.grid(True, alpha=0.3, color=COLORS["Light"])
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=100, bbox_inches='tight', facecolor=COLORS["Dark"])
    plt.close()
    return save_path


def get_temp_chart_path(filename):
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, f"organiseu_chart_{filename}.png")

