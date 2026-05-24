# 👏 Clap Launcher

Bata duas palmas e o sistema abre o que você quiser automaticamente.

## O que faz

Fica escutando o microfone em segundo plano. Quando detecta duas palmas rápidas, abre o VS Code no seu projeto e toca uma música no Spotify.

---

## Requisitos

- Windows 10/11
- Python 3.11 → [download aqui](https://www.python.org/downloads/release/python-3119/)
  - Durante a instalação, marca **"Add Python to PATH"**

---

## Instalação

**1. Clona o repositório**
```bash
git clone https://github.com/Wesleyelsew89/clap-launcher
cd clap-launcher
```

**2. Instala a dependência**
```bash
py -3.11 -m pip install pyaudio
```

---

## Configuração

Abre o `clap_launcher.py` e edita as linhas no topo:

**Pasta do projeto no VS Code:**
```python
PROJETO_PATH = r"C:\caminho\para\sua\pasta"
```

**Música do Spotify:**
1. Abre o Spotify e vai na música que quer
2. Clica com botão direito → **Compartilhar** → **Copiar link da música**
3. O link vai ser algo como `https://open.spotify.com/track/08mG3Y1vljYA6bvDt4Wqkj`
4. Pega só o ID (a parte depois de `/track/`) e coloca assim:
```python
SPOTIFY_URI = "spotify:track:SEU_ID_AQUI"
```

---

## Como rodar

```bash
py -3.11 clap_launcher.py
```

Para rodar invisível no início do Windows, veja a seção abaixo.

---

## Iniciar com o Windows (opcional)

1. Cria um arquivo `iniciar.bat` na pasta do projeto:
```bat
@echo off
pythonw "C:\caminho\completo\clap_launcher.py"
```
2. Aperta `Win + R`, digita `shell:startup` e dá Enter
3. Cria um atalho do `iniciar.bat` e cola nessa pasta

Pronto — vai subir sozinho com o PC sem abrir janela nenhuma.

---

## Ajuste de sensibilidade

Se não detectar suas palmas ou disparar com ruído, edita no topo do arquivo:

```python
THRESHOLD = 2500  # aumenta se abrir sozinho, diminua se não detectar
MAX_GAP   = 0.4   # janela de tempo entre as duas palmas (segundos)
```