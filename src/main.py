# uvicorn main:app --reload
import asyncio
import os
import time
from concurrent.futures import ProcessPoolExecutor

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from fastapi.middleware.cors import CORSMiddleware



# 引入 pg api router
from .app.route import router

# Override environment for OAuth2.0 development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="!secret")
app.include_router(router)

origins = [
    "http://localhost",
    "http://localhost:7877",
    "http://localhost:8081",
    "http://localhost:5432",
    "https://form.fang5-group.tw",
    "https://fang5-group.tw" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    
)


@app.get("/")
async def root():
    return {"message": "Hello World!!!!"}


@app.get("/fastapi/async_slowest/")
async def async_slowest():
    time.sleep(1)
    return {"message": "async mode but use sync sleep"}


@app.get("/fastapi/async_sleep_in_thread/")
async def async_sleep_in_thread():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, time.sleep, 1)
    return {"message": "sleep run in thread pool"}


@app.get("/fastapi/async_sleep/")
async def async_sleep():
    await asyncio.sleep(1)
    return {"message": "async mode sleep"}


@app.get("/fastapi/sync/")
def sync_sleep():
    time.sleep(1)
    return {"message": "sync, but run in thread pool"}


def cpu_bound_operation(BIGNUM):
    num = 0
    for i in range(BIGNUM):
        num += 1
    return num


executor = ProcessPoolExecutor()


async def async_cpu_operation(BIGNUM):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, cpu_bound_operation, BIGNUM)
    return result


@app.get("/fastapi/async_cpu_bound/")
async def async_cpu_bound():
    BIGNUM = 5000000
    result = await async_cpu_operation(BIGNUM)
    return {"data": result, "message": "async mode cpu operation"}


@app.get("/fastapi/sync_cpu_bound/")
def sync_cpu_bound():
    BIGNUM = 5000000
    cpu_bound_operation(BIGNUM)
    return {"message": "sync mode operation"}


@app.get("/fastapi/async_cpu_bound_slow/")
async def async_cpu_bound_slow():
    BIGNUM = 5000000
    cpu_bound_operation(BIGNUM)
    return {"message": "sync mode operation but run in async mode"}
