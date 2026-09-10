"""Vẽ lại biểu đồ ablation từ kết quả trong reports/aspect_hybrid_ablation.csv.

Dùng chung phong cách với notebook 01 (seaborn whitegrid, màu #4C78A8, 300 dpi)
để các hình trong báo cáo đồng nhất.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS = PROJECT_ROOT / "reports" / "aspect_hybrid_ablation.csv"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
BAR_COLOR = "#4C78A8"
ORDER = [
    "Text-only",
    "Text + lexicon",
    "Text + aspect",
    "Text + lexicon + aspect",
    "Aspect ratings only",
]


def plot_macro_f1(results: pd.DataFrame) -> None:
    data = results.sort_values("macro_f1", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    sns.barplot(data=data, x="macro_f1", y="feature_group", color=BAR_COLOR, ax=ax)
    ax.errorbar(
        data["macro_f1"],
        range(len(data)),
        xerr=data["macro_f1_std"],
        fmt="none",
        color="black",
        capsize=4,
    )
    for position, value in enumerate(data["macro_f1"]):
        ax.annotate(
            f"{value:.4f}",
            (value, position),
            xytext=(8, 0),
            textcoords="offset points",
            va="center",
        )
    ax.set(
        title="Ablation nhóm đặc trưng bằng 5-fold CV trên tập phát triển",
        xlabel="Macro F1",
        ylabel="Nhóm đặc trưng",
        xlim=(0, 1),
    )
    fig.tight_layout()
    path = FIGURES_DIR / "eda_feature_ablation_cv.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Đã lưu: {path}")


def plot_per_class(results: pd.DataFrame) -> None:
    metrics = {
        "neutral_f1": "Neutral F1",
        "negative_recall": "Recall Negative",
        "macro_f1": "Macro F1",
    }
    long = (
        results.melt(
            id_vars="feature_group",
            value_vars=list(metrics),
            var_name="metric",
            value_name="score",
        )
        .assign(metric=lambda frame: frame["metric"].map(metrics))
    )
    fig, ax = plt.subplots(figsize=(10, 5.4))
    sns.barplot(
        data=long,
        x="metric",
        y="score",
        hue="feature_group",
        hue_order=ORDER,
        palette="Blues",
        ax=ax,
    )
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", fontsize=8, padding=2)
    ax.set(
        title="Chỉ số theo lớp thiểu số của từng nhóm đặc trưng (5-fold CV)",
        xlabel="",
        ylabel="Giá trị",
        ylim=(0, 1),
    )
    ax.legend(title="Nhóm đặc trưng", loc="upper left", fontsize=8, title_fontsize=9)
    fig.tight_layout()
    path = FIGURES_DIR / "eda_ablation_per_class.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Đã lưu: {path}")


def main() -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    results = pd.read_csv(RESULTS)
    plot_macro_f1(results)
    plot_per_class(results)


if __name__ == "__main__":
    main()
