from typing import Dict
import uvicorn
from fastapi import FastAPI, status
from codepod_kube.codepod_kube import main
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/", status_code=status.HTTP_201_CREATED)
def read_root() -> Dict[str, str]:
    main()
    return {"success": "codepod created successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
