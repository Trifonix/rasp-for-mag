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

const style = document.createElement("style");
style.innerHTML = `
  @keyframes blink {
    0% { background-color: orange; }
    10% { background-color: whitesmoke; }
    60% { background-color: orange; }
    90% { background-color: whitesmoke; }
    100% { background-color: orange; }
  }
  tr.active {
    animation: blink 2s infinite;
  }
`;
document.head.appendChild(style);

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

    const items = scheduleData[day];
    const visibleItems = items.filter((item) => {
      if (filter === "today")
        return dayDateObj.toDateString() === today.toDateString();
      if (filter === "week")
        return dayDateObj >= monday && dayDateObj <= sunday;
      if (filter === "semester") return true;
      return false;
    });

    if (visibleItems.length === 0) continue;

    if (filter === "semester" && currentWeek !== weekNumber) {
      currentWeek = weekNumber;
      const trSep = document.createElement("tr");
      trSep.className = "week-separator";
      trSep.innerHTML = `<td colspan="6">Неделя ${weekNumber} (${formatDateShort(
        weekStart
      )} – ${formatDateShort(weekEnd)})</td>`;
      tbody.appendChild(trSep);
    }

    visibleItems.forEach((item, index) => {
      const tr = document.createElement("tr");
      let rowClass = "other";

      if (dayDateObj.toDateString() === today.toDateString()) {
        rowClass = "today";
      } else if (dayDateObj < today) {
        rowClass = "done";
      } else if (filter === "week" || filter === "semester") {
        rowClass = "week";
      }

      tr.className = rowClass;

      if (index === 0) {
        tr.innerHTML = `
          <td rowspan="${visibleItems.length}">${day}</td>
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
      } else {
        tr.innerHTML = `
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
      }

      tbody.appendChild(tr);
    });
  }

  highlightCurrentLesson();
}

function highlightCurrentLesson() {
  const now = new Date();
  const todayStr = now.toDateString();

  document.querySelectorAll("#schedule-body tr").forEach((tr) => {
    let dateCell = tr.children[0]?.textContent;
    let dayDateObj = parseDateObj(dateCell || "");

    if (!dayDateObj) {
      let prevRow = tr.previousElementSibling;
      while (prevRow && !dayDateObj) {
        dateCell = prevRow.children[0]?.textContent;
        dayDateObj = parseDateObj(dateCell || "");
        prevRow = prevRow.previousElementSibling;
      }
    }

    if (!dayDateObj || dayDateObj.toDateString() !== todayStr) {
      tr.classList.remove("active");
      return;
    }

    let timeCell = Array.from(tr.children).find(td =>
      /\d{2}:\d{2}-\d{2}:\d{2}/.test(td.textContent)
    );
    if (!timeCell) return;

    const match = timeCell.textContent.match(/(\d{2}:\d{2})-(\d{2}:\d{2})/);
    if (!match) return;

    const [_, start, end] = match;
    const [startH, startM] = start.split(":").map(Number);
    const [endH, endM] = end.split(":").map(Number);

    const startTime = new Date();
    startTime.setHours(startH, startM - 10, 0, 0);

    const endTime = new Date();
    endTime.setHours(endH, endM + 5, 0, 0);

    if (now >= startTime && now <= endTime) {
      tr.classList.add("active");
    } else {
      tr.classList.remove("active");
    }
  });
}

setInterval(highlightCurrentLesson, 1000);

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
