import streamlit as st
from streamlit.lib import StDict, StList, Pagination, SessionVar

st.code("""
from streamlit.lib import StDict, StList, Pagination, SessionVar
""")

tab1, tab2, tab3 = st.tabs(["Pagination", "Todo List", "Habit Tracker"])
with tab1:
    with st.echo():
      st.header("Pagination")
      page = Pagination("page")

      st.write(f"Page: {page}")

      col1, col2 = st.columns(2)
      col1.button("Previous", on_click=page.previous)
      col2.button("Next", on_click=page.next)
    
    if st.checkbox("Other code", key="1"):
        st.code("""
        st.header("Pagination")
        if "page" not in st.session_state:
          st.session_state.page = 0

        st.write(f"Page: {st.session_state.page}")

        def change_page(delta):
          st.session_state.page += delta
          st.session_state.page = max(0, st.session_state.page)

        col1, col2 = st.columns(2)
        col1.button("Previous", on_click=change_page, args=(-1,))
        col2.button("Next", on_click=change_page, args=(1,))
      """)

with tab2:
    with st.echo():
      st.header("Todo List")

      todos = StList("todos", ["Buy milk", "Buy eggs", "Buy bread"])
      for idx, todo in enumerate(todos):
          st.checkbox(todo, on_change=todos.delete(idx, filter=lambda checkbox_val: checkbox_val))

      new_todo = SessionVar("new_todo", "")
      st.text_input("New todo", key=new_todo)
      st.button("Add todo",
                on_click=todos.append(new_todo)
                  .chain(new_todo.set(""))
      )

    if st.checkbox("Other code", key="2"):
        st.code("""
        st.header("Todo List")

        if "todos" not in st.session_state:
          st.session_state.todos = ["Buy milk", "Buy eggs", "Buy bread"]

        def delete(idx):
          if st.session_state[f"todo_{idx}"]:
            del st.session_state.todos[idx]
                
        for idx, todo in enumerate(todos):
          st.checkbox(todo, on_change=delete, args=(idx,), key=f"todo_{idx}")

        def add_todo():
          new_todo = st.session_state.new_todo
          st.session_state.todos.append(new_todo)
          st.session_state.new_todo = ""

        st.text_input("New todo", key="new_todo")
        st.button("Add todo", on_click=add_todo)
      """)

with tab3:
  with st.echo():
    st.header("Habit Tracker")
    habits = StDict("habits", {"Wake Up": False, "Sleep": False})
    new_habit = SessionVar("new_habit", "")
    st.text_input("Add a new habit", key=new_habit)
    if st.button("Add Habit", on_click=habits.set(new_habit, False)):
        st.success(f"Added habit: {new_habit.val()}")

    st.subheader("Today's Habits")
    for habit, completed in habits.items():
        st.checkbox(habit, value=completed, on_change=habits.set(habit))

    if st.button("Reset for Today", on_click=habits.set_all(False)):
        st.success("Habits reset for a new day!")
    
  if st.checkbox("Other code", key="3"):
    st.code("""
      st.header("Habit Tracker")
      if "habits" not in st.session_state:
        st.session_state.habits = {"Wake Up": False, "Sleep": False}
      
      st.text_input("Add a new habit", key="new_habit")
      
      def add_habit():
        new_habit = st.session_state.new_habit
        st.session_state.habits[new_habit] = False
      if st.button("Add Habit", on_click=add_habit):
          st.success(f"Added habit: {new_habit.val()}")

      st.subheader("Today's Habits")
      def set_habit(habit, idx):
        completed = st.session_state[f"habit_{idx}"]
        st.session_state.habits[habit] = completed

      i = 0
      for habit, completed in habits.items():
        st.checkbox(habit, value=completed, on_change=set, args=(habit, i) key=f"habit_{i}")
        i += 1  

      def reset():
        for key in st.session_state.habits:
          st.session_state.habits[key] = False

      if st.button("Reset for Today", on_click=reset):
          st.success("Habits reset for a new day!")
      """)