# tasks.py
from invoke import task


@task
def uvc(c):
    """Update requirements.txt using uv compile."""
    print('Compile requirements.txt...')
    # Убедитесь, что uv доступен в PATH вашего окружения
    # или укажите полный путь, если это необходимо.
    c.run('uv pip compile pyproject.toml -o requirements.txt')
    print('Done!')


@task
def install(c):
    """Install dependencies from requirements.txt."""
    print('Installing dependencies...')
    c.run('uv pip install -r requirements.txt')
    print('Installation complete!')


@task(pre=[uvc, install])
def full_update(c):
    """Update requirements.txt and install dependencies."""
    print("Performing full update: compile and install.")
