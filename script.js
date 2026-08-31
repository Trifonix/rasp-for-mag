const loader = document.getElementById("loader");
const table = document.querySelector("table");
const tbody = document.getElementById("schedule-body");

const SEMESTER_VIEWS = [
  { value: "semester", scheduleKey: "semester1" },
  { value: "semester2", scheduleKey: "semester2" },
  { value: "semester3", scheduleKey: "semester3" },
];

let scheduleSemester = null;
let scheduleSemester2 = null;
let scheduleSemester3 = null;
let currentSemesterView = null;

table.style.display = "none";

Promise.all([
  fetch("schedule.json").then(r => r.json()),
  fetch("schedule2.json").then(r => r.json()),
  fetch("schedule3.json").then(r => r.json()),
  document.fonts.ready
])
.then(([dataMain, data2, data3]) => {
  scheduleSemester = sortScheduleByDate(dataMain);
  scheduleSemester2 = sortScheduleByDate(data2);
  scheduleSemester3 = sortScheduleByDate(data3);

  currentSemesterView = detectCurrentSemesterView({
    semester1: scheduleSemester,
    semester2: scheduleSemester2,
    semester3: scheduleSemester3,
  });

  updateControlStyles();
  renderTable(getMergedSchedules(), "today");

  loader.style.display = "none";
  table.style.display = "";
})
.catch(err => {
  loader.textContent = "Ошибка загрузки данных...";
  console.error("Ошибка:", err);
});

function getScheduleByView(view) {
  if (view === "semester") return scheduleSemester;
  if (view === "semester2") return scheduleSemester2;
  if (view === "semester3") return scheduleSemester3;
  return null;
}

function getMergedSchedules() {
  return mergeSchedules(scheduleSemester, scheduleSemester2, scheduleSemester3);
}

function parseDateObj(str) {
  const match = str.match(/\d{2}\.\d{2}\.\d{4}/);
  if (!match) return null;
  const [d, m, y] = match[0].split(".");
  return new Date(`${y}-${m}-${d}`);
}

function getScheduleDateRange(schedule) {
  if (!schedule) return null;

  const dates = Object.keys(schedule)
    .map(parseDateObj)
    .filter(Boolean);

  if (!dates.length) return null;

  dates.sort((a, b) => a - b);
  return { min: dates[0], max: dates[dates.length - 1] };
}

function detectCurrentSemesterView(schedulesByKey) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  for (const { value, scheduleKey } of SEMESTER_VIEWS) {
    const range = getScheduleDateRange(schedulesByKey[scheduleKey]);
    if (range && today >= range.min && today <= range.max) {
      return value;
    }
  }

  let nearestUpcoming = null;
  let nearestDiff = Infinity;

  for (const { value, scheduleKey } of SEMESTER_VIEWS) {
    const range = getScheduleDateRange(schedulesByKey[scheduleKey]);
    if (!range) continue;

    if (range.min >= today) {
      const diff = range.min - today;
      if (diff < nearestDiff) {
        nearestDiff = diff;
        nearestUpcoming = value;
      }
    }
  }

  if (nearestUpcoming) return nearestUpcoming;

  let latestPast = null;
  let latestEnd = null;

  for (const { value, scheduleKey } of SEMESTER_VIEWS) {
    const range = getScheduleDateRange(schedulesByKey[scheduleKey]);
    if (!range) continue;

    if (!latestEnd || range.max > latestEnd) {
      latestEnd = range.max;
      latestPast = value;
    }
  }

  return latestPast || "semester3";
}

function updateControlStyles() {
  document.querySelectorAll(".controls label.control-btn").forEach((label) => {
    label.classList.remove(
      "control-today",
      "control-week",
      "control-semester-past",
      "control-semester-current"
    );

    const view = label.dataset.view;
    if (view === "today") {
      label.classList.add("control-today");
    } else if (view === "week") {
      label.classList.add("control-week");
    } else if (view === currentSemesterView) {
      label.classList.add("control-semester-current");
    } else {
      label.classList.add("control-semester-past");
    }
  });
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
      if (filter === "today") return dayDateObj.toDateString() === today.toDateString();
      if (filter === "week") return dayDateObj >= monday && dayDateObj <= sunday;
      return true;
    });

    if (visibleItems.length === 0) continue;

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

      if (dayDateObj.toDateString() === today.toDateString()) {
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

function highlightCurrentLesson() {
  const now = new Date();
  const todayStr = now.toDateString();

  document.querySelectorAll("#schedule-body tr").forEach((tr) => {
    if (tr.classList.contains("week-separator")) return;

    let firstCell = tr.querySelector("td[rowspan]");
    let dateText = firstCell ? firstCell.textContent : "";

    let tempTr = tr;
    while (!dateText && tempTr.previousElementSibling) {
      tempTr = tempTr.previousElementSibling;
      const cell = tempTr.querySelector("td[rowspan]");
      if (cell) dateText = cell.textContent;
    }

    const dayDateObj = parseDateObj(dateText);

    if (!dayDateObj || dayDateObj.toDateString() !== todayStr) {
      tr.classList.remove("active");
      return;
    }

    const timeCell = Array.from(tr.children).find(td => /\d{2}:\d{2}-\d{2}:\d{2}/.test(td.textContent));
    if (!timeCell) return;

    const match = timeCell.textContent.match(/(\d{2}:\d{2})-(\d{2}:\d{2})/);
    if (match) {
      const [_, start, end] = match;
      const [sH, sM] = start.split(":").map(Number);
      const [eH, eM] = end.split(":").map(Number);

      const startTime = new Date(now).setHours(sH, sM, 0, 0);
      const endTime = new Date(now).setHours(eH, eM, 0, 0);

      if (now.getTime() >= startTime && now.getTime() <= endTime) {
        tr.classList.add("active");
        tr.classList.remove("done");
        tr.classList.add("today");
      } else if (now.getTime() > endTime) {
        tr.classList.remove("active");
        tr.classList.add("done");
        tr.classList.remove("today");
      } else {
        tr.classList.remove("active");
        tr.classList.remove("done");
        tr.classList.add("today");
      }
    }
  });
}

document.querySelectorAll('input[name="view"]').forEach((radio) => {
  radio.addEventListener("change", () => {
    const schedule = getScheduleByView(radio.value);
    if (schedule) {
      renderTable(schedule, radio.value);
    } else {
      renderTable(getMergedSchedules(), radio.value);
    }
  });
});

const style = document.createElement("style");
style.innerHTML = `
  @keyframes blink { 0% { background-color: orange; } 50% { background-color: whitesmoke; } 100% { background-color: orange; } }
  tr.active { animation: blink 2s infinite; font-weight: bold; }
`;
document.head.appendChild(style);
setInterval(highlightCurrentLesson, 30000);
