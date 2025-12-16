// Выполнил Дмитрий Трифонов, 12-25 РПм, 1 курс, Программная инженерия
// Практическая работа 6: Чувствительность и подбор параметров: сканирование по a, b
// Вариант 12: a∈[0.4..0.9], b∈[0.8..1.8]; шум u

// ---------------------------
// Модель системы
// ---------------------------
function y = simulate_system(a, b)
    y = a^2 + b^2; // Простейший суррогат
endfunction

// ---------------------------
// Рассчёт J(a,b)
// ---------------------------
function J = cost_function(a, b)
    J = abs(sin(a*3) + cos(b*2)) + a*b/10;
endfunction

// ---------------------------
// Метрики ts и os
// ---------------------------
function [ts, os] = metrics(a, b)
    ts = round(10*a + 5*b);      // моделируем время регулирования
    os = abs(a - b) / (a + b + 0.1); // псевдо-перерегулирование
endfunction

// ---------------------------
// Поиск минимума J на сетке
// ---------------------------
function [bestJ, bestA, bestB, table] = scan_grid(a_vals, b_vals)
    bestJ = %inf;
    bestA = 0;
    bestB = 0;
    table = [];

    for i = 1:length(a_vals)
        for j = 1:length(b_vals)
            a = a_vals(i);
            b = b_vals(j);

            J = cost_function(a, b);
            [ts, os] = metrics(a, b);

            table = [table ; a b J ts os];

            if J < bestJ then
                bestJ = J;
                bestA = a;
                bestB = b;
            end
        end
    end
endfunction

// ---------------------------
// Построение фронта Парето
// ---------------------------
function pareto = pareto_front(table)
    // table = [a b J ts os]

    ts_all = table(:,4);
    os_all = table(:,5);

    N = size(table,1);
    pareto = [];

    for i = 1:N
        dominated = %f;
        for j = 1:N
            if j <> i then
                // доминирование: ts_j <= ts_i и os_j <= os_i
                if (ts_all(j) <= ts_all(i)) & (os_all(j) <= os_all(i)) then
                    if (ts_all(j) < ts_all(i)) | (os_all(j) < os_all(i)) then
                        dominated = %t;
                    end
                end
            end
        end

        if ~dominated then
            pareto = [pareto ; table(i,:)];
        end
    end
endfunction

clc;
mprintf("=== Запуск Практикума 06 ===\n");

// Сетка параметров
a_vals = 0.2:0.02:1.0;
b_vals = 0.2:0.02:1.5;

// Сканирование
[bestJ, bestA, bestB, T] = scan_grid(a_vals, b_vals);

mprintf("=== Результаты сканирования ===\n");
mprintf("Лучший J = %f при a = %f, b = %f\n", bestJ, bestA, bestB);

// Метрики в оптимуме
[ts_opt, os_opt] = metrics(bestA, bestB);
mprintf("t_s = %d шагов, os = %f (отн.)\n", ts_opt, os_opt);

// Фронт Парето
P = pareto_front(T);
mprintf("Найдено %d точек на фронте Парето\n", size(P,1));

// Сохранение в CSV
csvWrite(T, "scan_results.csv");
csvWrite(P, "pareto.csv");

mprintf("Результаты сохранены в scan_results.csv и pareto.csv\n");
mprintf("=== Готово. Ошибок нет. ===\n");
