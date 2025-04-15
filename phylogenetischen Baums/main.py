from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/get_pipeline_data/")
async def get_pipeline_data():
    try:
        phylo_data = {"tree": "example_phylo_tree_data", "message": "Pipeline success"}
        return JSONResponse(content=phylo_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


