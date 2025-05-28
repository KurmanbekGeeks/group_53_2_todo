import flet as ft
from db import main_db
from datetime import datetime, date, timedelta


def main(page: ft.Page):
    print("Starting the app...")
    page.title = "Todo App"
    # page.padding = 20
    # page.bg_color = ft.Colors.GREY_600
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximized = True

    task_list = ft.Column(spacing=10)

    filter_type = 'all'

    def get_deadline_color(deadline_str):
        if not deadline_str:
            return ft.Colors.WHITE
        
        deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        today = date.today()

        if deadline_date < today:
            return ft.Colors.RED

        days_left = (deadline_date - today).days
        if days_left < 3:
            return ft.Colors.ORANGE
        elif days_left <= 7:
            return ft.Colors.YELLOW
        else:
            return ft.Colors.GREEN
    
    def get_deadline_text(deadline_str):
        if not deadline_str:
            return "Нет срока"
        
        deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        today = date.today()

        if deadline_date < today:
            return f'Просрочено! ({deadline_str})'
        
        days_left = (deadline_date - today).days
        if days_left == 0:
            return 'Сегодня'
        elif days_left == 1:
            return 'Завтра'
        elif days_left < 3:
            return f"Очень срочно! {days_left} дн. ({deadline_str})"
        else:
            return f"{days_left} дн. ({deadline_str})"

    # def load_tasks():
    #     task_list.controls.clear()
    #     for task_id, task_text, completed in main_db.get_tasks():
    #         task_list.controls.append(create_task_row(task_id, task_text, completed))
    #     page.update()

    def load_tasks():
        task_list.controls.clear()
        all_tasks = main_db.get_tasks()
        if filter_type == 'completed':
            tasks = [t for t in all_tasks if t[2]]  # t[2] — это completed
        elif filter_type == 'uncompleted':
            tasks = [t for t in all_tasks if not t[2]]
        else:
            tasks = all_tasks
        for task_id, task_text, completed, deadline in tasks:
            task_list.controls.append(create_task_row(task_id, task_text, completed, deadline))
        page.update()

    def create_task_row(task_id, task_text, completed, deadline):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        deadline_text = ft.Text(
            value=get_deadline_text(deadline),
            color=get_deadline_color(deadline),
            size=12,
            weight=ft.FontWeight.BOLD if deadline and 
                    datetime.strptime(deadline, "%Y-%m-%d").date() < date.today() + timedelta(days=3)
                    else ft.FontWeight.NORMAL
        )

        def enable_edit(e):
            task_field.read_only = False
            task_field.update()

        def save_task(e):
            main_db.update_task_db(task_id, task_field.value)
            page.update()

        def handler_date_picked(e):
            if e.control.value:
                selected_date = e.control.value
                update_deadline(task_id, selected_date.strftime("%Y-%m-%d"))

        def pick_date(e):
            date_picker = ft.DatePicker(
                on_change=handler_date_picked,
                open=True
            )

            page.overlay.append(date_picker)
            page.update()

        def update_deadline(task_id, new_deadline):
            main_db.update_task_db(task_id, deadline=new_deadline)
            load_tasks()

        return ft.Row([
            task_checkbox,
            task_field,
            deadline_text,
            ft.IconButton(ft.Icons.CALENDAR_TODAY, icon_color=ft.Colors.BLUE, on_click=pick_date),
            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.Icons.SAVE, icon_color=ft.Colors.GREEN_400, on_click=save_task),
            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e: delete_task(task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


    def add_task(e):
        if task_input.value:
            task_id = main_db.add_task_db(task_input.value)
            task_list.controls.append(create_task_row(task_id, task_input.value, False,  None))
            task_input.value = ""
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task_db(task_id, completed=int(is_completed))
        load_tasks()


    def delete_task(task_id):
        main_db.delete_task_db(task_id)
        load_tasks()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    task_input = ft.TextField(hint_text="Добавьте задачу: ", expand=True, dense=True, on_submit=add_task)

    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN_400)

    filter_buttons = ft.Row(
        controls=[
            ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
            ft.ElevatedButton("Завершенные", on_click=lambda e: set_filter('completed')),
            ft.ElevatedButton("Незавершенные", on_click=lambda e: set_filter('uncompleted'))
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # page.add(ft.Column({
    #     ft.Row({task_input, add_button}, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    #     task_list
    # }))

    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[task_input, add_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                filter_buttons,
                task_list
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=20,
        alignment=ft.alignment.center
    )

    background_image = ft.Image(
        src="/Users/kurmanbek/Desktop/Geeks/Groups_flet/group_53_2_to_do_list/media/image.png",
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )   

    background = ft.Stack(controls=[content])

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        background.update()

    page.add(background)
    page.on_resize = on_resize

    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
