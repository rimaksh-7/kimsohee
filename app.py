from __future__ import annotations

from typing import TypedDict

import streamlit as st


class Task(TypedDict):
    id: int
    title: str
    completed: bool


def initialize_state() -> None:
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "next_task_id" not in st.session_state:
        st.session_state.next_task_id = 1


def add_task(title: str) -> None:
    task_title = title.strip()
    if not task_title:
        return

    st.session_state.tasks.append(
        {
            "id": st.session_state.next_task_id,
            "title": task_title,
            "completed": False,
        }
    )
    st.session_state.next_task_id += 1


def delete_task(task_id: int) -> None:
    st.session_state.tasks = [
        task for task in st.session_state.tasks if task["id"] != task_id
    ]


def update_task_status(task: Task) -> None:
    task["completed"] = st.session_state[f"task_{task['id']}"]


def render_summary(tasks: list[Task]) -> None:
    completed_count = sum(task["completed"] for task in tasks)
    incomplete_count = len(tasks) - completed_count

    summary_columns = st.columns(3)
    summary_columns[0].metric("전체", len(tasks))
    summary_columns[1].metric("미완료", incomplete_count)
    summary_columns[2].metric("완료", completed_count)


def render_task_list(tasks: list[Task]) -> None:
    if not tasks:
        st.info("아직 등록된 할 일이 없습니다. 위 입력창에서 새로운 일을 추가해 보세요.")
        return

    for task in tasks:
        task_columns = st.columns([0.08, 0.82, 0.1])
        task_columns[0].checkbox(
            "완료",
            value=task["completed"],
            key=f"task_{task['id']}",
            label_visibility="collapsed",
            on_change=update_task_status,
            args=(task,),
        )
        title = f"~~{task['title']}~~" if task["completed"] else task["title"]
        task_columns[1].markdown(title)
        if task_columns[2].button("삭제", key=f"delete_{task['id']}"):
            delete_task(task["id"])
            st.rerun()


def render_add_form() -> None:
    with st.form("add_task_form", clear_on_submit=True):
        form_columns = st.columns([0.85, 0.15])
        title = form_columns[0].text_input(
            "새 할 일",
            placeholder="예: 주간 보고서 작성하기",
            label_visibility="collapsed",
        )
        submitted = form_columns[1].form_submit_button("추가", use_container_width=True)

    if submitted:
        if title.strip():
            add_task(title)
            st.rerun()
        st.warning("할 일 내용을 입력해 주세요.")


def main() -> None:
    st.set_page_config(page_title="할 일 관리", page_icon="✅", layout="centered")
    initialize_state()

    st.title("할 일 관리")
    st.caption("오늘 해야 할 일을 한 곳에서 정리해 보세요.")
    render_add_form()
    st.divider()

    tasks: list[Task] = st.session_state.tasks
    render_summary(tasks)
    st.subheader("할 일 목록")
    render_task_list(tasks)


if __name__ == "__main__":
    main()