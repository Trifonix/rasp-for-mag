const loader = document.getElementById("loader");
const table = document.querySelector("table");
const tbody = document.getElementById("schedule-body");

// Переменные для хранения данных
let scheduleSemester = null;
let scheduleSemester11 = null;
let scheduleSemester2 = null;

// Сначала прячем таблицу
table.style.display = "none";

// 1. ЗАГРУЗКА ДАННЫХ (Один блок для всех файлов)
Promise.all([
  fetch("schedule.json").then(r => r.json()),
  fetch("schedule1-1.json").then(r => r.json()),
  fetch("schedule2.json").then(r => r.json())
])
.then(([dataMain, data11, data2]) => {
  // Сортируем и сохраняем
  scheduleSemester = sortScheduleByDate(dataMain);
  scheduleSemester11 = sortScheduleByDate(data11);
  scheduleSemester2 = sortScheduleByDate(data2);

  // При первой загрузке показываем "Сегодня" (смешиваем 1 семестр и сессию)
  const merged = mergeSchedules(scheduleSemester, scheduleSemester11);
  renderTable(merged, "today");

  // Скрываем loader и показываем таблицу
  loader.style.display = "none";
  table.style.display = "";
})
.catch(err => {
  loader.textContent = "Ошибка загрузки данных...";
  console.error("Ошибка:", err);
});

// 2. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
function parseDateObj(str) {
  const match = str.match(/\d{2}\.\d{2}\.\d{4}/);
  if (!match) return null;
  const [d, m, y] = match[0].split(".");
  return new Date(`${y}-${m}-${d}`);
}

function sortScheduleByDate(schedule) {
  const entries = Object.entries(schedule);
  entries.sort(([keyA], [keyB]) => {
    const dateA = parseDateObj(keyA);
    const dateB = parseDateObj(keyB);
    return dateA - dateB;
  });
  return Object.fromEntries(entries);
}

function getWeekNumberISO(date) {
  const tmp = new Date(date.valueOf());
  tmp.setHours(0, 0, 0, 0);
  tmp.setDate(tmp.getDate() + 3 - ((tmp.getDay() + 6) % 7));
  const week1 = new Date(tmp.getFullYear(), 0, 4);
  return 1 + Math.round(((tmp.getTime() - week1.getTime()) / 86400000 - 3 + ((week1.getDay() + 6) % 7)) / 7);
}

function getWeekRange(date) {
  const tmp = new Date(date);
  const day = tmp.getDay() || 7;
  const monday = new Date(tmp);
  monday.setDate(tmp.getDate() - day + 1);
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  return { monday, sunday };
}

function formatDateShort(d) {
  return d.toLocaleDateString("ru-RU", { day: "2-digit", month: "2-digit", year: "numeric" });
}

function mergeSchedules(...schedules) {
  const result = {};
  schedules.forEach(s => {
    if (!s) return;
    for (const day in s) {
      result[day] = result[day] ? result[day].concat(s[day]) : [...s[day]];
    }
  });
  return sortScheduleByDate(result);
}

