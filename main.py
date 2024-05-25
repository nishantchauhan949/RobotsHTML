from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from httpx import AsyncClient
from jinja2 import Template
from uvicorn import run as unicorn_run

app = FastAPI()


async def get_robots_write_to_disk():
    """
    Function to get robots.txt from Capterra's Website and write it to disk
    :return: Capterra's status_code and robots.txt content
    """
    # URL of the robots.txt file on Capterra's website
    url = 'https://www.capterra.com/robots.txt'

    # Using asynchronous context manager to create an instance of AsyncClient
    async with AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 200:
            robots_txt = response.text
            # Writing robots.txt content to a file on the disk for subsequent at /robots
            with open('robots.txt', 'w') as robots_file:
                robots_file.write(robots_txt)

            # Returning status code and robots.txt content
            return response.status_code, robots_txt
        else:
            # Returning status code for HTTPException
            return response.status_code, None


@app.get("/")
async def read_root():
    """
    Base API, allows pre-downloading of the robots.txt file
    :return: HTMLResponse
    """
    # Calling function to get the robots.txt file and write it to disk
    await get_robots_write_to_disk()

    go_to_robots = 'Please go to /robots to read the robots.txt file.'
    template = Template('<pre>{{ go_to_robots|safe }}</pre>')
    rendered_html = template.render(go_to_robots=go_to_robots)

    return HTMLResponse(content=rendered_html)


@app.get("/robots")
async def get_robots():
    """
    Serves Capterra's robots.txt file
    :return: HTML robots.txt
    """
    filename = 'robots.txt'

    # Check if the file exists in the current directory
    file_path = Path(filename)
    if file_path.is_file():
        # Reading the robots.txt file that was written during base URL hit
        # as reading from disk will be faster than waiting for Capterra's API response
        with open(filename, 'r') as robots_file:
            robots_txt = robots_file.read()
    else:
        status_code, robots_txt = await get_robots_write_to_disk()

        # Checking if the response status code is not 200 (OK)
        if status_code != 200 or not robots_txt:
            # Raise an HTTPException with the status code and an error message
            raise HTTPException(status_code=status_code, detail='Failed to fetch robots.txt')

    # Replacing newlines ("\n") with HTML line breaks ("<br>") to format the text for HTML
    robots_html = robots_txt.replace('\n', '<br>')

    # Create a Jinja2 template to wrap the formatted robots.txt content in a <pre> tag
    template = Template('<pre>{{ robots_html|safe }}</pre>')

    rendered_html = template.render(robots_html=robots_html)

    return HTMLResponse(content=rendered_html)


if __name__ == '__main__':
    unicorn_run(app=app, host='0.0.0.0', port=8000, loop='uvloop', http='h11')
