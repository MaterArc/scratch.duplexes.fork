import aiohttp
import asyncio
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

async def send_request(session, username, id):
    try:
        async with session.get(f"https://cbzbf9.deta.dev/{username}/{id}", timeout=3):  # Don't await the response.text() method
            pass  # Do nothing
    except asyncio.TimeoutError:  # Catch the TimeoutError exception
        print("TimeoutError occurred")  # Handle the exception

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects', methods=['GET'])
async def projects():
    # Get the username and id from the url
    username = request.args.get('author')
    id = request.args.get('project_id')
    print(username, id)
    # Send the requests asynchronously
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(500):
            task = asyncio.create_task(send_request(session, username, id))
            tasks.append(task)
        await asyncio.gather(*tasks)
    return render_template('index.html', message='Successfully sent views to the project!')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)