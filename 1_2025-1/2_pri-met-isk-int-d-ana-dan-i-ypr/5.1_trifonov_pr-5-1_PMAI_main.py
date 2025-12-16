'''
Дисциплина: Применение методов искусственного интеллекта в анализе данных и управлении
Практическое занятие 5.1
Обобщение, недообучение и переобучение
Выполнил: Дмитрий Трифонов, 1 курс, 12-25 РПм, Программная инженерия
Дата выполнения: 15.12.2025 в 10:02
'''

# pip install tensorflow

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import models, layers, regularizers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import LeakyReLU

# -------------------------------
# 1. Загрузка и подготовка данных
# -------------------------------
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

x_train = x_train.reshape((-1, 28, 28, 1))
x_test = x_test.reshape((-1, 28, 28, 1))

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Для исследовательского задания №2 (10% данных)
def get_small_train_set(x, y, frac=0.1, seed=42):
    np.random.seed(seed)
    idx = np.random.permutation(len(x))[:int(len(x)*frac)]
    return x[idx], y[idx]

# Универсальная функция обучения и отображения графиков
def train_and_plot(model, x, y, title, epochs=25, batch_size=64, early_stop=False):
    callbacks = []
    if early_stop:
        callbacks.append(EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True))

    history = model.fit(
        x, y,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        callbacks=callbacks,
        verbose=1
    )

    plt.figure()
    plt.plot(history.history['loss'], label='train loss')
    plt.plot(history.history['val_loss'], label='val loss')
    plt.legend()
    plt.title(title)
    plt.show()

    return history

