import sys
import os
import zipfile
import shutil
import requests
from packaging.version import Version

from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QPropertyAnimation,
    QEasingCurve, QSize
)
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QWidget, QGraphicsOpacityEffect
)

# ── Configurações ──────────────────────────────────────────────────────────────

CURRENT_VERSION = "0.0.1"
GITHUB_REPO     = "minimusic-app/minimusic"
RELEASES_URL    = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


# ── Worker: roda em background ─────────────────────────────────

class UpdateChecker(QThread):
    """Verifica a versão remota sem bloquear a thread principal."""
    update_available = pyqtSignal(str, str, str)  # tag, url_download, notas
    no_update        = pyqtSignal()
    check_failed     = pyqtSignal(str)

    def run(self):
        try:
            r = requests.get(RELEASES_URL, timeout=6)
            r.raise_for_status()
            data     = r.json()
            tag      = data.get("tag_name", "")
            notes    = data.get("body", "Sem notas de versão.")[:400]
            assets   = data.get("assets", [])
            dl_url   = next(
                (a["browser_download_url"] for a in assets if a["name"].endswith(".zip")),
                None
            )

            remote = tag.lstrip("v")
            if Version(remote) > Version(CURRENT_VERSION) and dl_url:
                self.update_available.emit(tag, dl_url, notes)
            else:
                self.no_update.emit()

        except Exception as e:
            self.check_failed.emit(str(e))


class UpdateDownloader(QThread):
    """Faz o download + extração reportando progresso."""
    progress  = pyqtSignal(int)    # 0-100
    finished  = pyqtSignal()
    failed    = pyqtSignal(str)

    def __init__(self, url: str, asset_name: str):
        super().__init__()
        self.url        = url
        self.asset_name = asset_name

    def run(self):
        try:
            tmp = os.path.join(os.path.expanduser("~"), ".tmp_update")
            os.makedirs(tmp, exist_ok=True)
            zip_path = os.path.join(tmp, self.asset_name)

            r     = requests.get(self.url, stream=True, timeout=60)
            total = int(r.headers.get("content-length", 0))
            done  = 0

            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
                    done += len(chunk)
                    if total:
                        self.progress.emit(int(done / total * 90))

            # Extrai ao lado do executável
            app_dir = os.path.dirname(sys.executable)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(app_dir)

            self.progress.emit(100)
            shutil.rmtree(tmp, ignore_errors=True)
            self.finished.emit()

        except Exception as e:
            self.failed.emit(str(e))


# ── Diálogo principal ──────────────────────────────────────────────────────────

