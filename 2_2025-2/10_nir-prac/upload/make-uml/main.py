from graphviz import Digraph

dot = Digraph("UML Use Case")

dot.node("Dev", "Разработчик", shape="actor")
dot.node("AI", "AI (Cursor)", shape="actor")

dot.node("UC1", "Анализ кода")
dot.node("UC2", "Технический долг")
dot.node("UC3", "Рефакторинг предложения")
dot.node("UC4", "Рефакторинг")
dot.node("UC5", "Модернизация")
dot.node("UC6", "Генерация кода")
dot.node("UC7", "Проверка изменений")

dot.edges([
    ("Dev","UC1"),
    ("Dev","UC4"),
    ("Dev","UC5"),
    ("Dev","UC7"),

    ("AI","UC2"),
    ("AI","UC3"),
    ("AI","UC6"),
    ("AI","UC7"),

    ("UC1","UC2"),
    ("UC2","UC3"),
    ("UC3","UC4"),
    ("UC4","UC5"),
    ("UC5","UC7"),
])

dot.render("uml", format="png", cleanup=True)
