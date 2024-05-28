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

@app.get("/")
async def root():
    print("hello")
    return {"message": "Hello World"}