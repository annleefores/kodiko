from typing import Union, Dict
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root(name: str) -> Dict[str, str]:
    return {"Hello": name}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
