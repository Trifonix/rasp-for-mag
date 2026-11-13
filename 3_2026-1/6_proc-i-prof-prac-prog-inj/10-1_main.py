"""Демо: управление событиями UI (Observer / Command) на вымышленных данных."""
from __future__ import annotations

import copy
import tkinter as tk
from dataclasses import dataclass
from datetime import date, timedelta
from tkinter import messagebox, ttk


@dataclass
class Message:
    oid: int
    message_id: str
    sender: str
    contact: str
    subject: str
    scheduled: date
    status: str = "Черновик"


@dataclass
class Command:
    name: str
    undo_fn: object
    redo_fn: object


class EventBus:
    """Издатель событий (аналог источника ActionEvent / Observer)."""

    def __init__(self) -> None:
        self._subs: dict[str, list] = {}

    def subscribe(self, event: str, handler) -> None:
        self._subs.setdefault(event, []).append(handler)

    def publish(self, event: str, payload=None) -> None:
        for handler in self._subs.get(event, []):
            handler(payload)


class MessageStore:
    """Модель данных (аналог PMessageTableModel + PDisplayList)."""

    def __init__(self) -> None:
        today = date(2026, 11, 13)
        self._items: list[Message] = [
            Message(1, "M-1001", "Иванов А.П.", "ООО Альфа", "Счёт за октябрь", today - timedelta(days=2), "Отправлено"),
            Message(2, "M-1002", "Петрова М.И.", "ЗАО Бета", "Напоминание о встрече", today - timedelta(days=1), "Черновик"),
            Message(3, "M-1003", "Сидоров К.В.", "ИП Гамма", "Акт сверки", today, "Ошибка отправки"),
            Message(4, "M-1004", "Иванов А.П.", "ООО Альфа", "Прайс-лист Q4", today + timedelta(days=1), "Запланировано"),
            Message(5, "M-1005", "Козлова Е.Н.", "ЗАО Бета", "Договор поставки", today + timedelta(days=3), "Черновик"),
        ]
        self._next_oid = 6
        self.filter_contact: str | None = None
        self.filter_enabled = False
        self.bus = EventBus()

    def visible(self) -> list[Message]:
        items = list(self._items)
        if self.filter_enabled and self.filter_contact:
            items = [m for m in items if m.contact == self.filter_contact]
        return sorted(items, key=lambda m: m.scheduled, reverse=True)

    def contacts(self) -> list[str]:
        return sorted({m.contact for m in self._items})

    def snapshot(self) -> list[Message]:
        return copy.deepcopy(self._items)

    def restore(self, items: list[Message]) -> None:
        self._items = copy.deepcopy(items)
        self.bus.publish("model_changed")

    def add(self, sender: str, contact: str, subject: str, scheduled: date) -> Message:
        msg = Message(self._next_oid, f"M-{1000 + self._next_oid}", sender, contact, subject, scheduled)
        self._next_oid += 1
        self._items.append(msg)
        self.bus.publish("model_changed")
        return msg

    def delete(self, oid: int) -> Message | None:
        for i, m in enumerate(self._items):
            if m.oid == oid:
                removed = self._items.pop(i)
                self.bus.publish("model_changed")
                return removed
        return None

    def get(self, oid: int) -> Message | None:
        for m in self._items:
            if m.oid == oid:
                return m
        return None


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("EM Mail — управление событиями UI (практика 9)")
        self.geometry("920x520")
        self.minsize(800, 480)
        self.store = MessageStore()
        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []
        self._build()
        self.store.bus.subscribe("model_changed", self._on_model_changed)
        self._refresh_table()
        self._log("Подписчик таблицы зарегистрирован на событие model_changed")

    def _build(self) -> None:
        top = ttk.Frame(self, padding=8)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Исходящие сообщения (вымышленные данные)", font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT)

        toolbar = ttk.Frame(self, padding=(8, 0, 8, 8))
        toolbar.pack(fill=tk.X)
        ttk.Button(toolbar, text="Insert", command=self._on_insert).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete", command=self._on_delete).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Toggle Filter", command=self._on_toggle_filter).pack(side=tk.LEFT, padx=2)
        self.contact_var = tk.StringVar(value="ООО Альфа")
        self.contact_box = ttk.Combobox(toolbar, textvariable=self.contact_var, values=self.store.contacts(), width=18, state="disabled")
        self.contact_box.pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Undo", command=self._on_undo).pack(side=tk.LEFT, padx=8)
        ttk.Button(toolbar, text="Redo", command=self._on_redo).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Exit", command=self.destroy).pack(side=tk.RIGHT, padx=2)

        cols = ("message_id", "sender", "contact", "subject", "scheduled", "status")
        self.table = ttk.Treeview(self, columns=cols, show="headings", height=12)
        headings = {
            "message_id": "ID",
            "sender": "Отправитель",
            "contact": "Партнёр",
            "subject": "Тема",
            "scheduled": "Scheduled Dtp",
            "status": "Статус",
        }
        widths = {"message_id": 80, "sender": 120, "contact": 120, "subject": 220, "scheduled": 110, "status": 120}
        for c in cols:
            self.table.heading(c, text=headings[c], command=lambda col=c: self._on_sort(col))
            self.table.column(c, width=widths[c], anchor=tk.W)
        self.table.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        self.table.bind("<<TreeviewSelect>>", self._on_select)

        self.filter_label = ttk.Label(self, text="Фильтр: выключен", padding=(8, 0))
        self.filter_label.pack(anchor=tk.W)

        self.log = tk.Text(self, height=7, wrap=tk.WORD)
        self.log.pack(fill=tk.BOTH, padx=8, pady=8)

    def _log(self, text: str) -> None:
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def _on_model_changed(self, _payload=None) -> None:
        self._log("Событие: model_changed → обновление представления (Observer)")
        self.contact_box["values"] = self.store.contacts()
        self._refresh_table()

    def _refresh_table(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        for m in self.store.visible():
            self.table.insert("", tk.END, iid=str(m.oid), values=(
                m.message_id, m.sender, m.contact, m.subject, m.scheduled.isoformat(), m.status
            ))
        state = "включён" if self.store.filter_enabled else "выключен"
        contact = self.store.filter_contact or "—"
        self.filter_label.config(text=f"Фильтр: {state}; партнёр: {contact}; записей: {len(self.store.visible())}")

    def _selected_oid(self) -> int | None:
        sel = self.table.selection()
        return int(sel[0]) if sel else None

    def _push(self, cmd: Command) -> None:
        self.undo_stack.append(cmd)
        self.redo_stack.clear()
        self._log(f"Команда «{cmd.name}» добавлена в стек Undo")

    def _on_select(self, _evt=None) -> None:
        oid = self._selected_oid()
        if oid is None:
            return
        m = self.store.get(oid)
        if m:
            self._log(f"Событие выбора строки: {m.message_id} / {m.subject}")

    def _on_sort(self, col: str) -> None:
        self._log(f"Событие сортировки по столбцу «{col}» (аналог клика по заголовку JTable)")
        items = self.store.visible()
        reverse = col == "scheduled"
        key_map = {
            "message_id": lambda m: m.message_id,
            "sender": lambda m: m.sender,
            "contact": lambda m: m.contact,
            "subject": lambda m: m.subject,
            "scheduled": lambda m: m.scheduled,
            "status": lambda m: m.status,
        }
        items = sorted(items, key=key_map[col], reverse=reverse)
        for item in self.table.get_children():
            self.table.delete(item)
        for m in items:
            self.table.insert("", tk.END, iid=str(m.oid), values=(
                m.message_id, m.sender, m.contact, m.subject, m.scheduled.isoformat(), m.status
            ))

    def _on_toggle_filter(self) -> None:
        self.store.filter_enabled = not self.store.filter_enabled
        if self.store.filter_enabled:
            self.contact_box.config(state="readonly")
            self.store.filter_contact = self.contact_var.get()
            self._log("ActionListener: Toggle Filter → фильтр включён")
        else:
            self.contact_box.config(state="disabled")
            self.store.filter_contact = None
            self._log("ActionListener: Toggle Filter → фильтр выключен")
        self.store.bus.publish("model_changed")

    def _on_insert(self) -> None:
        dlg = tk.Toplevel(self)
        dlg.title("Create New Message")
        dlg.transient(self)
        dlg.grab_set()
        fields = {
            "sender": tk.StringVar(value="Иванов А.П."),
            "contact": tk.StringVar(value="ООО Альфа"),
            "subject": tk.StringVar(value=""),
            "scheduled": tk.StringVar(value=date(2026, 11, 20).isoformat()),
        }
        form = ttk.Frame(dlg, padding=12)
        form.pack(fill=tk.BOTH, expand=True)
        labels = [("Отправитель", "sender"), ("Партнёр", "contact"), ("Тема", "subject"), ("Дата (YYYY-MM-DD)", "scheduled")]
        for i, (label, key) in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky=tk.W, pady=4)
            ttk.Entry(form, textvariable=fields[key], width=36).grid(row=i, column=1, pady=4)

        def save() -> None:
            errors = []
            if not fields["subject"].get().strip():
                errors.append("Тема обязательна")
            if not fields["contact"].get().strip():
                errors.append("Партнёр обязателен")
            try:
                scheduled = date.fromisoformat(fields["scheduled"].get().strip())
            except ValueError:
                errors.append("Некорректная дата")
                scheduled = None
            if errors:
                messagebox.showerror("Unable to Send", "\n".join(errors), parent=dlg)
                self._log("Валидация: Unable to Send — " + "; ".join(errors))
                return
            before = self.store.snapshot()
            msg = self.store.add(
                fields["sender"].get().strip(),
                fields["contact"].get().strip(),
                fields["subject"].get().strip(),
                scheduled,
            )
            after = self.store.snapshot()
            self._push(Command(
                "Insert",
                undo_fn=lambda: self.store.restore(before),
                redo_fn=lambda: self.store.restore(after),
            ))
            self._log(f"Создан заместитель сообщения OID={msg.oid}, messageID={msg.message_id}")
            dlg.destroy()

        btns = ttk.Frame(form)
        btns.grid(row=len(labels), column=0, columnspan=2, pady=8)
        ttk.Button(btns, text="Сохранить", command=save).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="Отмена", command=dlg.destroy).pack(side=tk.LEFT, padx=4)

    def _on_delete(self) -> None:
        oid = self._selected_oid()
        if oid is None:
            messagebox.showinfo("Delete", "Выберите сообщение в таблице")
            return
        m = self.store.get(oid)
        if m is None:
            return
        ok = messagebox.askyesno(
            "Удаление исходящего сообщения",
            f"Удалить сообщение?\nID: {m.message_id}\nТема: {m.subject}\nПартнёр: {m.contact}",
        )
        if not ok:
            self._log("Удаление отменено пользователем")
            return
        before = self.store.snapshot()
        self.store.delete(oid)
        after = self.store.snapshot()
        self._push(Command(
            "Delete",
            undo_fn=lambda: self.store.restore(before),
            redo_fn=lambda: self.store.restore(after),
        ))
        self._log(f"Удалено сообщение {m.message_id}")

    def _on_undo(self) -> None:
        if not self.undo_stack:
            self._log("Undo: стек пуст")
            return
        cmd = self.undo_stack.pop()
        cmd.undo_fn()
        self.redo_stack.append(cmd)
        self._log(f"Undo: отменена команда «{cmd.name}»")

    def _on_redo(self) -> None:
        if not self.redo_stack:
            self._log("Redo: стек пуст")
            return
        cmd = self.redo_stack.pop()
        cmd.redo_fn()
        self.undo_stack.append(cmd)
        self._log(f"Redo: восстановлена команда «{cmd.name}»")


if __name__ == "__main__":
    App().mainloop()
