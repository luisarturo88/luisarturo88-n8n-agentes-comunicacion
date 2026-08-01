# optimize_blogger_colab.py
"""
Script preparado para ejecutarse en Google Colab: "Optimización masiva de entradas de Blogger".

Instrucciones rápidas:
- Pega este script en una celda de Colab o súbelo como archivo y ejecútalo en Colab.
- Por seguridad el script está pensado para ejecutarse en modo PRUEBA (TEST_MODE=True) por defecto.
- Si prefieres ejecutar el flujo OAuth con client_secret.json, sube ese archivo y sigue las instrucciones descritas abajo.

Este archivo contiene las funciones principales para autenticar con la API de Blogger, generar e insertar
JSON-LD (BlogPosting), meta-descriptions, asegurar H2 con preguntas y mejorar el tono de los párrafos.

ADVERTENCIA: Revisa siempre los previews generados en modo prueba antes de publicar cambios.
"""

# NOTA: este script está pensado para ejecutarse en Colab. Algunas líneas (como la instalación de paquetes)
# se han dejado en forma de comandos que en Colab deben ejecutarse en celdas separadas (o usando !pip).

# Ejemplo de uso en Colab (pegar en una celda y ejecutar):
# 1) !pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib beautifulsoup4 lxml tqdm
# 2) from optimize_blogger_colab import run_from_colab; run_from_colab()

from google.colab import auth
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from bs4 import BeautifulSoup, Comment
from datetime import datetime
from tqdm import tqdm
import json, re, textwrap, os, traceback

# ------------------ CONFIGURACIÓN ------------------
DEFAULT_BLOG_ID = "2772493032989228627"
DEFAULT_TEST_MODE = True  # True = simulación (no publica los cambios)
DEFAULT_MIN_H2 = 3
DEFAULT_PROCESS_LIMIT = None
# ---------------------------------------------------

# ---------- AUTENTICACIÓN -------------
def try_colab_auth(BLOG_ID, scopes=['https://www.googleapis.com/auth/blogger']):
    try:
        print("Iniciando auth.authenticate_user() (Colab). Sigue el flujo que aparece.")
        auth.authenticate_user()
        creds, _ = google.auth.default(scopes=scopes)
        service = build('blogger', 'v3', credentials=creds, cache_discovery=False)
        blog = service.blogs().get(blogId=BLOG_ID).execute()
        print("Acceso OK. Título del blog:", blog.get('name'))
        return service
    except HttpError as he:
        raise he
    except Exception:
        traceback.print_exc()
        raise


def oauth_client_flow(client_secret_path, BLOG_ID, scopes=['https://www.googleapis.com/auth/blogger']):
    if not os.path.exists(client_secret_path):
        raise FileNotFoundError(f"No encontré {client_secret_path} en este entorno. Súbelo en el panel Files.")
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes)
    print("Se abrirá una URL. Sigue las instrucciones y pega el código que te proporcionen.")
    creds = flow.run_console()
    service = build('blogger', 'v3', credentials=creds, cache_discovery=False)
    blog = service.blogs().get(blogId=BLOG_ID).execute()
    print("Acceso OK con client_secret.json. Título del blog:", blog.get('name'))
    return service


def authenticate_prefer_colab(BLOG_ID, client_secret_path=None):
    scopes = ['https://www.googleapis.com/auth/blogger']
    try:
        service = try_colab_auth(BLOG_ID, scopes=scopes)
        return service
    except HttpError as he:
        err_str = str(he)
        if 'insufficientPermissions' in err_str or he.resp.status == 403:
            print("\nERROR: insufficientPermissions. Posibles soluciones:")
            print("- Reinicia el runtime (Entorno de ejecución -> Reiniciar el entorno de ejecución) y vuelve a ejecutar esta celda,\n  luego autoriza de nuevo (asegúrate de seleccionar la cuenta correcta).")
            print("- Si tu cuenta es Google Workspace y los scopes están bloqueados, usa client_secret.json (llama a oauth_client_flow).")
            raise he
        else:
            traceback.print_exc()
            raise

# ------------ UTILIDADES ---------------

def short_text_summary(text, max_chars=150):
    text = re.sub(r'\s+', ' ', (text or '').strip())
    if not text:
        return ""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    summary = ""
    for s in sentences:
        if len(summary) + len(s) <= max_chars:
            summary += (s + " ")
        else:
            break
    if not summary:
        summary = textwrap.shorten(text, width=max_chars, placeholder="...")
    return summary.strip()


