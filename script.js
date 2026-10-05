const loader = document.getElementById("loader");
const table = document.querySelector(".schedule-table");
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

const WEEKDAY_SHORT = {
  понедельник: "пн",
  вторник: "вт",
  среда: "ср",
  четверг: "чт",
  пятница: "пт",
  суббота: "сб",
  воскресенье: "вс",
};

function formatDateCell(day) {
  const parts = String(day).trim().split(/\s+/);
  const date = parts[0] || day;
  const weekday = (parts.slice(1).join(" ") || "").toLowerCase();
  const shortWd = WEEKDAY_SHORT[weekday] || weekday.slice(0, 2);
  const shortDate = date.slice(0, 5);
  return `<span class="date-full">${day}</span><span class="date-short">${shortDate} ${shortWd}</span>`;
}

function formatPairCell(pair) {
  const match = String(pair).match(/(\d+)\s*пара\s*(.*)/i);
  if (!match) return pair;
  const time = match[2].replace(/-/g, "–");
  return `<span class="pair-num">${match[1]}<span class="pair-word"> пара</span></span> <span class="pair-time">${time}</span>`;
}

function applyViewLayout(filter) {
  document.documentElement.dataset.view = filter;
  document.body.dataset.view = filter;
  requestAnimationFrame(() => {
    requestAnimationFrame(fitWeekToScreen);
  });
}

function fitWeekToScreen() {
  const root = document.documentElement;
  const wrap = document.querySelector(".schedule-wrap");
  if (!wrap) return;

  if (root.dataset.view !== "week") {
    wrap.style.height = "";
    root.style.removeProperty("--lesson-font");
    root.style.removeProperty("--lesson-pad-y");
    root.style.removeProperty("--lesson-pad-x");
    root.style.removeProperty("--ui-compact");
    return;
  }

  const bottomPad = parseFloat(getComputedStyle(document.body).paddingBottom) || 0;
  const avail = Math.max(120, window.innerHeight - wrap.getBoundingClientRect().top - bottomPad);
  wrap.style.height = `${avail}px`;

  root.style.setProperty("--ui-compact", "1");
  let font = window.innerWidth >= 1024 ? 14 : window.innerWidth >= 700 ? 12 : 11;

  for (let i = 0; i < 24; i += 1) {
    root.style.setProperty("--lesson-font", `${font}px`);
    root.style.setProperty("--lesson-pad-y", `${Math.max(1, font * 0.22)}px`);
    root.style.setProperty("--lesson-pad-x", `${Math.max(3, font * 0.38)}px`);
    const fitsHeight = wrap.scrollHeight <= avail + 1;
    const fitsWidth = wrap.scrollWidth <= wrap.clientWidth + 1;
    if (fitsHeight && fitsWidth) break;
    font -= 0.4;
    if (font < 8) break;
  }
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

      tr.className = `lesson-row ${rowClass}`;
      tr.dataset.date = day;
      if (index === 0) tr.classList.add("day-group-start");

      const dateCell = index === 0
        ? `<td class="cell-date" rowspan="${visibleItems.length}">${formatDateCell(day)}</td>`
        : "";

      const discipline = item["Дисциплина"] || "";
      const teacher = item["Преподаватель"] || "";
      const kind = item["Вид занятий"] || "";

      const linkHtml = item["Ссылка"]
        ? `<a class="lesson-link" href="${item["Ссылка"]}" target="_blank" rel="noopener noreferrer"><span class="lesson-link-text">Открыть</span></a>`
        : "";

      tr.innerHTML = `
        ${dateCell}
        <td class="cell-pair" data-label="Пара">${formatPairCell(item["Пара"])}</td>
        <td class="cell-kind" data-label="Вид">${kind}</td>
        <td class="cell-discipline" data-label="Дисциплина" title="${discipline}">${discipline}</td>
        <td class="cell-teacher" data-label="Преподаватель" title="${teacher}">${teacher}</td>
        <td class="cell-link" data-label="Ссылка">${linkHtml}</td>
      `;
      tbody.appendChild(tr);
    });
  }
  highlightCurrentLesson();
  applyViewLayout(filter);
}

function highlightCurrentLesson() {
  const now = new Date();
  const todayStr = now.toDateString();

  document.querySelectorAll("#schedule-body tr.lesson-row").forEach((tr) => {
    const dayDateObj = parseDateObj(tr.dataset.date);

    if (!dayDateObj || dayDateObj.toDateString() !== todayStr) {
      tr.classList.remove("active");
      return;
    }

    const timeCell = Array.from(tr.children).find(td => /\d{2}:\d{2}[-–]\d{2}:\d{2}/.test(td.textContent));
    if (!timeCell) return;

    const match = timeCell.textContent.match(/(\d{2}:\d{2})[-–](\d{2}:\d{2})/);
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

setInterval(highlightCurrentLesson, 30000);

let fitWeekTimer = 0;
window.addEventListener("resize", () => {
  window.clearTimeout(fitWeekTimer);
  fitWeekTimer = window.setTimeout(fitWeekToScreen, 80);
});
window.addEventListener("orientationchange", () => {
  window.setTimeout(fitWeekToScreen, 160);
});