# -------------------------------
# 2. Малая модель (недообучение)
# -------------------------------
model_small = models.Sequential([
    layers.Flatten(input_shape=(28,28,1)),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
model_small.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history_small = train_and_plot(
    model_small, x_train, y_train,
    title='Small model (7 epochs)', epochs=7, batch_size=64
)

# Эксперимент №7: обучение малой модели 30 эпох
history_small_30 = train_and_plot(
    model_small, x_train, y_train,
    title='Small model (30 epochs)', epochs=30, batch_size=64
)

# -------------------------------
# 3. Большая модель (переобучение)
# -------------------------------
model_big = models.Sequential([
    layers.Flatten(input_shape=(28,28,1)),
    layers.Dense(256, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
model_big.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history_big = train_and_plot(
    model_big, x_train, y_train,
    title='Big model (25 epochs)', epochs=25, batch_size=64
)

# -------------------------------
# 4. Регуляризация (Dropout + L2)
# -------------------------------
model_reg = models.Sequential([
    layers.Flatten(input_shape=(28,28,1)),
    layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.Dropout(0.3),
    layers.Dense(10, activation='softmax')
])
model_reg.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history_reg = train_and_plot(
    model_reg, x_train, y_train,
    title='Regularized model', epochs=25, batch_size=64
)

# -------------------------------
# 5. Dropout = 0.7
# -------------------------------
model_reg_high_dropout = models.Sequential([
    layers.Flatten(input_shape=(28,28,1)),
    layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.Dropout(0.7),
    layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.Dropout(0.7),
    layers.Dense(10, activation='softmax')
])
model_reg_high_dropout.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

train_and_plot(
    model_reg_high_dropout, x_train, y_train,
    title='Regularized model (Dropout 0.7)', epochs=25, batch_size=64
)

# -------------------------------
# 6. LeakyReLU вместо ReLU
# -------------------------------
model_leaky = models.Sequential([
    layers.Flatten(input_shape=(28,28,1)),
    layers.Dense(256),
    LeakyReLU(alpha=0.1),
    layers.Dense(128),
    LeakyReLU(alpha=0.1),
    layers.Dense(10, activation='softmax')
])
model_leaky.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

train_and_plot(
    model_leaky, x_train, y_train,
    title='Model with LeakyReLU', epochs=25, batch_size=64
)

# -------------------------------
# 7. EarlyStopping
# -------------------------------
model_es = models.Sequential([
    layers.Flatten(input_shape=(28,28,1)),
    layers.Dense(256, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])
model_es.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

train_and_plot(
    model_es, x_train, y_train,
    title='Model with EarlyStopping', epochs=50, batch_size=64, early_stop=True
)

# -------------------------------
# 8. Batch size: 32 и 128
# -------------------------------
for bs in [32, 128]:
    model_bs = models.Sequential([
        layers.Flatten(input_shape=(28,28,1)),
        layers.Dense(256, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    model_bs.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    train_and_plot(
        model_bs, x_train, y_train,
        title=f'Batch size = {bs}', epochs=25, batch_size=bs
    )

# -------------------------------
# 9. Обучение на 10% данных
# -------------------------------
x_small, y_small = get_small_train_set(x_train, y_train, frac=0.1)

model_small_data = models.Sequential([
    layers.Flatten(input_shape=(28,28,1)),
    layers.Dense(256, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])
model_small_data.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

train_and_plot(
    model_small_data, x_small, y_small,
    title='Training on 10% of data', epochs=25, batch_size=64
)

'''
КРАТКИЕ ВЫВОДЫ:
1) Рост разницы между train и val loss → переобучение.
2) Большая модель имеет больше параметров и легко запоминает обучающие данные.
3) Слишком много эпох усиливает переобучение.
4) Dropout случайно отключает нейроны и улучшает обобщение.
5) L2 штрафует большие веса и упрощает модель.
6) Validation_split нужен для контроля качества на новых данных.
7) Малый batch size даёт шумное, но более устойчивое обучение.
8) Недообучение: оба loss большие. Переобучение: train ↓, val ↑.
'''

# 1. Что такое обобщение?
'''
Обобщение — это способность модели корректно работать на новых, ранее не виденных данных,
а не только на обучающей выборке.
'''

# 2. Как выглядит график переобучения?
'''
При переобучении:
* train loss уменьшается,
* val loss сначала уменьшается, затем начинает расти.
  Графики расходятся.
'''

# 3. Что означает рост val loss при падении train loss?
'''
Это означает, что модель запоминает обучающие данные,
но теряет способность обобщать — классический признак переобучения.
'''

# 4. Почему модель может недообучаться?
''' Недообучение возникает, если:
* модель слишком простая,
* недостаточно эпох обучения,
* слишком сильная регуляризация,
* данные слишком сложные для данной архитектуры.
'''

# 5. Каким образом увеличение глубины модели влияет на переобучение?
'''
Увеличение глубины:
* повышает емкость модели,
* увеличивает риск переобучения,
  если не использовать регуляризацию.
'''

# 6. Что такое емкость модели?
'''
Емкость модели — это способность аппроксимировать сложные зависимости.
Чем больше параметров и слоёв, тем выше емкость.
'''

# 7. Как уменьшить переобучение без изменения архитектуры?
'''
Можно:
* использовать EarlyStopping,
* уменьшить число эпох,
* увеличить объём данных,
* применить data augmentation,
* изменить batch size.
'''

# 8. Что делает Dropout?
'''
Dropout случайно отключает нейроны во время обучения,
что предотвращает их совместную адаптацию и улучшает обобщение.
'''

# 9. Как действует L2-регуляризация?
'''
L2-регуляризация:
* штрафует большие веса,
* делает модель более «гладкой»,
* снижает переобучение.
'''

# 10. Почему нужно следить за разницей train/val?
'''
Большая разница между train и val:
* указывает на переобучение,
* позволяет вовремя остановить обучение или изменить параметры.
'''

# 11. Что произойдет при увеличении batch size?
'''
При большом batch size:
* обучение становится стабильнее,
* хуже исследуется пространство решений,
* возможно усиление переобучения.
'''

# 12. Зачем использовать проверочную выборку?
'''
Проверочная выборка нужна для:
* оценки качества модели на новых данных,
* настройки гиперпараметров,
* выявления переобучения.
'''