def generate_meta_description(title, plain_text):
    base = f"{title} - {short_text_summary(plain_text, max_chars=120)}"
    base = re.sub(r'\s+', ' ', base).strip()
    if len(base) < 150:
        add = short_text_summary(plain_text, max_chars=160 - len(base))
        candidate = (base + " " + add).strip()
    else:
        candidate = base[:160].rsplit(' ', 1)[0]
    return candidate[:160]


def extract_plain_text_from_html(html):
    soup = BeautifulSoup(html or "", 'html.parser')
    for el in soup(['script','style']):
        el.decompose()
    text = soup.get_text(separator=' ', strip=True)
    return re.sub(r'\s+', ' ', text)


def find_first_image(html):
    soup = BeautifulSoup(html or "", 'html.parser')
    img = soup.find('img')
    if img and img.get('src'):
        return img.get('src')
    return None


def build_jsonld(post):
    title = post.get('title','')
    url = post.get('url','')
    published = post.get('published')
    updated = post.get('updated') or published
    author = post.get('author',{}).get('displayName','Autor')
    content = post.get('content','')
    image = find_first_image(content)
    plain = extract_plain_text_from_html(content)
    meta_desc = post.get('customMetaDescription') or short_text_summary(plain, max_chars=160)
    jsonld = {
        "@context":"https://schema.org",
        "@type":"BlogPosting",
        "headline": title,
        "mainEntityOfPage": {"@type":"WebPage", "@id": url},
        "datePublished": published,
        "dateModified": updated,
        "author": {"@type":"Person","name": author},
        "description": meta_desc
    }
    if image:
        jsonld["image"] = {"@type":"ImageObject","url": image}
    return jsonld


def improve_tone_simple(text):
    if not text:
        return text
    text = re.sub(r'\s+', ' ', text).strip()
    replacements = [
        (r'\b(es importante|es recomendable|es necesario)\b', r'Es importante:'),
        (r'\b[Pp]or ejemplo\b', r'Por ejemplo,'),
        (r'\b(se puede|puede)\b', r'puedes'),
        (r'\b(se recomienda|recomiendo)\b', r'recomiendo'),
        (r'\b(además)\b', r'Además,'),
    ]
    for pat, rep in replacements:
        text = re.sub(pat, rep, text)
    sentences = re.split(r'([.!?])\s*', text)
    combined = []
    for i in range(0, len(sentences)-1, 2):
        s = sentences[i].strip()
        p = sentences[i+1]
        sentence = (s + p).strip()
        if len(sentence) > 220:
            subs = s.split(',')
            for sub in subs:
                sub = sub.strip()
                if sub:
                    combined.append(sub + '.')
        else:
            combined.append(sentence)
    if len(sentences) % 2 == 1:
        tail = sentences[-1].strip()
        if tail:
            combined.append(tail)
    final = " ".join(combined)
    final = re.sub(r'\s+,', ',', final)
    final = re.sub(r'\s+\.', '.', final)
    if final and final[0].islower():
        final = final[0].upper() + final[1:]
    return final


def ensure_h2_questions(soup, title, min_q=3):
    existing_h2 = soup.find_all('h2')
    if len(existing_h2) >= min_q:
        return soup
    short_title = re.sub(r'[^A-Za-z0-9ÁÉÍÓÚáéíóúÑñ\s\-]', '', title).strip() or "este tema"
    q_candidates = [
        f"¿Qué es {short_title}?,",
        f"¿Cómo funciona {short_title}?",
        f"¿Por qué {short_title} es importante?",
        f"¿Cómo aplicar {short_title} en la práctica?",
        f"Consejos prácticos sobre {short_title}.",
    ]
    plain = extract_plain_text_from_html(str(soup))
    sentences = re.split(r'(?<=[.!?])\s+', plain)
    if len(sentences) >= 3:
        answers = [
            short_text_summary(" ".join(sentences[:2]), max_chars=400),
            short_text_summary(" ".join(sentences[2:4]) if len(sentences)>=4 else " ".join(sentences[1:3]), max_chars=400),
            short_text_summary(" ".join(sentences[4:6]) if len(sentences)>=6 else " ".join(sentences[-2:]), max_chars=400)
        ]
    else:
        answers = [short_text_summary(plain, max_chars=400)] * 3
    answers = [improve_tone_simple(a) for a in answers]
    fragment_html = ""
    for i in range(min_q):
        q = q_candidates[i] if i < len(q_candidates) else q_candidates[0]
        a = answers[i] if i < len(answers) else short_text_summary(plain, max_chars=300)
        fragment_html += f"<h2>{q}</h2>\n<p>{a}</p>\n"
    fragment_soup = BeautifulSoup(fragment_html, 'html.parser')
    for el in reversed(fragment_soup.contents):
        soup.insert(0, el)
    return soup

