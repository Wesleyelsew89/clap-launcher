import pyaudio
import audioop
import time
import subprocess
import os

VSCODE_PATH  = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")
PROJETO_PATH = r"C:\Users\wesle\OneDrive\Desktop\Projetos Pessoais\clap_launcher"
JARVIS_PATH = r"C:\Users\wesle\OneDrive\Desktop\Projetos Pessoais\J.A.R.V.I.S\Mark - III UI Lissajous"

# ─────────────────────────────────────────
#  CONFIGURAÇÕES
# ─────────────────────────────────────────

THRESHOLD = 2500   # sensibilidade (sobe se abrir sozinho, desce se não detectar)
MIN_GAP   = 0.15   # mínimo entre as duas palmas (evita eco)
MAX_GAP   = 0.4    # máximo entre as duas palmas (janela de detecção)
DEBOUNCE  = 0.12   # pausa após pico pra ignorar reverberação

# URI do Spotify — Back in Black (AC/DC)
SPOTIFY_URI = "spotify:track:08mG3Y1vljYA6bvDt4Wqkj"

# ─────────────────────────────────────────
#  AÇÕES
# ─────────────────────────────────────────

def abrir_jarvis():
    subprocess.Popen(
        ["python", "app.py"],
        cwd=JARVIS_PATH
    )

def abrir_spotify():
    subprocess.Popen(
        ["cmd", "/c", f"start {SPOTIFY_URI}"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

def abrir_vscode():
    subprocess.Popen([VSCODE_PATH, PROJETO_PATH])
    time.sleep(3)
    subprocess.Popen([
        "powershell", "-command",
        "$wshell = New-Object -ComObject wscript.shell; "
        "Start-Sleep -Milliseconds 3000; "
        "$wshell.AppActivate('Visual Studio Code'); "
        "Start-Sleep -Milliseconds 800; "
        "$wshell.SendKeys('{F11}')"
    ], creationflags=subprocess.CREATE_NO_WINDOW)

def abrir_tudo():
    print("\n🎉 Duas palmas detectadas! Abrindo tudo...\n")
    abrir_jarvis()
    abrir_spotify()
    time.sleep(3)
    abrir_vscode()

# ─────────────────────────────────────────
#  LOOP PRINCIPAL
# ─────────────────────────────────────────

def main():
    print("=" * 46)
    print("  👏  Clap Launcher  —  aguardando duas palmas")
    print("=" * 46)
    print(f"  Threshold : {THRESHOLD}  |  Janela : {MIN_GAP}s – {MAX_GAP}s")
    print("  Ctrl+C para encerrar")
    print("=" * 46 + "\n")

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )

    ultimo_clap = 0
    esperando_segundo = False

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            rms  = audioop.rms(data, 2)
            agora = time.time()

            if rms > THRESHOLD:
                if not esperando_segundo:
                    ultimo_clap = agora
                    esperando_segundo = True
                    print(f"👏 1ª palma detectada (RMS: {rms}) — aguardando 2ª...")
                    time.sleep(DEBOUNCE)

                else:
                    gap = agora - ultimo_clap

                    if gap < MIN_GAP:
                        # Eco da mesma palma — ignora
                        time.sleep(DEBOUNCE)
                        continue

                    if gap <= MAX_GAP:
                        # Segunda palma válida — dispara!
                        print(f"👏 2ª palma! (intervalo: {gap:.2f}s) ✅")
                        esperando_segundo = False
                        abrir_tudo()
                        time.sleep(2.0)  # cooldown pra não disparar de novo
                    else:
                        # Demorou demais — essa vira a nova 1ª palma
                        print(f"⏱️  Expirou ({gap:.2f}s). Reiniciando contagem...")
                        ultimo_clap = agora
                        print(f"👏 1ª palma detectada (RMS: {rms}) — aguardando 2ª...")
                        time.sleep(DEBOUNCE)

            # Reseta se ficou tempo demais esperando a segunda
            if esperando_segundo and (agora - ultimo_clap) > MAX_GAP + 0.1:
                esperando_segundo = False

    except KeyboardInterrupt:
        print("\n\nEncerrado pelo usuário.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()