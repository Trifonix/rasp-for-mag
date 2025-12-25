import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def draw_box(ax, center, text, width=2.0, height=0.6, fc="#D6EAF8", fontsize=12):
    x, y = center
    box = FancyBboxPatch(
        (x - width/2, y - height/2),
        width, height,
        boxstyle="round,pad=0.03,rounding_size=0.1",
        linewidth=1.2,
        edgecolor="black",
        facecolor=fc
    )
    ax.add_patch(box)
    ax.text(
        x, y, text,
        ha="center", va="center",
        fontsize=fontsize,
        wrap=True
    )
    return {"x": x, "y": y, "w": width, "h": height}

def connect(ax, a, b):
    x1, y1 = a["x"], a["y"] - a["h"]/2
    x2, y2 = b["x"], b["y"] + b["h"]/2
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1.2,
            shrinkA=6,
            shrinkB=6
        )
    )

def draw_publishing_architecture():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)

    # Настройки
    layer_spacing = 1.0  # вертикальные отступы между слоями
    fontsize = 6
    box_w = 1.8
    box_h = 0.6

    # Верхний слой
    y_top = 3.8
    author = draw_box(ax, (0, y_top), "Автор", width=box_w, height=box_h, fc="#FADBD8", fontsize=fontsize)
    editor = draw_box(ax, (3.5, y_top), "Редактор", width=box_w, height=box_h, fc="#FADBD8", fontsize=fontsize)
    admin = draw_box(ax, (7, y_top), "Администратор", width=box_w, height=box_h, fc="#FADBD8", fontsize=fontsize)

    # Нижние слои
    y_ui = y_top - layer_spacing
    ui = draw_box(ax, (3.5, y_ui), "Пользовательский интерфейс\n(Web UI)", width=box_w, height=box_h, fc="#D6EAF8", fontsize=fontsize)

    y_bl = y_ui - layer_spacing
    bl = draw_box(ax, (3.5, y_bl),
                  "Бизнес-логика\n• Рукописи\n• Редактирование\n• Публикации\n• Печать",
                  width=box_w, height=box_h, fc="#D5F5E3", fontsize=fontsize)

    y_db = y_bl - layer_spacing
    db = draw_box(ax, (3.5, y_db), "База данных\n• Авторы\n• Книги\n• Заказы", width=box_w, height=box_h, fc="#E5E7E9", fontsize=fontsize)

    # Связи
    for u in [author, editor, admin]:
        connect(ax, u, ui)
    connect(ax, ui, bl)
    connect(ax, bl, db)

    ax.set_title("Архитектура программного средства «Издательство»", fontsize=16)
    ax.set_xlim(-1, 8)
    ax.set_ylim(0, 5)
    ax.axis("off")

    plt.savefig("publishing_architecture.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Диаграмма сохранена: publishing_architecture.png")

if __name__ == "__main__":
    draw_publishing_architecture()
