import requests

def fetch(modulefile, modulename):
    url = f"https://filespace.neocryptix.repl.co/files/{modulefile}"
    r = requests.get(url, stream=True)
    with open(f"{modulefile}", "wb") as mod:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                mod.write(chunk)

fetch('config.json')
fetch('interpreter.py')
fetch('log.json')
fetch('docs.md')
fetch('run.neo')
fetch('log.txt')

os.remove('installer.py')