# ------------ PROCESAMIENTO DE POSTS ------------
def process_all_posts(service, blog_id, test_mode=True, min_question_h2=3, limit=None):
    report = {"total_found":0, "modified":[], "failed":[]}
    posts = []
    try:
        request = service.posts().list(blogId=blog_id, fetchBodies=True, maxResults=100)
        while request:
            resp = request.execute()
            items = resp.get('items', [])
            posts.extend(items)
            request = service.posts().list_next(request, resp)
            if limit and len(posts) >= limit:
                posts = posts[:limit]
                break
    except HttpError as he:
        print("Error listando posts:")
        traceback.print_exc()
        raise he
    report['total_found'] = len(posts)
    iterator = tqdm(posts, desc="Procesando entradas") if posts else []
    preview_dir = "/content/optimizado_preview"
    if test_mode:
        os.makedirs(preview_dir, exist_ok=True)
    for post in iterator:
        try:
            post_id = post.get('id')
            title = post.get('title','')
            original_content = post.get('content','') or ''
            plain = extract_plain_text_from_html(original_content)
            soup = BeautifulSoup(original_content, 'html.parser')
            if not soup.find('script', attrs={'type':'application/ld+json'}):
                jsonld = build_jsonld(post)
                script_tag = soup.new_tag('script', type='application/ld+json')
                script_tag.string = json.dumps(jsonld, ensure_ascii=False, indent=2)
                soup.insert(0, script_tag)
            meta_exists = bool(soup.find('meta', attrs={'name': re.compile(r'description', re.I)})) or re.search(r'<!--\s*meta-description\s*:', str(soup), re.I)
            if not meta_exists:
                meta_desc = generate_meta_description(title, plain)
                comment_node = soup.new_string(f" meta-description: {meta_desc} ", Comment=True)
                meta_tag = soup.new_tag('meta', attrs={'name':'description','content':meta_desc})
                soup.insert(0, meta_tag)
                soup.insert(0, comment_node)
                post['customMetaDescription'] = meta_desc
            soup = ensure_h2_questions(soup, title, min_q=min_question_h2)
            for p in soup.find_all('p'):
                text = p.get_text(separator=' ', strip=True)
                improved = improve_tone_simple(text)
                if improved and improved != text:
                    p.clear()
                    p.append(improved)
            final_html = str(soup)
            if test_mode:
                safe_title = re.sub(r'[^0-9A-Za-z\-_]', '_', title)[:60] or post_id
                filename_html = os.path.join(preview_dir, f"{post_id}_{safe_title}.html")
                with open(filename_html, "w", encoding="utf-8") as f:
                    f.write(final_html)
                metadata = {"post_id": post_id, "title": title, "url": post.get('url'), "meta_description": post.get('customMetaDescription', generate_meta_description(title, plain)), "preview_file": filename_html}
                with open(os.path.join(preview_dir, f"{post_id}_meta.json"), "w", encoding="utf-8") as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                report['modified'].append({"post_id": post_id, "title": title, "action": "simulated", "preview": metadata['preview_file']})
            else:
                update_body = {"id": post_id, "title": post.get('title'), "content": final_html, "labels": post.get('labels', [])}
                updated = service.posts().update(blogId=blog_id, postId=post_id, body=update_body).execute()
                report['modified'].append({"post_id": post_id, "title": title, "action": "updated", "url": updated.get('url')})
        except Exception as e:
            report['failed'].append({"post_id": post.get('id'), "title": post.get('title'), "error": str(e)})
    return report

# ---------- WRAPPER PARA USO EN COLAB -------------
def run_from_colab(BLOG_ID=DEFAULT_BLOG_ID, TEST_MODE=DEFAULT_TEST_MODE, MIN_H2=DEFAULT_MIN_H2, LIMIT=DEFAULT_PROCESS_LIMIT):
    print("Autenticando y preparando servicio...")
    try:
        service = authenticate_prefer_colab(BLOG_ID)
    except Exception as e:
        print("Autenticación Colab falló o requiere acción. Si tienes client_secret.json sube el archivo y usa oauth_client_flow.")
        raise
    print(f"Blog ID: {BLOG_ID} | Modo prueba: {TEST_MODE}")
    report = process_all_posts(service, BLOG_ID, test_mode=TEST_MODE, min_question_h2=MIN_H2, limit=LIMIT)
    print("\n--- Informe final ---")
    print("Entradas encontradas:", report['total_found'])
    print("Entradas modificadas:", len(report['modified']))
    print("Entradas con error:", len(report['failed']))
    if TEST_MODE:
        print("Previews guardados en: /content/optimizado_preview/")
    return report

if __name__ == '__main__':
    print('Este script está pensado para usarse desde Google Colab. Importa run_from_colab() y ejecútalo allí.')
