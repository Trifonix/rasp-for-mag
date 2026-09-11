"""Анализ тренировок и питания из dolgator-import.json."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

DATA_PATH = Path(__file__).parent / "dolgator-import.json"
EXERCISE_NAMES = ("Приседания", "Отжимания", "Подтягивания")

COLORS = {
    "bg": "#f4f6f8",
    "card": "#ffffff",
    "border": "#dce3ea",
    "text": "#1c2430",
    "muted": "#5c6b7a",
    "grid": "#e8edf2",
    "green": "#1f8a5b",
    "green_soft": "rgba(31, 138, 91, 0.22)",
    "blue": "#2f6fed",
    "orange": "#c2410c",
    "orange_soft": "rgba(194, 65, 12, 0.9)",
}
EX_COLORS = [COLORS["green"], COLORS["blue"], COLORS["orange"]]
PLOTLY_CFG = {"displayModeBar": False, "responsive": True}


def load_data(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def build_frames(raw: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    day_rows: list[dict] = []
    meal_rows: list[dict] = []
    set_rows: list[dict] = []

    for date_str, day in sorted(raw.get("days", {}).items()):
        meals = day.get("meals") or []
        exercises = day.get("exercises") or []
        total_grams = sum(meals)
        meal_count = len(meals)
        workout = any(ex for ex in exercises)
        total_reps = sum(sum(ex) for ex in exercises if ex)
        total_sets = sum(len(ex) for ex in exercises if ex)

        day_rows.append(
            {
                "date": pd.to_datetime(date_str),
                "label": pd.to_datetime(date_str).strftime("%d.%m"),
                "total_grams": total_grams,
                "meal_count": meal_count,
                "avg_portion": total_grams / meal_count if meal_count else 0,
                "workout": workout,
                "total_reps": total_reps,
                "total_sets": total_sets,
            }
        )
        for i, grams in enumerate(meals, start=1):
            meal_rows.append(
                {"date": pd.to_datetime(date_str), "label": pd.to_datetime(date_str).strftime("%d.%m"), "meal_n": i, "grams": grams}
            )
        for ex_i, sets in enumerate(exercises):
            name = EXERCISE_NAMES[ex_i] if ex_i < len(EXERCISE_NAMES) else f"Упражнение {ex_i + 1}"
            for set_i, reps in enumerate(sets, start=1):
                set_rows.append(
                    {
                        "date": pd.to_datetime(date_str),
                        "label": pd.to_datetime(date_str).strftime("%d.%m"),
                        "exercise": name,
                        "set_n": set_i,
                        "reps": reps,
                    }
                )

    return pd.DataFrame(day_rows), pd.DataFrame(meal_rows), pd.DataFrame(set_rows)


def linear_trend(y: pd.Series) -> np.ndarray:
    """Линейный тренд по индексу 0..n-1."""
    y = y.astype(float)
    if len(y) < 2 or y.isna().all():
        return y.to_numpy()
    x = np.arange(len(y), dtype=float)
    mask = ~y.isna().to_numpy()
    if mask.sum() < 2:
        return np.full(len(y), np.nan)
    coef = np.polyfit(x[mask], y.to_numpy()[mask], 1)
    return np.polyval(coef, x)


def pct_change(first: float, last: float) -> float | None:
    if first == 0:
        return None
    return (last - first) / abs(first) * 100


def apply_theme(fig: go.Figure, height: int) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=COLORS["card"],
        font=dict(family="Segoe UI, Arial, sans-serif", color=COLORS["text"], size=11),
        title=dict(font=dict(size=13, color=COLORS["text"]), x=0, xanchor="left", pad=dict(t=0, b=0)),
        margin=dict(l=42, r=42, t=28, b=28),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="left",
            x=0,
            font=dict(size=10),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            gridcolor=COLORS["grid"],
            zeroline=False,
            linecolor=COLORS["border"],
            tickfont=dict(size=10, color=COLORS["muted"]),
            title=dict(text="", font=dict(size=10)),
            type="category",
        ),
        yaxis=dict(
            gridcolor=COLORS["grid"],
            zeroline=False,
            linecolor=COLORS["border"],
            tickfont=dict(size=10, color=COLORS["muted"]),
            title=dict(font=dict(size=10, color=COLORS["muted"])),
        ),
    )
    return fig


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{ background: {COLORS["bg"]}; color: {COLORS["text"]}; }}
        .block-container {{
            padding: 0.55rem 1rem 0.4rem 1rem !important;
            max-width: 1200px;
        }}
        [data-testid="stSidebar"] {{
            background: {COLORS["card"]};
            border-right: 1px solid {COLORS["border"]};
        }}
        [data-testid="stSidebar"] .block-container {{ padding-top: 0.7rem !important; }}
        header[data-testid="stHeader"] {{ background: transparent; height: 0; }}
        .page-head {{
            display: flex; align-items: baseline; justify-content: space-between;
            gap: 0.75rem; margin: 0 0 0.45rem 0; padding-bottom: 0.35rem;
            border-bottom: 1px solid {COLORS["border"]};
        }}
        .page-head h1 {{
            margin: 0; font-size: 1.15rem; font-weight: 700; color: {COLORS["text"]};
        }}
        .page-head p {{ margin: 0; color: {COLORS["muted"]}; font-size: 0.8rem; }}
        .insight {{
            margin: 0 0 0.45rem 0; padding: 0.35rem 0.6rem;
            background: {COLORS["card"]}; border: 1px solid {COLORS["border"]};
            border-radius: 6px; font-size: 0.82rem; color: {COLORS["text"]};
        }}
        .insight b.down {{ color: {COLORS["green"]}; }}
        .insight b.up {{ color: {COLORS["orange"]}; }}
        div[data-testid="stMetric"] {{
            background: {COLORS["card"]}; border: 1px solid {COLORS["border"]};
            border-radius: 6px; padding: 0.3rem 0.55rem 0.25rem 0.55rem;
        }}
        div[data-testid="stMetric"] label {{
            color: {COLORS["muted"]} !important; font-size: 0.72rem !important;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            font-size: 1.1rem; font-weight: 700; color: {COLORS["text"]} !important;
        }}
        div[data-testid="stHorizontalBlock"] {{ gap: 0.4rem; }}
        .stTabs [data-baseweb="tab-list"] {{ gap: 0; border-bottom: 1px solid {COLORS["border"]}; }}
        .stTabs [data-baseweb="tab"] {{
            padding: 0.25rem 0.7rem; font-size: 0.88rem; font-weight: 600; color: {COLORS["muted"]};
        }}
        .stTabs [aria-selected="true"] {{ color: {COLORS["text"]} !important; }}
        div[data-testid="stVerticalBlock"] > div {{ gap: 0.35rem; }}
        [data-testid="stSidebar"] h3 {{ font-size: 0.9rem; margin: 0 0 0.3rem 0; }}
        hr {{ margin: 0.5rem 0; border-color: {COLORS["border"]}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def dynamics_chart(d: pd.DataFrame) -> go.Figure:
    """Главный график: снижение еды + рост повторов."""
    labels = d["label"].tolist()
    food = d["total_grams"]
    food_trend = linear_trend(food)

    # Повторы только в дни тренировок — иначе линия «падает в ноль» и тренд нечитаем
    reps = d["total_reps"].where(d["workout"])
    workout = d[d["workout"]].copy()
    if len(workout) >= 2:
        reps_trend_on_w = linear_trend(workout["total_reps"])
        # растянуть тренд на все дни через интерполяцию по датам тренировок
        reps_trend = np.interp(
            np.arange(len(d)),
            np.where(d["workout"].to_numpy())[0],
            reps_trend_on_w,
        )
    else:
        reps_trend = np.full(len(d), np.nan)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=labels,
            y=food,
            name="Питание за день, г",
            marker_color=COLORS["green_soft"],
            marker_line=dict(width=0),
            hovertemplate="%{x}<br>Питание: %{y:.0f} г<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=food_trend,
            name="Тренд питания ↓",
            mode="lines",
            line=dict(color=COLORS["green"], width=3, dash="solid"),
            hovertemplate="%{x}<br>Тренд питания: %{y:.0f} г<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=reps,
            name="Повторы (дни тренировок)",
            mode="markers+lines",
            connectgaps=True,
            line=dict(color=COLORS["orange"], width=2),
            marker=dict(size=8, color=COLORS["orange"]),
            hovertemplate="%{x}<br>Повторы: %{y:.0f}<extra></extra>",
        ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=reps_trend,
            name="Тренд повторов ↑",
            mode="lines",
            line=dict(color=COLORS["orange"], width=3, dash="dot"),
            hovertemplate="%{x}<br>Тренд повторов: %{y:.0f}<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.update_yaxes(title_text="Питание, г", secondary_y=False, showgrid=True)
    fig.update_yaxes(title_text="Повторы", secondary_y=True, showgrid=False)
    fig.update_layout(title_text="Динамика: питание ↓ · повторы ↑", bargap=0.25)
    apply_theme(fig, height=360)
    fig.update_layout(margin=dict(l=46, r=46, t=30, b=52))
    return fig


def main() -> None:
    st.set_page_config(
        page_title="Тренировки и питание",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    if not DATA_PATH.exists():
        st.error(f"Файл не найден: `{DATA_PATH.name}`")
        st.stop()

    raw = load_data(DATA_PATH)
    days_df, meals_df, sets_df = build_frames(raw)
    if days_df.empty:
        st.warning("В JSON нет дней с данными.")
        st.stop()

    st.markdown(
        """
        <div class="page-head">
          <h1>Тренировки и питание</h1>
          <p>Динамика питания и нагрузки</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### Фильтры")
        min_d, max_d = days_df["date"].min().date(), days_df["date"].max().date()
        date_range = st.date_input(
            "Период",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            format="DD.MM.YYYY",
        )
        show_workout_only = st.checkbox("Только дни с тренировкой", value=False)
        st.markdown("---")
        st.caption(f"Источник: `{DATA_PATH.name}`")
        st.caption(f"Дней в файле: **{len(days_df)}**")

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
    else:
        start, end = min_d, max_d

    mask = (days_df["date"].dt.date >= start) & (days_df["date"].dt.date <= end)
    d = days_df.loc[mask].copy().reset_index(drop=True)
    if show_workout_only:
        d = d[d["workout"]].reset_index(drop=True)

    m = meals_df[
        (meals_df["date"].dt.date >= start) & (meals_df["date"].dt.date <= end)
    ].copy()
    s = sets_df[
        (sets_df["date"].dt.date >= start) & (sets_df["date"].dt.date <= end)
    ].copy()

    if d.empty:
        st.info("Нет данных за выбранный период.")
        st.stop()

    workout_days = int(d["workout"].sum())
    avg_grams = float(d["total_grams"].mean())
    total_reps = int(d["total_reps"].sum())

    food_start, food_end = float(d["total_grams"].iloc[0]), float(d["total_grams"].iloc[-1])
    food_trend_vals = linear_trend(d["total_grams"])
    food_pct = pct_change(float(food_trend_vals[0]), float(food_trend_vals[-1]))

    w = d[d["workout"]]
    if len(w) >= 2:
        reps_trend_w = linear_trend(w["total_reps"])
        reps_pct = pct_change(float(reps_trend_w[0]), float(reps_trend_w[-1]))
    else:
        reps_pct = None

    food_txt = f"{food_pct:+.0f}%" if food_pct is not None else "—"
    reps_txt = f"{reps_pct:+.0f}%" if reps_pct is not None else "—"

    st.markdown(
        f"""
        <div class="insight">
          По тренду за период:
          питание <b class="down">{food_txt}</b>
          · повторы на тренировках <b class="up">{reps_txt}</b>
          · факт: первый день {food_start:.0f} г → последний {food_end:.0f} г
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4, gap="small")
    c1.metric("Дней", len(d))
    c2.metric("Тренировок", workout_days)
    c3.metric("Среднее питание", f"{avg_grams:.0f} г")
    c4.metric("Всего повторов", total_reps)

    tab_overview, tab_food, tab_train, tab_raw = st.tabs(
        ["Обзор", "Питание", "Тренировки", "Таблица"]
    )

    with tab_overview:
        st.plotly_chart(dynamics_chart(d), width="stretch", config=PLOTLY_CFG)

    with tab_food:
        fig_food = go.Figure()
        fig_food.add_trace(
            go.Scatter(
                x=d["label"],
                y=d["total_grams"],
                fill="tozeroy",
                name="Сумма за день, г",
                line=dict(color=COLORS["green"], width=2),
                fillcolor=COLORS["green_soft"],
                hovertemplate="%{x}: %{y:.0f} г<extra></extra>",
            )
        )
        fig_food.add_trace(
            go.Scatter(
                x=d["label"],
                y=linear_trend(d["total_grams"]),
                name="Тренд питания",
                mode="lines",
                line=dict(color=COLORS["blue"], width=2, dash="dash"),
            )
        )
        fig_food.add_trace(
            go.Bar(
                x=d["label"],
                y=d["meal_count"],
                name="Число порций",
                marker_color=COLORS["blue"],
                opacity=0.35,
                yaxis="y2",
                hovertemplate="%{x}: %{y} порц.<extra></extra>",
            )
        )
        fig_food.update_layout(
            title_text="Питание по дням",
            yaxis=dict(title="Граммы"),
            yaxis2=dict(title="Порции", overlaying="y", side="right", showgrid=False),
            bargap=0.3,
        )
        apply_theme(fig_food, height=300)
        fig_food.update_layout(margin=dict(l=42, r=42, t=28, b=52))
        st.plotly_chart(fig_food, width="stretch", config=PLOTLY_CFG)

        if not m.empty:
            left, right = st.columns(2, gap="small")
            with left:
                fig_box = px.box(
                    m,
                    x="label",
                    y="grams",
                    points="all",
                    color_discrete_sequence=[COLORS["orange"]],
                    labels={"label": "День", "grams": "Порция, г"},
                    title="Разброс порций",
                )
                apply_theme(fig_box, height=240)
                st.plotly_chart(fig_box, width="stretch", config=PLOTLY_CFG)
            with right:
                fig_hist = go.Figure(
                    data=[
                        go.Histogram(
                            x=m["grams"],
                            nbinsx=16,
                            marker_color=COLORS["blue"],
                            name="Порции",
                            hovertemplate="Порция: %{x} г<br>Количество: %{y}<extra></extra>",
                        )
                    ]
                )
                fig_hist.update_layout(
                    title_text="Распределение порций",
                    xaxis_title="Порция, г",
                    yaxis_title="Количество",
                )
                apply_theme(fig_hist, height=240)
                st.plotly_chart(fig_hist, width="stretch", config=PLOTLY_CFG)

    with tab_train:
        if s.empty:
            st.info("В выбранном периоде нет записанных подходов.")
        else:
            vol = (
                s.groupby(["label", "exercise", "date"], as_index=False)["reps"]
                .sum()
                .sort_values("date")
            )
            fig_vol = px.bar(
                vol,
                x="label",
                y="reps",
                color="exercise",
                barmode="stack",
                color_discrete_sequence=EX_COLORS,
                labels={"reps": "Повторы", "label": "Дата", "exercise": "Упражнение"},
                title="Объём повторов по упражнениям",
                category_orders={"label": d["label"].tolist()},
            )
            apply_theme(fig_vol, height=260)
            fig_vol.update_layout(margin=dict(l=42, r=20, t=28, b=52))
            st.plotly_chart(fig_vol, width="stretch", config=PLOTLY_CFG)

            prog = (
                s.groupby(["label", "exercise", "date"], as_index=False)["reps"]
                .sum()
                .sort_values("date")
            )
            fig_prog = px.line(
                prog,
                x="label",
                y="reps",
                color="exercise",
                markers=True,
                color_discrete_sequence=EX_COLORS,
                labels={"reps": "Повторы за день", "label": "Дата", "exercise": "Упражнение"},
                title="Прогресс по упражнениям",
                category_orders={"label": sorted(prog["label"].unique(), key=lambda x: prog.loc[prog["label"] == x, "date"].iloc[0])},
            )
            # порядок дат по календарю
            order = prog.drop_duplicates("label").sort_values("date")["label"].tolist()
            fig_prog.update_xaxes(categoryorder="array", categoryarray=order)
            apply_theme(fig_prog, height=240)
            fig_prog.update_layout(margin=dict(l=42, r=20, t=28, b=52))
            st.plotly_chart(fig_prog, width="stretch", config=PLOTLY_CFG)

            st.markdown("**Детализация подходов**")
            ex_pick = st.selectbox("Упражнение", list(EXERCISE_NAMES))
            detail = s[s["exercise"] == ex_pick]
            if detail.empty:
                st.caption("Нет данных по этому упражнению.")
            else:
                heat = detail.pivot_table(
                    index=detail["label"],
                    columns="set_n",
                    values="reps",
                    aggfunc="first",
                )
                # сортировка строк по дате
                order_idx = (
                    detail.drop_duplicates("label")
                    .sort_values("date")["label"]
                    .tolist()
                )
                heat = heat.reindex(order_idx)
                fig_heat = go.Figure(
                    data=go.Heatmap(
                        z=heat.values,
                        x=[f"Подход {c}" for c in heat.columns],
                        y=heat.index,
                        colorscale=[[0, "#f1f5f9"], [0.5, "#93c5fd"], [1, COLORS["green"]]],
                        colorbar=dict(title="Повторы"),
                        text=heat.values,
                        texttemplate="%{text}",
                        hovertemplate="%{y}<br>%{x}: %{z}<extra></extra>",
                    )
                )
                fig_heat.update_layout(
                    title_text=f"Матрица подходов — {ex_pick}",
                    yaxis=dict(autorange="reversed", title="Дата"),
                    xaxis=dict(title=""),
                )
                apply_theme(fig_heat, height=max(200, 28 * len(heat) + 80))
                st.plotly_chart(fig_heat, width="stretch", config=PLOTLY_CFG)

    with tab_raw:
        view = d.copy()
        view["date"] = view["date"].dt.strftime("%d.%m.%Y")
        view["workout"] = view["workout"].map({True: "да", False: "нет"})
        view = view.rename(
            columns={
                "date": "Дата",
                "total_grams": "Еда, г",
                "meal_count": "Порций",
                "avg_portion": "Ср. порция",
                "workout": "Тренировка",
                "total_reps": "Повторы",
                "total_sets": "Подходы",
            }
        )
        view["Ср. порция"] = view["Ср. порция"].round(0).astype(int)
        st.dataframe(
            view[["Дата", "Еда, г", "Порций", "Ср. порция", "Тренировка", "Повторы", "Подходы"]],
            width="stretch",
            hide_index=True,
            height=280,
        )

        if not s.empty:
            st.markdown("**Подходы**")
            sv = s.copy()
            sv["date"] = sv["date"].dt.strftime("%d.%m.%Y")
            st.dataframe(
                sv.rename(
                    columns={
                        "date": "Дата",
                        "exercise": "Упражнение",
                        "set_n": "Подход",
                        "reps": "Повторы",
                    }
                )[["Дата", "Упражнение", "Подход", "Повторы"]],
                width="stretch",
                hide_index=True,
                height=220,
            )


if __name__ == "__main__":
    main()
