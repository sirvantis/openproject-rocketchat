from typing import Optional
import uvicorn
from fastapi_offline import FastAPIOffline
from pydantic import BaseModel
from rocketchat.api import RocketChatAPI

op_project_root_url = 'http://192.168.0.155:8080/projects/' # ссылка на OpenProject
rocket_username = 'openproject' # Логин пользователя в Rocket.Chat от имени которого будут приходить сообщения
rocket_password = 'openproject' # Пароль пользователя в Rocket.Chat от имени которого будут приходить сообщения
rocket_url = 'http://chat:3000' # Ссылка на Rocket.Chat

app = FastAPIOffline() # инициализируем приложение FastAPI
class Item(BaseModel): # описываем модели данных для "Назначенного" и "Подотчетного" (могут быть указаны в задаче, а могут быть и не указаны)
    assignee: Optional[dict] | None = None
    responsible: Optional[dict] | None = None

@app.post('/webhook')
def webhook(data: dict):
    global assignee_login, responsible_login
    api = RocketChatAPI(settings={'username': rocket_username, 'password': rocket_password, 'domain': rocket_url})
    author = data["work_package"]["_embedded"]["author"]["login"]
    task_id = data["work_package"]["id"]
    task_name = data["work_package"]["subject"]
    project_name = data["work_package"]["_embedded"]["project"]["identifier"]
    d = Item(**data["work_package"]["_embedded"])
    if d.assignee is not None: # если у задачи есть назначенный, то присвоить ему login для отправки в Rocket.Chat
        assignee_login = data["work_package"]["_embedded"]["assignee"]["login"]
    if d.responsible is not None: # если у задачи есть подотчетный, то присвоить ему login для отправки в Rocket.Chat
        responsible_login = data["work_package"]["_embedded"]["responsible"]["login"]

    if data["action"] == "work_package:updated":
        api.send_message(
            'Обновление задачи ' + task_name + ' ' + op_project_root_url + project_name + '/' + 'work_packages' + '/' + str(task_id) + '/' + 'activity' + '/', '@' + author)
        if d.assignee is not None:
            if assignee_login != author:
                api.send_message(
            'Обновление задачи ' + task_name + ' ' + op_project_root_url + project_name + '/' + 'work_packages' + '/' + str(task_id) + '/' + 'activity' + '/', '@' + assignee_login)
        #if d.responsible is not None:
        #   if responsible_login != author:
        #       api.send_message(
        #   'Обновление задачи ' + task_name + ' ' + op_project_root_url + project_name + '/' + 'work_packages' + '/' + str(task_id) + '/' + 'activity' + '/', '@' + responsible_login)
    if data["action"] == "work_package:created":
        api.send_message(
            'Создана задача ' + task_name + ' ' + op_project_root_url + project_name + '/' + 'work_packages' + '/' + str(task_id) + '/' + 'activity' + '/', '@' + author)
        if d.assignee is not None:
            if assignee_login != author:
                api.send_message(
            'Создана задача ' + task_name + ' ' + op_project_root_url + project_name + '/' + 'work_packages' + '/' + str(task_id) + '/' + 'activity' + '/', '@' + assignee_login)
       # if d.responsible is not None:
        #   if responsible_login != author:
       #       api.send_message(
        #    'Создана задача ' + task_name + ' ' + op_project_root_url + project_name + '/' + 'work_packages' + '/' + str(task_id) + '/' + 'activity' + '/', '@' + responsible_login)
    return {"status": "ok", "message": "data send complete"} # ответная часть на отправленный вэбхук


if __name__ == "__main__": # запуск вэб-сервера для приема вэбхуков
    uvicorn.run("app:app", host="0.0.0.0", port=8000)