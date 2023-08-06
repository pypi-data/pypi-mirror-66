import click
import pkgutil
import os
import re

@click.option('--image-name', default='dockerized-app', help='The image name and optionally a tag in the ‘name:tag’ '
                                                             'format.')
@click.option('--port', type=int, default=-1, help='The port on which your application has been configured to run. '
                                                   '(Your application will be exposed on the same port.)')
@click.option('--app-type', required=True, help='The type of app (FLASK, NODE_JS, SPRING_BOOT).')
@click.command()
def cli(image_name, port, app_type):
    """Main cli"""
    # Port was not passed in argument, set default values based on app_type
    if (port == -1):
        if (app_type == 'FLASK'):
            port = 5000
        else:
            port = 8080

    if(app_type == 'NODE_JS'):
        handle_nodejs(image_name, port)
    elif(app_type == 'SPRING_BOOT'):
        handle_java_spring_boot(image_name, port)
    elif(app_type == 'FLASK'):
        handle_python_flask(image_name, port)

def handle_java_spring_boot(image_name, port):
    # Generate Dockerfile
    click.echo('Generating Dockerfile...')
    if (not os.path.exists('target')):
        click.echo('No target/ present')
        exit(1)
    found_file = ''
    for filename in os.listdir('target/'):
        if re.search('.*\.jar', filename):
            found_file = filename
            break
    if (found_file == ''):
        click.echo('No jar file present. Make sure your target/ contains a jar file')
        exit(1)
    text = pkgutil.get_data(__name__, "templates/Java.Dockerfile").decode()

    open("Dockerfile", "w").writelines([l for l in text])
    click.echo('Dockerfile generated')

    # Build Docker image
    click.echo('Building Docker image...')
    os.system('docker build -t {} .'.format(image_name))
    click.echo('Built image {}'.format(image_name))

    # Run Docker image
    click.echo('Running Docker image...')
    os.system('docker run -it -p {}:{} {}'.format(port, port, image_name))

def handle_python_flask(image_name, port):
    python_entrypoint_file = 'app.py'

    # Generate Dockerfile
    click.echo('Generating Dockerfile...')
    python_entrypoint_file = click.prompt('Enter python entrypoint file')
    os.environ["FLASK_ENTRYPOINT_FILE"] = python_entrypoint_file
    text = pkgutil.get_data(__name__, "templates/Python-Flask.Dockerfile").decode()

    open("Dockerfile", "w").writelines([l for l in text])
    click.echo('Dockerfile generated')

    # Build Docker image
    click.echo('Building Docker image...')
    os.system('docker build -t {} --build-arg FLASK_ENTRYPOINT_FILE={} .'.format(image_name, python_entrypoint_file))
    click.echo('Built image {}'.format(image_name))

    # Run Docker image
    click.echo('Running Docker image...')
    os.system('docker run -it -p {}:{} {}'.format(port, port, image_name))

def handle_nodejs(image_name, port):
    # Generate Dockerfile
    click.echo('Generating Dockerfile...')
    text = pkgutil.get_data(__name__, "templates/NodeJS.Dockerfile").decode()
    open("Dockerfile", "w").writelines([l for l in text])
    click.echo('Dockerfile generated')

    # Build Docker image
    click.echo('Building Docker image...')
    os.system('docker build -t {} .'.format(image_name))
    click.echo('Built image {}'.format(image_name))

    # Run Docker image
    click.echo('Running Docker image...')
    os.system('docker run -it -p {}:{} {}'.format(port, port, image_name))