class UpdateDialog(QDialog):
    DARK_BG     = "#111114"
    CARD_BG     = "#18181c"
    ACCENT      = "#7C6FEB"   
    ACCENT_DARK = "#5a4fcf"
    TEXT_PRI    = "#EEEEF0"
    TEXT_SEC    = "#8888A0"
    BORDER      = "#2a2a35"
    SUCCESS     = "#3ecf8e"

    def __init__(self, tag: str, dl_url: str, notes: str, parent=None):
        super().__init__(parent)
        self.tag     = tag
        self.dl_url  = dl_url
        self.notes   = notes
        self.asset   = dl_url.split("/")[-1]

        self.setWindowTitle("Atualização disponível")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(420)

        self._build_ui()
        self._apply_styles()
        self._fade_in()

    # ── Construção da UI ───────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.card = QWidget()
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(28, 28, 28, 24)
        card_layout.setSpacing(0)

        # — Cabeçalho ─────────────────────────────────────────────────────────
        header = QHBoxLayout()

        badge = QLabel("NOVO")
        badge.setObjectName("badge")
        badge.setFixedHeight(20)

        self.title_lbl = QLabel(f"Versão {self.tag} disponível")
        self.title_lbl.setObjectName("title")
        self.title_lbl.setWordWrap(True)

        close_btn = QPushButton("✕")
        close_btn.setObjectName("close_btn")
        close_btn.setFixedSize(28, 28)
        close_btn.clicked.connect(self.reject)

        header.addWidget(badge)
        header.addStretch()
        header.addWidget(close_btn)

        card_layout.addLayout(header)
        card_layout.addSpacing(12)
        card_layout.addWidget(self.title_lbl)
        card_layout.addSpacing(4)

        # Versão atual
        cur = QLabel(f"Você tem a {CURRENT_VERSION}")
        cur.setObjectName("subtitle")
        card_layout.addWidget(cur)
        card_layout.addSpacing(16)

        # — Notas de versão ───────────────────────────────────────────────────
        notes_label = QLabel(self.notes)
        notes_label.setObjectName("notes")
        notes_label.setWordWrap(True)
        notes_label.setMaximumHeight(100)
        card_layout.addWidget(notes_label)
        card_layout.addSpacing(24)

        # — Barra de progresso (oculta no início) ─────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progress")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()

        self.progress_lbl = QLabel("Baixando…")
        self.progress_lbl.setObjectName("subtitle")
        self.progress_lbl.hide()

        card_layout.addWidget(self.progress_lbl)
        card_layout.addSpacing(8)
        card_layout.addWidget(self.progress_bar)
        card_layout.addSpacing(8)

        # — Botões ─────────────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.skip_btn = QPushButton("Agora não")
        self.skip_btn.setObjectName("skip_btn")
        self.skip_btn.clicked.connect(self.reject)

        self.update_btn = QPushButton("Atualizar agora")
        self.update_btn.setObjectName("update_btn")
        self.update_btn.clicked.connect(self._start_download)

        btn_row.addWidget(self.skip_btn)
        btn_row.addWidget(self.update_btn)
        card_layout.addLayout(btn_row)

        root.addWidget(self.card)

    # ── Estilos ────────────────────────────────────────────────────────────────

    def _apply_styles(self):
        self.setStyleSheet(f"""
            QDialog {{ background: transparent; }}

            #card {{
                background: {self.CARD_BG};
                border: 1px solid {self.BORDER};
                border-radius: 16px;
            }}

            #badge {{
                background: {self.ACCENT}22;
                color: {self.ACCENT};
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                padding: 2px 8px;
                border-radius: 4px;
            }}

            #title {{
                font-size: 17px;
                font-weight: 600;
                color: {self.TEXT_PRI};
            }}

            #subtitle {{
                font-size: 12px;
                color: {self.TEXT_SEC};
            }}

            #notes {{
                font-size: 13px;
                color: {self.TEXT_SEC};
                line-height: 1.6;
                background: {self.DARK_BG};
                border-radius: 8px;
                padding: 10px 12px;
            }}

            #close_btn {{
                background: transparent;
                color: {self.TEXT_SEC};
                border: none;
                font-size: 14px;
                border-radius: 6px;
            }}
            #close_btn:hover {{ background: {self.BORDER}; color: {self.TEXT_PRI}; }}

            #skip_btn {{
                background: transparent;
                color: {self.TEXT_SEC};
                border: 1px solid {self.BORDER};
                border-radius: 8px;
                padding: 9px 20px;
                font-size: 13px;
            }}
            #skip_btn:hover {{ border-color: {self.ACCENT}; color: {self.TEXT_PRI}; }}

            #update_btn {{
                background: {self.ACCENT};
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 9px 20px;
                font-size: 13px;
                font-weight: 600;
            }}
            #update_btn:hover  {{ background: {self.ACCENT_DARK}; }}
            #update_btn:disabled {{ background: {self.BORDER}; color: {self.TEXT_SEC}; }}

            QProgressBar#progress {{
                background: {self.BORDER};
                border-radius: 3px;
                border: none;
            }}
            QProgressBar#progress::chunk {{
                background: {self.ACCENT};
                border-radius: 3px;
            }}
        """)

    # ── Animação de entrada ────────────────────────────────────────────────────

    def _fade_in(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(200)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    # ── Download ───────────────────────────────────────────────────────────────

    def _start_download(self):
        self.update_btn.setEnabled(False)
        self.update_btn.setText("Baixando…")
        self.skip_btn.hide()
        self.progress_bar.show()
        self.progress_lbl.show()

        self._downloader = UpdateDownloader(self.dl_url, self.asset)
        self._downloader.progress.connect(self._on_progress)
        self._downloader.finished.connect(self._on_finished)
        self._downloader.failed.connect(self._on_failed)
        self._downloader.start()

    def _on_progress(self, pct: int):
        self.progress_bar.setValue(pct)
        self.progress_lbl.setText(f"Baixando… {pct}%")

    def _on_finished(self):
        self.progress_lbl.setText("Atualização concluída!")
        self.update_btn.setEnabled(True)
        self.update_btn.setText("Reiniciar agora")
        self.update_btn.setStyleSheet(
            f"background: {self.SUCCESS}; color: #000; border-radius: 8px;"
            f"padding: 9px 20px; font-size: 13px; font-weight: 600;"
        )
        self.update_btn.clicked.disconnect()
        self.update_btn.clicked.connect(self._restart)

    def _on_failed(self, msg: str):
        self.progress_lbl.setText(f"Erro: {msg}")
        self.update_btn.setEnabled(True)
        self.update_btn.setText("Tentar novamente")
        self.update_btn.clicked.disconnect()
        self.update_btn.clicked.connect(self._start_download)
        self.skip_btn.show()

    def _restart(self):
        self.accept()
        os.execv(sys.executable, [sys.executable] + sys.argv)


# ── Função pública — chame no MainWindow ───────────────────────────────────────

def check_for_updates_async(parent=None):
    """
    Dispara a verificação em background.
    Se houver update, abre o UpdateDialog automaticamente.

    Uso no MainWindow:
        def __init__(self):
            ...
            check_for_updates_async(parent=self)
    """
    checker = UpdateChecker()

    def _on_available(tag, url, notes):
        dialog = UpdateDialog(tag, url, notes, parent=parent)
        dialog.exec()

    checker.update_available.connect(_on_available)
    checker.start()

    
    if parent:
        parent._update_checker = checker
    else:
        check_for_updates_async._checker = checker


# ── Preview standalone ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    
    dlg = UpdateDialog(
        tag=f"{CURRENT_VERSION}",
        dl_url=f"https://github.com/{GITHUB_REPO}/releases/download/{CURRENT_VERSION}/app.zip",
        notes="Teste"
    )
    dlg.exec()
    sys.exit(0)

# 1.3.0