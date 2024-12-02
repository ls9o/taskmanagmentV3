from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.database import get_db
from app.database import init_db
from app.api.routes.greet_router import router as greet_router
from app.api.routes.menu_router import router as menu_router
# from app.api.routes.user_router import router as user_router
from app.api.routes.employee_router import router as employee_router
from app.api.routes.option_router import router as option_router
# from app.api.routes.task_router import router as task_router
from app.api.routes.task_routerdb import router as task_routerdb
from app.api.routes.subtasksdb_router import router as subtasksdb_router
# from app.api.routes.process_router import router as process_router
from app.api.routes.processdb_router import router as processdb_router
# from app.api.routes.subprocess_router import router as subprocess_router
from app.api.routes.subprocessdb_router import router as subprocessdb_router
from app.api.routes.log_router import router as log_router
from app.api.routes.login_router import router as login_router
from app.api.routes.sendmail_router import router as sendmail_router

from app.api.routes.user_routerdb import router as user_routerdb
from app.api.routes.task_routerdb import router as task_routerdb
from app.api.routes.subprocessdb_router import router as subprocessdb_router
from app.api.routes.processdb_router import router as processdb_router
from app.api.routes.menudb_router import router as menudb_router
from app.api.routes.teamdb_router import router as teamdb_router

app = FastAPI(title="SME D Connect")
init_db()
get_db()   

origins = [
    "http://localhost:8080",  # ตัวอย่าง: อนุญาตให้เข้าถึงจาก frontend ที่อยู่บน localhost:8081
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ระบุ origins ที่อนุญาต
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตทุก HTTP methods เช่น GET, POST
    allow_headers=["*"],  # อนุญาตทุก HTTP headers
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    headers = dict(request.headers)
    print("Headers:", headers)
    if request.method == "GET":
        query_params = dict(request.query_params)
        print("GET Query Parameters:", query_params)
    response = await call_next(request)
    return response

routers = [
    greet_router,
    menu_router,
    menudb_router,
    user_routerdb,
    employee_router,
    option_router,
    task_routerdb,
    subtasksdb_router,
    processdb_router,
    processdb_router,
    subprocessdb_router,
    log_router,
    teamdb_router,
    login_router,
    sendmail_router,
    

]

for router in routers:
    app.include_router(router, prefix="/api", tags=["API Module"])


app.mount(
    "/views",
    StaticFiles(directory="views/dist", html=True),
    name="static",
)
