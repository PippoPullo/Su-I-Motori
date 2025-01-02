import instaloader
import os
from datetime import datetime
import subprocess

# Configura Instaloader
instagram = instaloader.Instaloader()
profile_name = "su.i.motorii"

# Scarica l'ultimo post
profile = instaloader.Profile.from_username(instagram.context, profile_name)
latest_post = next(profile.get_posts())

# Salva testo e immagine
post_text = latest_post.caption
image_url = latest_post.url
timestamp = latest_post.date.strftime('%Y-%m-%d_%H-%M-%S')

# Creare un file HTML per il post
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Post {timestamp}</title>
</head>
<body>
    <h1>{timestamp}</h1>
    <p>{post_text}</p>
    <img src="{image_url}" alt="Post image">
</body>
</html>
"""

# Salva il file HTML
output_dir = "./Su-I-Motori"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"post_{timestamp}.html")

with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

# Funzione per automatizzare il deploy
def deploy_to_github():
    # Directory del sito (dove si trova il file HTML generato)
    output_dir = "./Su-I-Motori"
    
    # Verifica che la directory esista
    if not os.path.exists(output_dir):
        print("Errore: la directory del sito non esiste.")
        return
    
    # Configura il messaggio di commit
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_message = f"Auto-update: {timestamp}"
    
    try:
        # Aggiunge tutti i file modificati
        subprocess.run(["git", "add", "."], cwd=output_dir, check=True)
        
        # Commit dei file
        subprocess.run(["git", "commit", "-m", commit_message], cwd=output_dir, check=True)
        
        # Push al repository remoto
        subprocess.run(["git", "push"], cwd=output_dir, check=True)
        
        print("Deploy completato con successo!")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il deploy: {e}")

# Esegui la funzione di deploy
deploy_to_github()
