const tbody = document.getElementById("schedule-body");

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
  return (
    1 +
    Math.round(
      ((tmp.getTime() - week1.getTime()) / 86400000 -
        3 +
        ((week1.getDay() + 6) % 7)) /
        7
    )
  );
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
  return d
    .toLocaleDateString("ru-RU", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    })
    .replace(/\//g, ".");
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

    const weekNumber = getWeekNumberISO(dayDateObj);
    const { monday: weekStart, sunday: weekEnd } = getWeekRange(dayDateObj);

    if (filter === "semester") {
      if (currentWeek !== weekNumber) {
        currentWeek = weekNumber;
        const trSep = document.createElement("tr");
        trSep.className = "week-separator";
        trSep.innerHTML = `<td colspan="6">Неделя ${weekNumber} (${formatDateShort(
          weekStart
        )} – ${formatDateShort(weekEnd)})</td>`;
        tbody.appendChild(trSep);
      }
    }

    for (const item of scheduleData[day]) {
      let tr = document.createElement("tr");
      let rowClass = "other";

      if (filter === "today") {
        if (dayDateObj.toDateString() !== today.toDateString()) continue;
        rowClass = "today";
      } else if (filter === "week") {
        if (dayDateObj < monday || dayDateObj > sunday) continue;
        if (dayDateObj.toDateString() === today.toDateString()) {
          rowClass = "today";
        } else if (dayDateObj < today) {
          rowClass = "done";
        } else {
          rowClass = "week";
        }
      } else if (filter === "semester") {
        if (dayDateObj.toDateString() === today.toDateString()) {
          rowClass = "today";
        } else if (dayDateObj < today) {
          rowClass = "done";
        } else {
          rowClass = "week";
        }
      }

      tr.className = rowClass;
      tr.innerHTML = `
              <td>${day}</td>
              <td>${item["Пара"]}</td>
              <td>${item["Вид занятий"]}</td>
              <td>${item["Дисциплина"]}</td>
              <td>${item["Преподаватель"]}</td>
              <td>${
                item["Ссылка"]
                  ? `<a href="${item["Ссылка"]}" target="_blank">Ссылка</a>`
                  : ""
              }</td>
            `;
      tbody.appendChild(tr);
    }
  }
}

fetch("schedule.json")
  .then((response) => response.json())
  .then((data) => {
    window.scheduleData = sortScheduleByDate(data);
    renderTable(window.scheduleData, "today");
  })
  .catch((err) => console.error("Ошибка загрузки JSON:", err));

document.querySelectorAll('input[name="view"]').forEach((radio) => {
  radio.addEventListener("change", () => {
    renderTable(window.scheduleData, radio.value);
  });
});
