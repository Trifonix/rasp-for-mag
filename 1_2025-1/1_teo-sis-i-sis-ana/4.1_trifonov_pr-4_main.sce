// Выполнил Дмитрий Трифонов, 12-25 РПм, 1 курс, Программная инженерия
// Практическая работа 4: Структура и связность: матрица смежности, кратчайшие пути, SPOF
// Вариант 12: 6 узлов: брокер сообщений — SPOF‑брокер → кластер

clear; clc;

// ==================== Матрица смежности ====================
A = [0 1 1 0 0 0;
     0 0 1 1 0 0;
     0 0 0 1 1 0;
     0 0 0 0 1 1;
     0 0 0 0 0 1;
     0 0 0 0 0 0];

s = 1; // источник
t = 6; // цель
n = size(A,1);

// ==================== BFS для кратчайших расстояний ====================
function dist = bfs(A,s)
    n = size(A,1);
    dist = -ones(n,1);
    Q = [];
    dist(s) = 0;
    Q($+1) = s;
    while size(Q,'*')>0
        v = Q(1);
        Q(1) = [];
        for w = 1:n
            if A(v,w)==1 & dist(w)==-1 then
                dist(w) = dist(v)+1;
                Q($+1) = w;
            end
        end
    end
endfunction

// ==================== Функция вывода вектора ====================
function s = vec2str(v)
    s = "";
    for i = 1:length(v)
        s = s + string(v(i)) + " ";
    end
endfunction

// ==================== Степени узлов ====================
outdeg = sum(A,'r');  // исходящая степень
indeg  = sum(A,'c');  // входящая степень

// ==================== Кратчайшие расстояния ====================
dist_s = bfs(A,s);

// ==================== Поиск SPOF ====================
SPOF = [];
for v = 1:n
    if v==s | v==t then continue; end
    A_temp = A;
    A_temp(v,:) = 0;
    A_temp(:,v) = 0;
    dist_temp = bfs(A_temp,s);
    if dist_temp(t) == -1 then
        SPOF($+1) = v;
    end
end

// ==================== Вывод результатов ====================
mprintf("Исходящие степени: outdeg = %s\n", vec2str(outdeg));
mprintf("Входящие степени : indeg  = %s\n", vec2str(indeg));
mprintf("Кратчайшие расстояния от узла %d: %s\n", s, vec2str(dist_s));
if isempty(SPOF) then
    mprintf("SPOF узлы отсутствуют\n");
else
    mprintf("SPOF узлы = %s\n", vec2str(SPOF));
end

// ==================== Добавление альтернативного пути ====================
A_alt = A;
if ~isempty(SPOF) then
    for v = SPOF
        A_alt(v,t) = 1; // добавляем альтернативный путь к цели
    end
end
dist_alt = bfs(A_alt,s);
mprintf("Кратчайшие расстояния после добавления альтернатив: %s\n", vec2str(dist_alt));

// ==================== Визуализация графа ====================
clf();
x = [0 1 2 0 1 2];
y = [0 0 0 1 1 1];

// Рисуем ребра
for i = 1:n
    for j = 1:n
        if A(i,j)==1 then
            plot([x(i) x(j)],[y(i) y(j)],'b-','LineWidth',2);
        end
    end
end

// Рисуем узлы
for i = 1:n
    if ~isempty(SPOF) & sum(SPOF==i) > 0 then
        plot(x(i),y(i),'ro','MarkerSize',10,'MarkerFaceColor','r'); // SPOF красным
    else
        plot(x(i),y(i),'go','MarkerSize',8,'MarkerFaceColor','g');  // остальные зелёным
    end
    xstring(x(i),y(i)+0.05,string(i));
end

xtitle("Вариант 12: граф системы (SPOF красным)","x","y");
xgrid();
