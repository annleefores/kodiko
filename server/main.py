from typing import Union, Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root(name: str = "Annlee") -> Dict[str, str]:
    return {"Hello": name}
