import uvicorn


if __name__ == "__main__":
    uvicorn.run("backend:app", host="localhost", port = 8000, reload=True)