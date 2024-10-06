from langchain_community.document_loaders import GithubFileLoader
from app.config import settings
import requests


def get_params_from_url(url):
    url_parts = url.split('/')
    repo_owner = url_parts[3]
    repo_name = url_parts[4]
    branch_and_file_path = '/'.join(url_parts[6:])
    branch_name, file_path = branch_and_file_path.split('/', 1)
    params_url_github = {
        'owner': repo_owner,
        'repo': repo_name,
        'branch': branch_name,
        'file_path': file_path,
        'branch_file_fath': branch_and_file_path,
        'repo_path': f'{repo_owner}/{repo_name}',
    }
    return params_url_github


def get_file_from_github(url):
    github = get_params_from_url(url)
    new_url = f"https://raw.githubusercontent.com/{github['owner']}/{github['repo']}/{github['branch']}/{github['file_path']}"
    response = requests.get(new_url)
    if response.status_code == 200:
        return response
    else:
        print(
            f"حدث خطأ أثناء الحصول على الملف. حالة الاستجابة: {response.status_code}"
        )
        return []


def GithubFileLoader_folder(url, file_filter='.md'):
    github = get_params_from_url(url)
    loader = GithubFileLoader(
        repo=github['repo_path'],
        branch=github['branch'],
        access_token=settings.github_token,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: file_path.endswith(file_filter),
    )
    documents = loader
    return documents


def GithubFileLoader_singleFile(url):
    github = get_params_from_url(url)
    # استخراج اسم الملف من الجزء الأخير من الرابط
    # file_name = github['file_path'].split('/')[
    file_name = github['file_path']  # آخر جزء في المسار هو اسم الملف
    loader = GithubFileLoader(
        repo=github['repo_path'],
        branch=github['branch'],
        access_token=settings.github_token,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: file_path.endswith(file_name),
    )
    documents = loader
    return documents


def GithubFileLoader_listFiles(url, file_list):
    github = get_params_from_url(url)
    loader = GithubFileLoader(
        repo=github['repo_path'],
        branch=github['branch'],
        access_token=settings.github_token,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: any(
            file_path.endswith(f)
            for f in file_list)  # فلترة لتحميل الملفات المحددة
    )
    documents = loader
    return documents


def GithubFileLoader_file(url):
    loader = GithubFileLoader_folder(url)
    documents = loader
    return documents
