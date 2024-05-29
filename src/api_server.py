from fastapi import FastAPI

app = FastAPI()


""" 
@app.post()
@app.put()
@app.delete()
@app.options()
@app.head()
@app.patch()
@app.trace()a
"""

@app.post("/start-session")
async def start_session():
    manager = app.manager
    await manager.temp_test()
    