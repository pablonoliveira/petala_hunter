from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
import yt_dlp
import os
import uuid
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'creativehunter-2026'
socketio = SocketIO(app, cors_allowed_origins="*")

PASTA_DOWNLOADS = 'downloads'
downloads_status = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    mensagem = None
    arquivos = []

    if request.method == 'POST':
        # Garante que só processa se o request veio de um submit real
        url = (request.form.get('url') or '').strip()
        tipo = request.form.get('tipo') or 'video'

        # Se não tem URL, NÃO dispara download
        if url:
            download_id = str(uuid.uuid4())[:8]
            tipo_nome = "Vídeo/Reel" if tipo == 'video' else "Imagem/Post"
            mensagem = f'CreativeHunter · {tipo_nome} {download_id} iniciado...'
            threading.Thread(
                target=baixar_com_progresso,
                args=(download_id, url, tipo),
                daemon=True
            ).start()
        else:
            # Nada de usar cache antigo: apenas mensagem suave
            mensagem = "Cole um link para iniciar um novo download."

    if os.path.exists(PASTA_DOWNLOADS):
        arquivos = sorted(os.listdir(PASTA_DOWNLOADS), reverse=True)[:12]

    return render_template('index.html', mensagem=mensagem, arquivos=arquivos)


def baixar_com_progresso(download_id, url, tipo='video'):
    status = {
        'status': '🔍 CreativeHunter analisando...',
        'progress': 0,
        'filename': 'Detectando criativo...'
    }
    downloads_status[download_id] = status
    socketio.emit('download_start', {'download_id': download_id})

    def progress_hook(d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%')
            try:
                percent_num = float(
                    percent_str.replace('%', '').replace('N/A', '0')
                )
            except Exception:
                percent_num = 0.0

            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', '?')
            filename = d.get('filename', 'Baixando...')

            status.update({
                'status': f'{percent_str} | {speed} | ETA: {eta}',
                'progress': percent_num,
                'filename': os.path.basename(filename)
            })
            socketio.emit('progress_update', status)

        elif d['status'] == 'finished':
            status.update({
                'status': '✅ Criativo salvo na pasta downloads/',
                'progress': 100,
                'filename': os.path.basename(d.get('filename', 'Arquivo'))
            })
            socketio.emit('progress_update', status)
            socketio.emit('download_complete')

    playlist_opts = {
        'extract_flat': False,
        'noplaylist': False,
    }

    if tipo == 'imagem':
        ydl_opts = {
            'outtmpl': os.path.join(
                PASTA_DOWNLOADS, '[%(uploader)s] %(title)s.%(ext)s'
            ),
            'format': 'image*+bestaudio/bestimage/best',
            'progress_hooks': [progress_hook],
            **playlist_opts
        }
    else:
        ydl_opts = {
            'outtmpl': os.path.join(
                PASTA_DOWNLOADS, '[%(uploader)s] %(title)s.%(ext)s'
            ),
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'progress_hooks': [progress_hook],
            **playlist_opts
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if isinstance(info, dict) and 'entries' in info and info['entries']:
                total = len([e for e in info['entries'] if e])
                status['status'] = f'✅ {total} criativos salvos!'
                socketio.emit('progress_update', status)

    except Exception as e:
        status['status'] = f'❌ Erro CreativeHunter: {str(e)[:70]}'
        socketio.emit('progress_update', status)
        socketio.emit('download_error')

    finally:
        threading.Timer(
            10.0, lambda: downloads_status.pop(download_id, None)
        ).start()


@socketio.on('connect')
def handle_connect():
    for status in downloads_status.values():
        emit('progress_update', status)


@app.route('/download/<path:filename>')
def download(filename):
    safe_name = os.path.basename(filename)
    return send_from_directory(PASTA_DOWNLOADS, safe_name, as_attachment=True)


@app.route('/api/files')
def get_files():
    if os.path.exists(PASTA_DOWNLOADS):
        files = sorted(os.listdir(PASTA_DOWNLOADS), reverse=True)[:12]
        return jsonify(
            [f for f in files if os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))]
        )
    return jsonify([])


if __name__ == '__main__':
    os.makedirs(PASTA_DOWNLOADS, exist_ok=True)
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('DEBUG', 'False') == 'True'
    
    print(f"🔥 CreativeHunter rodando em porta {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=debug_mode)
