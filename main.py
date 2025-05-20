import flet as ft
from db import main_db

def main(page: ft.Page):
    print("Starting the app...")
    page.title = "Todo App"
    page.padding = 20
    page.bg_color = ft.Colors.GREY_600
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_tasks():
            task_list.controls.append(create_task_row(task_id, task_text))
        page.update()

    def create_task_row(task_id, task_text):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        def enable_edit(e):
            task_field.read_only = False
            task_field.update()

        def save_task(e):
            main_db.update_task_db(task_id, task_field.value)
            page.update()

        return ft.Row([
            task_field,
            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.Icons.SAVE, icon_color=ft.Colors.GREEN_400, on_click=save_task)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_task(e):
        if task_input.value:
            task_id = main_db.add_task_db(task_input.value)
            task_list.controls.append(create_task_row(task_id, task_input.value))
            task_input.value = ""
            page.update()

    task_input = ft.TextField(hint_text="Добавьте задачу: ", expand=True, dense=True, on_submit=add_task)

    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN_400)

    page.add(ft.Column({
        ft.Row({task_input, add_button}, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        task_list
    }))

    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