// 3. ОТРИСОВКА ТАБЛИЦЫ
function renderTable(scheduleData, filter = "today") {
  tbody.innerHTML = "";
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const dayOfWeek = today.getDay() || 7;
  const monday = new Date(today);
  monday.setDate(today.getDate() - dayOfWeek + 1);
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);

  let currentWeek = null;

  for (const day in scheduleData) {
    const dayDateObj = parseDateObj(day);
    if (!dayDateObj) continue;

    const visibleItems = scheduleData[day].filter(item => {
      if (filter === "today") return dayDateObj.getTime() === today.getTime();
      if (filter === "week") return dayDateObj >= monday && dayDateObj <= sunday;
      return true; // для всех вариантов семестров
    });

    if (visibleItems.length === 0) continue;

    // Разделитель недель
    const isSemesterView = filter.includes("semester");
    if (isSemesterView) {
      const weekNumber = getWeekNumberISO(dayDateObj);
      if (currentWeek !== weekNumber) {
        currentWeek = weekNumber;
        const { monday: wStart, sunday: wEnd } = getWeekRange(dayDateObj);
        const trSep = document.createElement("tr");
        trSep.className = "week-separator";
        trSep.innerHTML = `<td colspan="6">Неделя ${weekNumber} (${formatDateShort(wStart)} – ${formatDateShort(wEnd)})</td>`;
        tbody.appendChild(trSep);
      }
    }

    visibleItems.forEach((item, index) => {
      const tr = document.createElement("tr");
      let rowClass = "other";

      if (dayDateObj.getTime() === today.getTime()) {
        rowClass = "today";
      } else if (dayDateObj < today) {
        rowClass = "done";
      } else if (filter === "week" || isSemesterView) {
        rowClass = "week";
      }

      tr.className = rowClass;
      if (index === 0) tr.classList.add("day-group-start");

      const dateCell = index === 0 ? `<td rowspan="${visibleItems.length}">${day}</td>` : "";
      
      tr.innerHTML = `
        ${dateCell}
        <td>${item["Пара"]}</td>
        <td>${item["Вид занятий"]}</td>
        <td>${item["Дисциплина"]}</td>
        <td>${item["Преподаватель"]}</td>
        <td>${item["Ссылка"] ? `<a href="${item["Ссылка"]}" target="_blank">Ссылка</a>` : ""}</td>
      `;
      tbody.appendChild(tr);
    });
  }
  highlightCurrentLesson();
}

// 4. ПОДСВЕТКА ТЕКУЩЕЙ ПАРЫ
function highlightCurrentLesson() {
  const now = new Date();
  const todayStr = now.toDateString();

  document.querySelectorAll("#schedule-body tr").forEach((tr) => {
    // Находим дату строки
    let dateRow = tr;
    if (tr.classList.contains('week-separator')) return;
    
    let firstCell = tr.querySelector('td[rowspan]');
    let dateText = firstCell ? firstCell.textContent : "";
    
    // Если в этой строке нет даты (rowspan), ищем в предыдущих
    let tempTr = tr;
    while (!dateText && tempTr.previousElementSibling) {
      tempTr = tempTr.previousElementSibling;
      let cell = tempTr.querySelector('td[rowspan]');
      if (cell) dateText = cell.textContent;
    }

    const dayDateObj = parseDateObj(dateText);
    if (!dayDateObj || dayDateObj.toDateString() !== todayStr) {
      tr.classList.remove("active");
      return;
    }

    // Ищем ячейку со временем (формат 00:00-00:00)
    let timeCell = Array.from(tr.children).find(td => /\d{2}:\d{2}-\d{2}:\d{2}/.test(td.textContent));
    if (!timeCell) return;

    const match = timeCell.textContent.match(/(\d{2}:\d{2})-(\d{2}:\d{2})/);
    if (match) {
      const [_, start, end] = match;
      const [sH, sM] = start.split(":").map(Number);
      const [eH, eM] = end.split(":").map(Number);
      
      const startTime = new Date(now).setHours(sH, sM, 0, 0);
      const endTime = new Date(now).setHours(eH, eM, 0, 0);

      if (now >= startTime && now <= endTime) {
        tr.classList.add("active");
      } else {
        tr.classList.remove("active");
      }
    }
  });
}

// 5. ОБРАБОТКА ПЕРЕКЛЮЧАТЕЛЕЙ (Radio Buttons)
document.querySelectorAll('input[name="view"]').forEach((radio) => {
  radio.addEventListener("change", () => {
    if (radio.value === "semester1-1") {
      renderTable(scheduleSemester11, "semester");
    } else if (radio.value === "semester") {
      renderTable(scheduleSemester, "semester");
    } else if (radio.value === "semester2") {
      renderTable(scheduleSemester2, "semester2");
    } else {
      // Для "Сегодня" и "Недели" объединяем основные данные
      const merged = mergeSchedules(scheduleSemester, scheduleSemester11, scheduleSemester2);
      renderTable(merged, radio.value);
    }
  });
});

// Анимация и интервал
const style = document.createElement("style");
style.innerHTML = `
  @keyframes blink { 0% { background-color: orange; } 50% { background-color: whitesmoke; } 100% { background-color: orange; } }
  tr.active { animation: blink 2s infinite; font-weight: bold; }
`;
document.head.appendChild(style);
setInterval(highlightCurrentLesson, 30000); // Проверяем раз в 30 сек