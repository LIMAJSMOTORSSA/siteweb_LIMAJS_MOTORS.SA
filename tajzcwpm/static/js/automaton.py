import os
import sys
import shutil
import re
from pathlib import Path
import subprocess
import time
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from tqdm import tqdm
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "tqdm", "colorama"])
    from tqdm import tqdm
    from colorama import Fore, Back, Style, init
    init(autoreset=True)

class HackerAnimation:
    def __init__(self):
        self.characters = string.ascii_letters + string.digits + string.punctuation

    def hacker_print(self, message, speed=0.01):
        for char in message:
            time.sleep(speed)
            print(Fore.GREEN + char, end='', flush=True)
        print()

    def matrix_effect(self, duration=3):
        end_time = time.time() + duration
        while time.time() < end_time:
            print(Fore.GREEN + ''.join(random.choice(self.characters) for _ in range(80)))
            time.sleep(0.05)
        print(Style.RESET_ALL)

    def loading_bar(self, iterable, desc=""):
        return tqdm(iterable, desc=Fore.CYAN + desc, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET))

class DjangoConverter:
    def __init__(self):
        self.animation = HackerAnimation()
        self.ignored_dirs = set(['.git', 'node_modules', 'env', 'venv', '__pycache__', 'site-packages'])
        self.project_name = self.generate_project_name()
        self.app_name = self.generate_app_name()
        self.file_types = {
            'html': ['.html', '.htm'],
            'css': ['.css', '.scss', '.sass', '.less'],
            'js': ['.js', '.ts', '.jsx', '.tsx'],
            'fonts': ['.woff', '.woff2', '.ttf', '.eot', '.otf'],
            'images': ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico'],
            'data': ['.json', '.xml', '.yaml', '.yml'],
            'media': ['.mp3', '.mp4', '.ogg', '.webm']
        }

    def generate_project_name(self):
        adjectives = ['cyber', 'quantum', 'neural', 'crypto', 'nano']
        nouns = ['nexus', 'matrix', 'pulse', 'cipher', 'core']
        return f"{random.choice(adjectives)}_{random.choice(nouns)}"

    def generate_app_name(self):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(8))

    def analyze_directory(self):
        self.animation.hacker_print("Analyzing current directory and all subdirectories...")
        file_list = {k: [] for k in self.file_types.keys()}
        total_files = 0
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs and not d.startswith('.') and 'site-packages' not in root]
            for file in files:
                total_files += 1
                file_path = Path(root) / file
                ext = file_path.suffix.lower()
                for type_name, extensions in self.file_types.items():
                    if ext in extensions:
                        file_list[type_name].append(file_path)
                        break

        self.animation.hacker_print(f"Total files found: {total_files}")
        for file_type, files in file_list.items():
            self.animation.hacker_print(f"Found {len(files)} {file_type} file(s)")
        
        html_folders = set(file.parent for file in file_list['html'])
        if html_folders:
            self.source_dir = min(html_folders, key=lambda x: len(x.parts))
            self.animation.hacker_print(f"Identified main static site folder: {self.source_dir}")
        else:
            self.source_dir = Path('.')
            self.animation.hacker_print("No HTML files found. Using current directory as source.")

        return file_list

    def create_django_project(self):
        self.animation.hacker_print(f"Initializing Django project: {self.project_name}")
        
        try:
            import django
        except ImportError:
            self.animation.hacker_print("Django not found. Installing Django...")
            subprocess.run([sys.executable, "-m", "pip", "install", "Django"], check=True)

        django_admin_path = shutil.which("django-admin")
        if not django_admin_path:
            self.animation.hacker_print("django-admin not found. Using python -m django...")
            subprocess.run([sys.executable, "-m", "django", "startproject", self.project_name], check=True)
        else:
            subprocess.run([django_admin_path, "startproject", self.project_name], check=True)

        os.chdir(self.project_name)
        self.animation.hacker_print(f"Creating Django app: {self.app_name}")
        subprocess.run([sys.executable, "manage.py", "startapp", self.app_name], check=True)

    def organize_files(self, file_list):
        self.animation.hacker_print("Organizing files into Django structure...")
        files_processed = 0
        for dir_type in ['templates'] + list(self.file_types.keys()):
            os.makedirs(f"{self.app_name}/{dir_type}", exist_ok=True)

        with ThreadPoolExecutor() as executor:
            futures = []
            for file_type, files in file_list.items():
                for file in self.animation.loading_bar(files, f"Copying {file_type} files"):
                    if file_type == 'html':
                        dest = Path(f"{self.app_name}/templates/{file.name}")
                    else:
                        dest = Path(f"{self.app_name}/static/{file_type}/{file.name}")
                    futures.append(executor.submit(self.safe_copy, file, dest))
            
            for future in as_completed(futures):
                try:
                    if future.result():
                        files_processed += 1
                except Exception as e:
                    self.animation.hacker_print(f"Error copying file: {e}")

        self.animation.hacker_print(f"Total files processed: {files_processed}")

    def safe_copy(self, src, dest):
        try:
            self.animation.hacker_print(f"Copying {src} to {dest}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            return True
        except FileNotFoundError:
            self.animation.hacker_print(f"File not found: {src}")
        except Exception as e:
            self.animation.hacker_print(f"Error copying {src} to {dest}: {e}")
        return False

    def adapt_html_files(self):
        self.animation.hacker_print("Adapting HTML files to Django templates...")
        templates_dir = Path(f"{self.app_name}/templates")
        files_processed = 0
        for html_file in self.animation.loading_bar(list(templates_dir.glob('*.html')), "Processing HTML"):
            try:
                with open(html_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                content = re.sub(r'(src|href)=["\'](.+?\.(?:css|js|png|jpg|jpeg|gif|svg|webp|ico|mp3|mp4|ogg|webm))["\']',
                                r'\1="{% static \'\2\' %}"', content)
                
                for section in ['header', 'footer', 'nav']:
                    if f'<{section}' in content:
                        content = re.sub(f'<{section}.*?>.*?</{section}>', f'{{% include "{section}.html" %}}', content, flags=re.DOTALL)
                
                with open(html_file, 'w', encoding='utf-8') as file:
                    file.write('{% load static %}\n' + content)
                
                files_processed += 1
            except Exception as e:
                self.animation.hacker_print(f"Error processing {html_file}: {e}")

        self.animation.hacker_print(f"Total HTML files processed: {files_processed}")

    def create_views_and_urls(self):
        self.animation.hacker_print("Generating Django views and URLs...")
        views_file = Path(f"{self.app_name}/views.py")
        urls_file = Path(f"{self.app_name}/urls.py")
        templates = [f.stem for f in Path(f"{self.app_name}/templates").glob('*.html')]
        
        with open(views_file, 'w', encoding='utf-8') as file:
            file.write("from django.shortcuts import render\n\n")
            for template in self.animation.loading_bar(templates, "Creating views"):
                file.write(f"def {template}_view(request):\n")
                file.write(f"    return render(request, '{template}.html')\n\n")

        with open(urls_file, 'w', encoding='utf-8') as file:
            file.write("from django.urls import path\nfrom . import views\n\nurlpatterns = [\n")
            for template in self.animation.loading_bar(templates, "Mapping URLs"):
                file.write(f"    path('{template}/', views.{template}_view, name='{template}'),\n")
            file.write("]\n")

    def setup_deployment(self):
        self.animation.hacker_print("Setting up deployment configuration...")
        requirements = [
            'Django>=3.2,<4.0',
            'gunicorn==20.1.0',
            'whitenoise==5.3.0',
            'django-compressor==3.1',
        ]
        with open('requirements.txt', 'w', encoding='utf-8') as file:
            for req in self.animation.loading_bar(requirements, "Writing requirements"):
                file.write(f"{req}\n")

        dockerfile = f"""
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "{self.project_name}.wsgi:application"]
"""
        with open('Dockerfile', 'w', encoding='utf-8') as file:
            file.write(dockerfile)

        docker_compose = """
version: '3'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
"""
        with open('docker-compose.yml', 'w', encoding='utf-8') as file:
            file.write(docker_compose)

    def update_settings(self):
        self.animation.hacker_print("Updating Django settings...")
        settings_file = Path(f"{self.project_name}/settings.py")
        with open(settings_file, 'r', encoding='utf-8') as file:
            content = file.read()

        replacements = [
            ("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['*']"),
            ("'DIRS': []", f"'DIRS': [os.path.join(BASE_DIR, '{self.app_name}', 'templates')]"),
        ]

        for old, new in self.animation.loading_bar(replacements, "Updating settings"):
            content = content.replace(old, new)

        static_config = f"""
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, '{self.app_name}', 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
"""

        content += static_config

        with open(settings_file, 'w', encoding='utf-8') as file:
            file.write(content)

    def run(self):
        self.animation.matrix_effect()
        self.animation.hacker_print("Initializing Django Converter...")
        time.sleep(1)

        steps = [
            (self.analyze_directory, "Analyzing directory structure"),
            (self.create_django_project, "Creating Django project"),
            (self.organize_files, "Organizing files"),
            (self.adapt_html_files, "Adapting HTML files"),
            (self.create_views_and_urls, "Creating views and URLs"),
            (self.setup_deployment, "Setting up deployment"),
            (self.update_settings, "Updating Django settings")
        ]

        file_list = None
        for step in self.animation.loading_bar(steps, "Overall progress"):
            func, desc = step
            self.animation.hacker_print(f"\n{desc}...")
            if func == self.analyze_directory:
                file_list = func()
            elif func == self.organize_files:
                func(file_list)
            else:
                func()
            time.sleep(0.5)

        self.animation.matrix_effect(1)
        self.animation.hacker_print(f"\nConversion complete! Project '{self.project_name}' with app '{self.app_name}' is ready.")
        self.animation.hacker_print("To run your project:")
        self.animation.hacker_print(f"1. cd {self.project_name}")
        self.animation.hacker_print("2. pip install -r requirements.txt")
        self.animation.hacker_print("3. python manage.py runserver")
        self.animation.hacker_print("Or use Docker: docker-compose up --build")

if __name__ == "__main__":
    converter = DjangoConverter()
    converter.run()