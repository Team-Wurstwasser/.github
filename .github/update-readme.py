import os
import requests
import re

ORG_NAME = os.environ["ORG_NAME"]
README_PATH = os.environ["README_PATH"]

def fetch_repositories():
    url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page=100"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Repositories für {ORG_NAME}: {response.status_code}")
        return []
    
    repos = response.json()
    repos.sort(key=lambda x: x['name'].lower())
    return repos

def generate_markdown_table(repos):
    table = [
        "| Repository | Beschreibung | Tech |",
        "| :--- | :--- | :--- |"
    ]
    
    for repo in repos:
        if repo['name'] == ".github":
            continue
            
        name = f"`{repo['name']}`"
        description = repo['description'] if repo['description'] else "Keine Beschreibung hinterlegt"
        language = repo['language'] if repo['language'] else "k.A."
        
        table.append(f"| {name} | {description} | {language} |")
        
    return "\n".join(table)

def update_readme():
    repos = fetch_repositories()
    if not repos:
        return
        
    new_table = generate_markdown_table(repos)
    
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    pattern = r"(### 📂 Projekt-Übersicht \(Öffentliche Repositories\)\n\n).*?(\n\n---)"
    replacement = f"\\1{new_table}\\2"
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print(f"README.md unter '{README_PATH}' erfolgreich für {ORG_NAME} aktualisiert!")

if __name__ == "__main__":
    update_readme()