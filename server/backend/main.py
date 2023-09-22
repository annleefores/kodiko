from typing import Dict
from fastapi import FastAPI, HTTPException, status
from dotenv import load_dotenv
import uvicorn

load_dotenv()

from codepod_kube.codepod_kube import create


app = FastAPI()


@app.get("/create", status_code=status.HTTP_201_CREATED)
def create_codepod() -> Dict[str, str]:
    try:
        create()
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail="Codepod creation failed")

    return {"success": "codepod created successfully"}


@app.get("/delete", status_code=status.HTTP_201_CREATED)
def delete_codepod() -> Dict[str, str]:
    # create()
    return {"success": "codepod deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
