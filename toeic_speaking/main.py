#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOEIC Speaking Practice Application
Windows Desktop Application - Full simulation of TOEIC Speaking test (PART 1-5)
"""

import sys
import json
import os
import shutil
import threading
import datetime
from enum import Enum, auto
from typing import List, Dict, Any, Optional

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QTextEdit, QGroupBox, QStackedWidget,
        QTreeWidget, QTreeWidgetItem, QToolBar, QCheckBox, QFileDialog,
        QMessageBox, QFrame, QScrollArea, QSizePolicy, QLineEdit,
        QSplitter, QTabWidget, QSpacerItem, QAbstractItemView,
        QTableWidget, QTableWidgetItem, QHeaderView
    )
    from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize, QUrl
    from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor, QIcon
    PYQT = 5
except ImportError:
    try:
        from PySide6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QPushButton, QTextEdit, QGroupBox, QStackedWidget,
            QTreeWidget, QTreeWidgetItem, QToolBar, QCheckBox, QFileDialog,
            QMessageBox, QFrame, QScrollArea, QSizePolicy, QLineEdit,
            QSplitter, QTabWidget, QSpacerItem, QAbstractItemView,
            QTableWidget, QTableWidgetItem, QHeaderView
        )
        from PySide6.QtCore import Qt, QTimer, QThread, Signal as pyqtSignal, QSize, QUrl
        from PySide6.QtGui import QFont, QPixmap, QPalette, QColor, QIcon
        PYQT = 6
    except ImportError:
        print("Error: PyQt5 or PySide6 is required.\n  pip install PyQt5")
        sys.exit(1)

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import pyaudio
    import wave
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False

# ============================================================
# DEFAULT CONFIGURATION
# ============================================================
DEFAULT_CONFIG = {
    "part1": [
        {
            "text": (
                "Welcome to Union Job Fair where your gateway to career opportunities awaits. "
                "Today we have over two hundred employers from a variety of industries looking "
                "to connect with talented individuals like you. Whether you are seeking your "
                "first job or looking to advance your career, our dedicated team of career "
                "counselors is here to assist you. Make sure to pick up a job fair guide at "
                "the entrance and check out the map for booth locations. We look forward to "
                "helping you find your perfect match today."
            )
        },
        {
            "text": (
                "This is Angela Thompson with your local weather forecast. Today we can expect "
                "partly cloudy skies with a high of seventy-two degrees Fahrenheit. There is a "
                "twenty percent chance of afternoon showers, so you may want to carry an umbrella "
                "just in case. Tonight will be cooler with temperatures dropping to around "
                "fifty-five degrees. Looking ahead to the weekend, we are expecting sunny skies "
                "with temperatures in the mid-seventies, perfect weather for outdoor activities."
            )
        }
    ],
    "part2": [
        {
            "image_path": "images/pic1.jpg",
            "answer": (
                "This picture shows a busy office environment. I can see several people working "
                "at their desks with computers. The office appears to be modern with good lighting. "
                "Some people are talking to each other, possibly in a meeting. The overall atmosphere "
                "seems professional and productive."
            ),
            "marked": False
        },
        {
            "image_path": "images/pic2.jpg",
            "answer": (
                "The picture depicts an outdoor market or shopping area. There are many stalls "
                "with various goods on display. People are walking around and browsing the items. "
                "The weather appears to be nice and sunny. This looks like a weekend farmers market."
            ),
            "marked": False
        }
    ],
    "part3": {
        "background": (
            "Imagine that an English newspaper company is doing research in your area. "
            "You have agreed to participate in a telephone interview about using computers."
        ),
        "questions": [
            {
                "text": (
                    "Has anyone ever asked for your help to resolve any computer-related issues? "
                    "If so, were you able to solve the problem?"
                ),
                "answer": (
                    "Yes, my colleagues often ask me for help with computer issues. I was usually "
                    "able to solve the problems because I have some technical knowledge. For example, "
                    "last week I helped a coworker recover a lost file."
                ),
                "speaking_time": 15,
                "marked": False
            },
            {
                "text": (
                    "Have you considered hiring professional help to resolve technological issues "
                    "with your computer?"
                ),
                "answer": (
                    "Yes, I have considered it. For major issues like hardware problems, I think "
                    "it is better to hire a professional. It saves time and ensures the problem "
                    "is fixed correctly."
                ),
                "speaking_time": 15,
                "marked": False
            },
            {
                "text": (
                    "Which of the following methods would you prefer when seeking technical support "
                    "from a specialist? Interacting face-to-face; Talking on the phone; Chatting online."
                ),
                "answer": (
                    "I would prefer chatting online because it is convenient and I can share "
                    "screenshots to show the problem. Also, I can refer back to the conversation "
                    "later if I need to follow the instructions again."
                ),
                "speaking_time": 30,
                "marked": False
            }
        ]
    },
    "part4": {
        "material": (
            "Annual Medical Conference\n"
            "Crown Royal Hotel (Banquet Hall) | Thursday, January 5th\n\n"
            "• 9:00 – 10:00 a.m.: Keynote Speech: Future of Medical Science (Presenter: Jennifer Fleming)\n"
            "• 10:15 – 11:15 a.m.: Lecture: Discharge options for extended-care patients (Presenter: Robert Chang)\n"
            "• 11:30 a.m. – 12:30 p.m.: Workshop: Address unrealistic care goals (Presenter: William Lee)\n"
            "• 12:30 – 1:30 p.m.: Lunch Break\n"
            "• 1:30 – 2:30 p.m.: Lecture: Emergency management in rural settings (Presenter: Sarah Johnson)\n"
            "• 2:45 – 3:45 p.m.: Workshop: Patient communication strategies (Presenter: Michael Torres)\n"
            "• 4:00 – 5:00 p.m.: Q&A Panel Discussion\n\n"
            "Registration Fee: $75 (Lunch included)\n"
            "Contact: conference@medassoc.org"
        ),
        "questions": [
            {
                "text": "What is the registration fee for the conference?",
                "answer": "The registration fee is $75, and lunch is included.",
                "speaking_time": 15
            },
            {
                "text": "Who is presenting the workshop on 'Address unrealistic care goals'?",
                "answer": "William Lee is presenting that workshop.",
                "speaking_time": 15
            },
            {
                "text": "According to the schedule, what activities are planned for the afternoon?",
                "answer": (
                    "The afternoon includes a lecture on emergency management in rural settings "
                    "by Sarah Johnson, a workshop on patient communication strategies by Michael "
                    "Torres, and a Q&A panel discussion."
                ),
                "speaking_time": 30
            }
        ]
    },
    "part5": [
        {
            "question": (
                "Do you think parents should allow their children to watch TV during their free time? "
                "Why or why not? Give specific reasons and examples to support your opinion."
            ),
            "answer": (
                "I think parents should allow children to watch TV in moderation. Educational programs "
                "can help children learn new things. However, parents should set time limits and choose "
                "appropriate content. For example, nature documentaries or educational shows can be "
                "both entertaining and informative."
            ),
            "marked": False
        }
    ]
}

# ============================================================
# TTS WORKER
# ============================================================
class TTSWorker(QThread):
    """Background TTS thread — creates pyttsx3 engine inside run() for thread safety."""
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lock = threading.Lock()
        self._queue: List[str] = []

    def speak(self, text: str):
        with self._lock:
            self._queue.append(text)
        if not self.isRunning():
            self.start()

    def clear(self):
        with self._lock:
            self._queue.clear()

    def run(self):
        if not TTS_AVAILABLE:
            return
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 155)
            engine.setProperty('volume', 1.0)
            # Prefer English voice
            voices = engine.getProperty('voices')
            for v in voices:
                if 'english' in v.name.lower() or 'zira' in v.name.lower() or 'david' in v.name.lower():
                    engine.setProperty('voice', v.id)
                    break
            while True:
                with self._lock:
                    if not self._queue:
                        break
                    text = self._queue.pop(0)
                engine.say(text)
                engine.runAndWait()
        except Exception as e:
            print(f"[TTS] Error: {e}")
        finally:
            self.finished.emit()


class TTSManager:
    _worker: Optional[TTSWorker] = None

    def __init__(self):
        self._worker = TTSWorker()

    def speak(self, text: str):
        if TTS_AVAILABLE and text:
            self._worker.speak(text)

    def stop(self):
        if self._worker:
            self._worker.clear()

    @property
    def available(self):
        return TTS_AVAILABLE


tts = TTSManager()

# ============================================================
# RECORD THREAD
# ============================================================
class RecordThread(QThread):
    """Background thread: records microphone input via pyaudio and saves as WAV."""
    record_started  = pyqtSignal()
    record_finished = pyqtSignal(str)   # emits saved filepath

    CHUNK    = 1024
    CHANNELS = 1
    RATE     = 44100

    def __init__(self, filepath: str, parent=None):
        super().__init__(parent)
        self._filepath   = filepath
        self._stop_flag  = False

    def request_stop(self):
        self._stop_flag = True

    def run(self):
        if not PYAUDIO_AVAILABLE:
            return
        try:
            p           = pyaudio.PyAudio()
            sample_size = p.get_sample_size(pyaudio.paInt16)
            stream      = p.open(
                format=pyaudio.paInt16,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
            )
            frames = []
            self.record_started.emit()
            while not self._stop_flag:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(data)
            stream.stop_stream()
            stream.close()
            p.terminate()

            dirpath = os.path.dirname(self._filepath)
            if dirpath:
                os.makedirs(dirpath, exist_ok=True)
            wf = wave.open(self._filepath, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(sample_size)
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            self.record_finished.emit(self._filepath)
        except Exception as e:
            print(f"[Record] Error: {e}")
            self.record_finished.emit("")


CONFIG_FILE = "toeic_speaking_config.json"


class ConfigManager:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self, filepath: str = None) -> bool:
        path = filepath or CONFIG_FILE
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                return True
            except Exception as e:
                QMessageBox.warning(None, "Load Error", f"Failed to load config:\n{e}")
                self.data = json.loads(json.dumps(DEFAULT_CONFIG))
                return False
        else:
            self.data = json.loads(json.dumps(DEFAULT_CONFIG))
            return True

    def save(self, filepath: str = None) -> bool:
        path = filepath or CONFIG_FILE
        if os.path.exists(path):
            try:
                shutil.copy(path, path + ".bak")
            except Exception:
                pass
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            QMessageBox.critical(None, "Save Error", f"Failed to save:\n{e}")
            return False

    def part1(self) -> List[Dict]:
        return self.data.setdefault('part1', [])

    def part2(self) -> List[Dict]:
        return self.data.setdefault('part2', [])

    def part3(self) -> Dict:
        return self.data.setdefault('part3', {'background': '', 'questions': []})

    def part4(self) -> Dict:
        return self.data.setdefault('part4', {'material': '', 'questions': []})

    def part5(self) -> List[Dict]:
        return self.data.setdefault('part5', [])


cfg = ConfigManager()

# ============================================================
# TIMER PHASE
# ============================================================
class Phase(Enum):
    IDLE = auto()
    PREPARATION = auto()
    READING = auto()
    SPEAKING = auto()
    COMPLETED = auto()


PHASE_LABELS = {
    Phase.IDLE: "READY",
    Phase.PREPARATION: "PREPARATION TIME",
    Phase.READING: "READING TIME",
    Phase.SPEAKING: "SPEAKING TIME",
    Phase.COMPLETED: "COMPLETED",
}

# ============================================================
# STYLES
# ============================================================
STYLE_EDIT = "border: 2px solid #f39c12; border-radius: 5px; padding: 6px; background: #fffde7;"
STYLE_READ = "border: 1px solid #bdc3c7; border-radius: 5px; padding: 6px; background: white;"
STYLE_MATERIAL = "border: 1px solid #bdc3c7; border-radius: 5px; padding: 6px; background: #fafafa;"

BTN_START = """
QPushButton {
    background: #27ae60; color: white; border-radius: 6px;
    font-size: 14px; font-weight: bold; padding: 8px 20px; min-height: 38px;
}
QPushButton:hover { background: #2ecc71; }
QPushButton:disabled { background: #95a5a6; }
"""
BTN_RESET = """
QPushButton {
    background: #e67e22; color: white; border-radius: 6px;
    font-size: 13px; padding: 8px 16px; min-height: 38px;
}
QPushButton:hover { background: #f39c12; }
"""
BTN_BLUE = """
QPushButton {
    background: #2980b9; color: white; border-radius: 6px;
    font-size: 13px; padding: 8px 16px; min-height: 38px;
}
QPushButton:hover { background: #3498db; }
"""

# ============================================================
# COUNTDOWN WIDGET
# ============================================================
class CountdownWidget(QWidget):
    phase_finished = pyqtSignal(object)  # emits Phase

    def __init__(self, parent=None):
        super().__init__(parent)
        self._phase = Phase.IDLE
        self._remaining = 0
        self._hms = False
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.phase_label = QLabel("READY")
        self.phase_label.setAlignment(Qt.AlignCenter)
        self.phase_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.phase_label.setStyleSheet("color: #2c3e50; letter-spacing: 2px;")

        self.time_label = QLabel("00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont("Courier New", 52, QFont.Bold))
        self._set_time_style(Phase.IDLE)

        layout.addWidget(self.phase_label)
        layout.addWidget(self.time_label)

    def _set_time_style(self, phase: Phase):
        colors = {
            Phase.IDLE: ("#7f8c8d", "#f5f6fa"),
            Phase.PREPARATION: ("#2980b9", "#ebf5fb"),
            Phase.READING: ("#8e44ad", "#f5eef8"),
            Phase.SPEAKING: ("#27ae60", "#eafaf1"),
            Phase.COMPLETED: ("#27ae60", "#eafaf1"),
        }
        fg, bg = colors.get(phase, ("#7f8c8d", "#f5f6fa"))
        self.time_label.setStyleSheet(
            f"color: {fg}; background: {bg}; border-radius: 10px; padding: 8px 20px;"
        )

    def start(self, phase: Phase, seconds: int, hms: bool = False):
        self._phase = phase
        self._remaining = seconds
        self._hms = hms
        self._update_display()
        self._timer.start()

    def stop(self):
        self._timer.stop()
        self._phase = Phase.IDLE

    def reset(self):
        self._timer.stop()
        self._phase = Phase.IDLE
        self._remaining = 0
        self._hms = False
        self.phase_label.setText("READY")
        self.time_label.setText("00:00")
        self._set_time_style(Phase.IDLE)

    def is_running(self) -> bool:
        return self._timer.isActive()

    def current_phase(self) -> Phase:
        return self._phase

    def _tick(self):
        self._remaining -= 1
        self._update_display()
        if self._remaining <= 0:
            self._timer.stop()
            done = self._phase
            self._phase = Phase.IDLE
            self.phase_finished.emit(done)

    def _update_display(self):
        if self._hms:
            h, rem = divmod(max(0, self._remaining), 3600)
            m, s = divmod(rem, 60)
            self.time_label.setText(f"{h:02d}:{m:02d}:{s:02d}")
        else:
            m, s = divmod(max(0, self._remaining), 60)
            self.time_label.setText(f"{m:02d}:{s:02d}")
        self.phase_label.setText(PHASE_LABELS.get(self._phase, ""))
        self._set_time_style(self._phase)

    def mark_done(self):
        self._timer.stop()
        self._phase = Phase.COMPLETED
        self.phase_label.setText("COMPLETED")
        self.time_label.setText("✓ Done")
        self._set_time_style(Phase.COMPLETED)


# ============================================================
# COLLAPSIBLE ANSWER BOX
# ============================================================
class AnswerBox(QWidget):
    def __init__(self, label="Reference Answer", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.toggle_btn = QPushButton(f"▶ {label}")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(False)
        self.toggle_btn.setStyleSheet(
            "QPushButton { background: #ecf0f1; border: none; border-radius: 4px; "
            "padding: 5px 10px; text-align: left; color: #555; font-size: 12px; }"
            "QPushButton:checked { background: #d5dbdb; }"
        )
        self.toggle_btn.toggled.connect(self._toggle)
        layout.addWidget(self.toggle_btn)

        self.content = QTextEdit()
        self.content.setFixedHeight(0)
        self.content.setFont(QFont("Arial", 10))
        self.content.setStyleSheet(STYLE_READ)
        layout.addWidget(self.content)

    def _toggle(self, checked: bool):
        self.toggle_btn.setText(
            f"{'▼' if checked else '▶'} {self.toggle_btn.text()[2:]}"
        )
        self.content.setFixedHeight(110 if checked else 0)

    def set_text(self, text: str):
        self.content.setPlainText(text)

    def get_text(self) -> str:
        return self.content.toPlainText()

    def set_read_only(self, ro: bool):
        self.content.setReadOnly(ro)
        style = STYLE_READ if ro else STYLE_EDIT
        self.content.setStyleSheet(style)


# ============================================================
# INSTRUCTION BOX
# ============================================================
class InstructionBox(QGroupBox):
    def __init__(self, title: str, body: str, parent=None):
        super().__init__("Instructions (click to collapse)", parent)
        self.setCheckable(True)
        self.setChecked(True)
        self.setStyleSheet(
            "QGroupBox { font-weight: bold; border: 2px solid #3498db; border-radius: 8px; "
            "margin-top: 8px; background: #ebf5fb; }"
            "QGroupBox::title { subcontrol-origin: margin; left: 10px; color: #2980b9; }"
        )
        layout = QVBoxLayout(self)
        t = QLabel(f"<b>{title}</b>")
        t.setFont(QFont("Arial", 11))
        t.setWordWrap(True)
        b = QLabel(body)
        b.setFont(QFont("Arial", 10))
        b.setWordWrap(True)
        b.setStyleSheet("color: #444; margin-top: 4px;")
        layout.addWidget(t)
        layout.addWidget(b)

        # Hide children when unchecked
        self.toggled.connect(lambda on: [t.setVisible(on), b.setVisible(on)])


# ============================================================
# DIRECTIONS WIDGET — TOEIC Speaking Test Directions
# ============================================================
class DirectionsWidget(QWidget):
    """Displays the TOEIC Speaking Test Directions page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content.setStyleSheet("background: white;")
        cl = QVBoxLayout(content)
        cl.setContentsMargins(56, 40, 56, 40)
        cl.setSpacing(20)

        # ── Title ────────────────────────────────────────────────────────────
        title = QLabel("TOEIC® Speaking Test Directions")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet(
            "color: #1a2a3a; padding-bottom: 10px;"
            "border-bottom: 3px solid #3498db;"
        )
        cl.addWidget(title)

        # ── Intro paragraph ───────────────────────────────────────────────────
        intro = QLabel(
            "This is the TOEIC® Speaking test. This test includes 11 questions that measure "
            "different aspects of your speaking ability. The test lasts approximately 20 minutes."
        )
        intro.setFont(QFont("Arial", 13))
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #34495e; line-height: 1.6;")
        cl.addWidget(intro)

        # ── Section heading ───────────────────────────────────────────────────
        sec_lbl = QLabel("Question Overview")
        sec_lbl.setFont(QFont("Arial", 15, QFont.Bold))
        sec_lbl.setStyleSheet("color: #2c3e50; margin-top: 4px;")
        cl.addWidget(sec_lbl)

        # ── Table ─────────────────────────────────────────────────────────────
        headers = ["Questions", "Task", "Evaluation Criteria", "Prep Time", "Speaking Time"]
        table_rows = [
            ("Q 1 – 2",
             "Read a text aloud",
             "Pronunciation, intonation and stress",
             "45 sec", "45 sec"),
            ("Q 3 – 4",
             "Describe a picture",
             "All above + grammar, vocabulary, cohesion",
             "45 sec", "30 sec"),
            ("Q 5 – 6",
             "Respond to questions",
             "All above + relevance and completeness of content",
             "3 sec", "15 sec"),
            ("Q 7",
             "Respond to questions",
             "All above + relevance and completeness of content",
             "3 sec", "30 sec"),
            ("Q 8 – 10",
             "Respond using information provided",
             "All above",
             "45 sec (reading)", "15 / 15 / 30 sec"),
            ("Q 11",
             "Express an opinion",
             "All above",
             "45 sec", "60 sec"),
        ]

        table = QTableWidget(len(table_rows), len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)
        table.setShowGrid(True)
        table.setWordWrap(True)
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #d5d8dc;
                border-radius: 6px;
                gridline-color: #d5d8dc;
                font-size: 12px;
                background: white;
            }
            QHeaderView::section {
                background: #2c3e50;
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 6px;
                border: none;
                border-right: 1px solid #3d5166;
            }
            QTableWidget::item {
                padding: 8px 8px;
            }
            QTableWidget::item:alternate {
                background: #f0f4f8;
            }
        """)

        col_widths = [90, 190, 0, 110, 115]  # 0 = stretch (col 2)
        for col, w in enumerate(col_widths):
            if w:
                table.setColumnWidth(col, w)

        row_colors = [
            QColor("#ebf5fb"), QColor("#eaf4fb"),
            QColor("#fdfefe"), QColor("#fdfefe"),
            QColor("#fdfefe"), QColor("#fdfefe"),
        ]

        for row, (q, task, criteria, prep, speaking) in enumerate(table_rows):
            cells = [q, task, criteria, prep, speaking]
            for col, text in enumerate(cells):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if col == 0:
                    item.setFont(QFont("Arial", 12, QFont.Bold))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    item.setBackground(QColor("#d6eaf8"))
                else:
                    item.setFont(QFont("Arial", 12))
                table.setItem(row, col, item)

        table.resizeRowsToContents()
        table.setMinimumHeight(240)
        cl.addWidget(table)

        # ── Footer notes ──────────────────────────────────────────────────────
        for text in [
            "For each type of question, you will be given specific directions, including the "
            "time allowed for preparation and speaking.",
            "It is to your advantage to say as much as you can in the time allowed. It is also "
            "important that you speak clearly and that you answer each question according to the directions.",
        ]:
            lbl = QLabel(text)
            lbl.setFont(QFont("Arial", 12))
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color: #34495e;")
            cl.addWidget(lbl)

        cl.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)


    def set_edit_mode(self, on: bool):
        pass  # no editable fields

    def refresh(self):
        pass

    def load_question(self, index: int):
        pass  # not applicable


# ============================================================
# PART 1 WIDGET — Read Aloud (fully automatic exam simulation)
# ============================================================
class Part1Widget(QWidget):
    PREP_TIME = 45   # preparation seconds
    READ_TIME = 30   # reading seconds

    # Emitted when the auto-flow advances to a different question index
    question_changed = pyqtSignal(int)

    INTRO_BODY = (
        "In this part of the test, you will read aloud the text on the screen. "
        "You will have 45 seconds to prepare. Then you will have 45 seconds to read the text aloud."
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit_mode = False
        self.current_index = 0
        self._pending_callback = None

        # Timer for the initial 2-second delay before "Begin preparing now"
        self._init_timer = QTimer(self)
        self._init_timer.setSingleShot(True)
        self._init_timer.timeout.connect(self._begin_prepare)

        # Timer for the 3-second delay before auto-reading instructions
        self._intro_read_timer = QTimer(self)
        self._intro_read_timer.setSingleShot(True)
        self._intro_read_timer.timeout.connect(self._read_intro_aloud)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Stacked widget: page 0 = intro, page 1 = question
        self.content_stack = QStackedWidget()
        layout.addWidget(self.content_stack, 1)

        # ── Page 0: Instruction page ──────────────────────────────────────────
        instr_page = QWidget()
        instr_page.setStyleSheet("background: white;")
        ip_layout = QVBoxLayout(instr_page)
        ip_layout.setContentsMargins(100, 0, 100, 40)
        ip_layout.setSpacing(0)

        ip_layout.addStretch(2)

        # Part badge
        part_badge = QLabel("PART 1  ·  Questions 1 – 2")
        part_badge.setAlignment(Qt.AlignCenter)
        part_badge.setFont(QFont("Arial", 12, QFont.Bold))
        part_badge.setStyleSheet(
            "color: white; background: #2980b9; border-radius: 16px; "
            "padding: 4px 22px; letter-spacing: 1px;"
        )
        part_badge.setFixedHeight(32)
        ip_layout.addWidget(part_badge, 0, Qt.AlignCenter)

        ip_layout.addSpacing(24)

        # Centered title
        self._intro_title = QLabel("Read a Text Aloud")
        self._intro_title.setAlignment(Qt.AlignCenter)
        self._intro_title.setFont(QFont("Arial", 26, QFont.Bold))
        self._intro_title.setStyleSheet("color: #1a2a3a;")
        ip_layout.addWidget(self._intro_title)

        ip_layout.addSpacing(16)

        # Thin separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #3498db; background: #3498db; max-height: 2px; margin: 0 80px;")
        sep.setFixedHeight(2)
        ip_layout.addWidget(sep)

        ip_layout.addSpacing(24)

        # Body text (will be read aloud after 3s delay)
        self._intro_body = QLabel(self.INTRO_BODY)
        self._intro_body.setAlignment(Qt.AlignCenter)
        self._intro_body.setFont(QFont("Arial", 15))
        self._intro_body.setWordWrap(True)
        self._intro_body.setStyleSheet(
            "color: #2c3e50; line-height: 1.9; padding: 0 20px;"
        )
        ip_layout.addWidget(self._intro_body)

        ip_layout.addStretch(3)

        # "Next page" button at bottom right
        next_row = QHBoxLayout()
        next_row.addStretch()
        self.next_btn = QPushButton("下一页  ▶")
        self.next_btn.setFixedHeight(40)
        self.next_btn.setMinimumWidth(120)
        self.next_btn.setStyleSheet(BTN_BLUE)
        self.next_btn.clicked.connect(self._on_next_clicked)
        next_row.addWidget(self.next_btn)
        ip_layout.addLayout(next_row)

        self.content_stack.addWidget(instr_page)

        # ── Page 1: Question page ─────────────────────────────────────────────
        q_page = QWidget()
        q_page.setStyleSheet("background: white;")
        qp_layout = QVBoxLayout(q_page)
        qp_layout.setContentsMargins(30, 20, 30, 16)
        qp_layout.setSpacing(14)

        self.q_label = QLabel("Question 1 of 11")
        self.q_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.q_label.setStyleSheet(
            "color: #2c3e50; padding: 6px 0; border-bottom: 2px solid #3498db; margin-bottom: 4px;"
        )
        qp_layout.addWidget(self.q_label)

        grp = QGroupBox("Text to Read Aloud")
        grp.setStyleSheet(
            "QGroupBox { font-weight: bold; font-size: 13px; color: #2980b9; "
            "border: 1px solid #aed6f1; border-radius: 8px; margin-top: 10px; "
            "background: #fbfcfe; padding-top: 6px; }"
            "QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 6px; }"
        )
        gl = QVBoxLayout(grp)
        gl.setContentsMargins(12, 12, 12, 12)
        self.text_edit = QTextEdit()
        self.text_edit.setMinimumHeight(220)
        self.text_edit.setFont(QFont("Georgia", 17))
        self.text_edit.setStyleSheet(
            "border: none; background: transparent; "
            "color: #1a252f; line-height: 1.8; padding: 4px;"
        )
        self.text_edit.setReadOnly(True)
        self.text_edit.textChanged.connect(self._sync_text)
        gl.addWidget(self.text_edit)
        qp_layout.addWidget(grp)

        self.countdown = CountdownWidget()
        self.countdown.phase_finished.connect(self._on_phase_done)
        self.countdown.setVisible(False)
        qp_layout.addWidget(self.countdown)

        qp_layout.addStretch()

        # Bottom-right: STOP and RESTART buttons
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        self.stop_btn = QPushButton("■  Stop")
        self.stop_btn.setStyleSheet(BTN_RESET)
        self.stop_btn.clicked.connect(self._stop)
        self.restart_btn = QPushButton("↺  Restart")
        self.restart_btn.setStyleSheet(BTN_BLUE)
        self.restart_btn.clicked.connect(self._restart)
        bottom_row.addWidget(self.stop_btn)
        bottom_row.addWidget(self.restart_btn)
        qp_layout.addLayout(bottom_row)

        self.content_stack.addWidget(q_page)

        # Default to intro page
        self.content_stack.setCurrentIndex(0)

    # ── Public interface ──────────────────────────────────────────────────────

    def show_intro(self):
        """Show the instruction page; auto-reads body after 3 seconds."""
        self._cancel_all()
        self.content_stack.setCurrentIndex(0)
        self._intro_read_timer.start(3000)

    def load_question(self, index: int):
        """Load a question and start the fully-automatic exam flow."""
        self._cancel_all()
        self.current_index = index
        data = cfg.part1()
        self.q_label.setText(f"Question {index + 1} of 11")
        self.text_edit.blockSignals(True)
        self.text_edit.setPlainText(data[index]['text'] if index < len(data) else "")
        self.text_edit.blockSignals(False)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet(
            "border: none; background: transparent; "
            "color: #1a252f; line-height: 1.8; padding: 4px;"
        )
        self.countdown.reset()
        self.countdown.setVisible(False)
        self.content_stack.setCurrentIndex(1)
        if not self.edit_mode:
            self._init_timer.start(2000)

    def refresh(self):
        self.show_intro()

    def set_edit_mode(self, on: bool):
        self.edit_mode = on
        if on:
            self._cancel_all()
            # Show question 0 for editing without auto-flow
            data = cfg.part1()
            self.q_label.setText(f"Question {self.current_index + 1} of 11")
            self.text_edit.blockSignals(True)
            self.text_edit.setPlainText(
                data[self.current_index]['text'] if self.current_index < len(data) else ""
            )
            self.text_edit.blockSignals(False)
            self.text_edit.setReadOnly(False)
            self.text_edit.setStyleSheet(STYLE_EDIT)
            self.content_stack.setCurrentIndex(1)
        else:
            self.text_edit.setReadOnly(True)
            self.text_edit.setStyleSheet(
                "border: none; background: transparent; "
                "color: #1a252f; line-height: 1.8; padding: 4px;"
            )

    def is_active(self) -> bool:
        """Returns True if the automatic exam flow is running."""
        return (
            self._init_timer.isActive()
            or self._intro_read_timer.isActive()
            or self._pending_callback is not None
            or self.countdown.is_running()
        )

    # ── Internal flow ─────────────────────────────────────────────────────────

    def _cancel_all(self):
        """Stop all timers, TTS, and countdown."""
        self._init_timer.stop()
        self._intro_read_timer.stop()
        self._pending_callback = None
        try:
            tts._worker.finished.disconnect(self._on_tts_done)
        except Exception:
            pass
        tts.stop()
        self.countdown.stop()
        self.countdown.reset()
        self.countdown.setVisible(False)

    def _on_next_clicked(self):
        """User clicked the 'Next page' button on the intro page."""
        self._cancel_all()
        self.load_question(0)

    def _read_intro_aloud(self):
        """Called 3s after showing intro — reads the body text (not the title)."""
        tts.speak(self.INTRO_BODY)

    def _tts_then(self, text: str, callback):
        """Speak text and call callback when TTS finishes."""
        self._pending_callback = callback
        if TTS_AVAILABLE:
            tts._worker.finished.connect(self._on_tts_done)
        tts.speak(text)
        if not TTS_AVAILABLE:
            # No TTS engine — use a short timer as fallback
            QTimer.singleShot(1500, self._on_tts_done)

    def _on_tts_done(self):
        try:
            tts._worker.finished.disconnect(self._on_tts_done)
        except Exception:
            pass
        if self._pending_callback:
            cb = self._pending_callback
            self._pending_callback = None
            cb()

    def _begin_prepare(self):
        """Called 2s after entering question page. Speaks 'Begin preparing now'."""
        self.countdown.setVisible(True)
        self._tts_then("Begin preparing now", self._start_prep_countdown)

    def _start_prep_countdown(self):
        self.countdown.start(Phase.PREPARATION, self.PREP_TIME)

    def _on_phase_done(self, phase):
        if phase == Phase.PREPARATION:
            self._tts_then("Begin reading now", self._start_read_countdown)
        elif phase == Phase.READING:
            self._on_question_complete()

    def _start_read_countdown(self):
        self.countdown.start(Phase.READING, self.READ_TIME)

    def _on_question_complete(self):
        if self.current_index == 0:
            # Auto-advance to Question 2
            self.load_question(1)
            self.question_changed.emit(1)
        else:
            # Question 2 finished — mark done
            self.countdown.mark_done()

    def _stop(self):
        self._cancel_all()

    def _restart(self):
        self.load_question(self.current_index)

    def _sync_text(self):
        if not self.edit_mode:
            return
        data = cfg.part1()
        if self.current_index < len(data):
            data[self.current_index]['text'] = self.text_edit.toPlainText()


# ============================================================
# PART 2 WIDGET — Describe a Picture
# ============================================================
class Part2Widget(QWidget):
    TITLE = "Questions 3 - 4: Describe a picture"
    BODY = (
        "In this part of the test, you will describe the picture on your screen in as much detail "
        "as you can. You will have 45 seconds to prepare your response. Then you will have 30 seconds "
        "to speak about the picture."
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit_mode = False
        self.current_index = 0
        self._build_ui()
        self.load_question(0)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 12, 15, 12)

        self.intro = InstructionBox(self.TITLE, self.BODY)
        layout.addWidget(self.intro)

        self.q_label = QLabel("Question 3 of 11")
        self.q_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.q_label.setStyleSheet("color: #2c3e50; padding: 4px 0;")
        layout.addWidget(self.q_label)

        content = QHBoxLayout()

        # Left: image
        img_grp = QGroupBox("Picture")
        img_grp.setStyleSheet("QGroupBox { font-weight: bold; }")
        ig = QVBoxLayout(img_grp)
        self.img_label = QLabel("[ No image loaded ]")
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setMinimumSize(320, 240)
        self.img_label.setStyleSheet(
            "border: 2px dashed #bdc3c7; border-radius: 6px; "
            "background: #f8f9fa; color: #95a5a6; font-size: 13px;"
        )
        ig.addWidget(self.img_label)

        path_row = QHBoxLayout()
        self.img_path_edit = QLineEdit()
        self.img_path_edit.setPlaceholderText("Image path (e.g. images/pic1.jpg)")
        self.img_path_edit.setReadOnly(True)
        self.img_path_edit.textChanged.connect(self._sync_path)
        self.browse_btn = QPushButton("Browse…")
        self.browse_btn.setEnabled(False)
        self.browse_btn.clicked.connect(self._browse)
        path_row.addWidget(self.img_path_edit)
        path_row.addWidget(self.browse_btn)
        ig.addLayout(path_row)
        content.addWidget(img_grp, 3)

        # Right panel
        right = QVBoxLayout()

        self.answer_box = AnswerBox("Reference Answer")
        self.answer_box.content.textChanged.connect(self._sync_answer)
        right.addWidget(self.answer_box)

        self.countdown = CountdownWidget()
        self.countdown.phase_finished.connect(self._on_phase_done)
        right.addWidget(self.countdown)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("▶  Start Practice")
        self.start_btn.setStyleSheet(BTN_START)
        self.start_btn.clicked.connect(self._start)
        self.reset_btn = QPushButton("↺  Reset")
        self.reset_btn.setStyleSheet(BTN_RESET)
        self.reset_btn.clicked.connect(self._reset)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.reset_btn)
        right.addLayout(btn_row)
        right.addStretch()
        content.addLayout(right, 2)

        layout.addLayout(content)

    def load_question(self, index: int):
        self.current_index = index
        data = cfg.part2()
        self.q_label.setText(f"Question {index + 3} of 11")
        if index < len(data):
            item = data[index]
            self.img_path_edit.blockSignals(True)
            self.img_path_edit.setText(item.get('image_path', ''))
            self.img_path_edit.blockSignals(False)
            self.answer_box.set_text(item.get('answer', ''))
            self._load_image(item.get('image_path', ''))
        self._reset()

    def refresh(self):
        self.load_question(self.current_index)

    def set_edit_mode(self, on: bool):
        self.edit_mode = on
        self.answer_box.set_read_only(not on)
        self.img_path_edit.setReadOnly(not on)
        self.browse_btn.setEnabled(on)

    def _load_image(self, path: str):
        if not path:
            self.img_label.setText("[ No image path set ]")
            return
        if os.path.exists(path):
            px = QPixmap(path)
            if not px.isNull():
                self.img_label.setPixmap(
                    px.scaled(self.img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                return
        self.img_label.setText(f"[ Image not found ]\n{path}")

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.jpg *.jpeg *.png *.bmp *.gif)"
        )
        if path:
            try:
                path = os.path.relpath(path)
            except ValueError:
                pass
            self.img_path_edit.setText(path)
            self._load_image(path)

    def _sync_path(self, path: str):
        if not self.edit_mode:
            return
        data = cfg.part2()
        if self.current_index < len(data):
            data[self.current_index]['image_path'] = path

    def _sync_answer(self):
        if not self.edit_mode:
            return
        data = cfg.part2()
        if self.current_index < len(data):
            data[self.current_index]['answer'] = self.answer_box.get_text()

    def _start(self):
        if self.countdown.is_running():
            return
        tts.speak("Begin preparing now")
        self.start_btn.setEnabled(False)
        self.countdown.start(Phase.PREPARATION, 45)

    def _on_phase_done(self, phase):
        if phase == Phase.PREPARATION:
            tts.speak("Begin speaking now")
            self.countdown.start(Phase.SPEAKING, 30)
        elif phase == Phase.SPEAKING:
            self.countdown.mark_done()
            self.start_btn.setEnabled(True)

    def _reset(self):
        self.countdown.reset()
        self.start_btn.setEnabled(True)


# ============================================================
# PART 3 WIDGET — Respond to Questions
# ============================================================
class Part3Widget(QWidget):
    TITLE = "Questions 5 - 7: Respond to questions"
    BODY = (
        "In this part of the test, you will answer three questions. You will have three seconds to "
        "prepare after you hear each question. You will have 15 seconds to respond to Questions 5 "
        "and 6, and 30 seconds to respond to Question 7."
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit_mode = False
        self.current_index = 0
        self._build_ui()
        self.load_question(0)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 12, 15, 12)

        self.intro = InstructionBox(self.TITLE, self.BODY)
        layout.addWidget(self.intro)

        self.q_label = QLabel("Question 5 of 11")
        self.q_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.q_label.setStyleSheet("color: #2c3e50; padding: 4px 0;")
        layout.addWidget(self.q_label)

        bg_grp = QGroupBox("Background Information (shared across Questions 5–7)")
        bg_grp.setStyleSheet("QGroupBox { font-weight: bold; color: #555; }")
        bg_l = QVBoxLayout(bg_grp)
        self.bg_edit = QTextEdit()
        self.bg_edit.setMaximumHeight(75)
        self.bg_edit.setFont(QFont("Arial", 10))
        self.bg_edit.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; background: #eaf4fb;")
        self.bg_edit.textChanged.connect(self._sync_bg)
        bg_l.addWidget(self.bg_edit)
        layout.addWidget(bg_grp)

        q_grp = QGroupBox("Question")
        q_grp.setStyleSheet("QGroupBox { font-weight: bold; }")
        ql = QVBoxLayout(q_grp)
        self.q_edit = QTextEdit()
        self.q_edit.setMaximumHeight(90)
        self.q_edit.setFont(QFont("Arial", 11))
        self.q_edit.setStyleSheet(STYLE_READ)
        self.q_edit.textChanged.connect(self._sync_question)
        ql.addWidget(self.q_edit)
        layout.addWidget(q_grp)

        self.answer_box = AnswerBox()
        self.answer_box.content.textChanged.connect(self._sync_answer)
        layout.addWidget(self.answer_box)

        self.countdown = CountdownWidget()
        self.countdown.phase_finished.connect(self._on_phase_done)
        layout.addWidget(self.countdown)

        btn_row = QHBoxLayout()
        self.read_btn = QPushButton("🔊  Read Question")
        self.read_btn.setStyleSheet(BTN_BLUE)
        self.read_btn.clicked.connect(self._read_question)
        self.start_btn = QPushButton("▶  Start Practice")
        self.start_btn.setStyleSheet(BTN_START)
        self.start_btn.clicked.connect(self._start)
        self.reset_btn = QPushButton("↺  Reset")
        self.reset_btn.setStyleSheet(BTN_RESET)
        self.reset_btn.clicked.connect(self._reset)
        btn_row.addWidget(self.read_btn)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.reset_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        layout.addStretch()

    def load_question(self, index: int):
        self.current_index = index
        data = cfg.part3()
        self.q_label.setText(f"Question {index + 5} of 11")

        self.bg_edit.blockSignals(True)
        self.bg_edit.setPlainText(data.get('background', ''))
        self.bg_edit.blockSignals(False)

        qs = data.get('questions', [])
        self.q_edit.blockSignals(True)
        if index < len(qs):
            self.q_edit.setPlainText(qs[index].get('text', ''))
            self.answer_box.set_text(qs[index].get('answer', ''))
        else:
            self.q_edit.setPlainText('')
            self.answer_box.set_text('')
        self.q_edit.blockSignals(False)
        self._reset()

    def refresh(self):
        self.load_question(self.current_index)

    def set_edit_mode(self, on: bool):
        self.edit_mode = on
        self.bg_edit.setReadOnly(not on)
        self.bg_edit.setStyleSheet(STYLE_EDIT if on else "border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; background: #eaf4fb;")
        self.q_edit.setReadOnly(not on)
        self.q_edit.setStyleSheet(STYLE_EDIT if on else STYLE_READ)
        self.answer_box.set_read_only(not on)

    def _speaking_time(self) -> int:
        qs = cfg.part3().get('questions', [])
        if self.current_index < len(qs):
            return qs[self.current_index].get('speaking_time', 15 if self.current_index < 2 else 30)
        return 15 if self.current_index < 2 else 30

    def _read_question(self):
        tts.speak(self.q_edit.toPlainText())

    def _start(self):
        if self.countdown.is_running():
            return
        tts.speak(self.q_edit.toPlainText())
        tts.speak("Begin preparing now")
        self.start_btn.setEnabled(False)
        self.countdown.start(Phase.PREPARATION, 3)

    def _on_phase_done(self, phase):
        if phase == Phase.PREPARATION:
            tts.speak("Begin speaking now")
            self.countdown.start(Phase.SPEAKING, self._speaking_time())
        elif phase == Phase.SPEAKING:
            self.countdown.mark_done()
            self.start_btn.setEnabled(True)

    def _reset(self):
        self.countdown.reset()
        self.start_btn.setEnabled(True)

    def _sync_bg(self):
        if not self.edit_mode:
            return
        cfg.part3()['background'] = self.bg_edit.toPlainText()

    def _sync_question(self):
        if not self.edit_mode:
            return
        qs = cfg.part3().get('questions', [])
        if self.current_index < len(qs):
            qs[self.current_index]['text'] = self.q_edit.toPlainText()

    def _sync_answer(self):
        if not self.edit_mode:
            return
        qs = cfg.part3().get('questions', [])
        if self.current_index < len(qs):
            qs[self.current_index]['answer'] = self.answer_box.get_text()


# ============================================================
# PART 4 WIDGET — Info-Based Questions
# ============================================================
class P4State(Enum):
    IDLE = auto()
    READING = auto()
    Q_PREP = auto()
    Q_SPEAK = auto()
    DONE = auto()


class Part4Widget(QWidget):
    TITLE = "Questions 8 - 10: Respond to questions using information provided"
    BODY = (
        "In this part of the test, you will answer three questions based on the information provided. "
        "You will have 45 seconds to read the information before the questions begin. "
        "You will have three seconds to prepare and 15 seconds to respond to Questions 8 and 9. "
        "You will hear Question 10 two times. "
        "You will have three seconds to prepare and 30 seconds to respond to Question 10."
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit_mode = False
        self.current_index = 0
        self._state = P4State.IDLE
        self._q_idx = 0
        self._build_ui()
        self.load_question(0)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 12, 15, 12)

        self.intro = InstructionBox(self.TITLE, self.BODY)
        layout.addWidget(self.intro)

        self.q_label = QLabel("Questions 8 – 10 of 11")
        self.q_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.q_label.setStyleSheet("color: #2c3e50; padding: 4px 0;")
        layout.addWidget(self.q_label)

        self.status_label = QLabel("Ready — press Start Practice to begin")
        self.status_label.setFont(QFont("Arial", 11))
        self.status_label.setStyleSheet("color: #7f8c8d; padding: 2px 0;")
        layout.addWidget(self.status_label)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs, 1)

        # Tab 1: Practice
        practice_tab = QWidget()
        pt_layout = QVBoxLayout(practice_tab)
        pt_layout.setSpacing(8)

        mat_grp = QGroupBox("Information Material")
        mat_grp.setStyleSheet("QGroupBox { font-weight: bold; }")
        mg = QVBoxLayout(mat_grp)
        self.material_edit = QTextEdit()
        self.material_edit.setMinimumHeight(180)
        self.material_edit.setFont(QFont("Courier New", 10))
        self.material_edit.setStyleSheet(STYLE_MATERIAL)
        self.material_edit.textChanged.connect(self._sync_material)
        mg.addWidget(self.material_edit)
        pt_layout.addWidget(mat_grp)

        cur_q_grp = QGroupBox("Current Question (reference — voice only in real exam)")
        cg = QVBoxLayout(cur_q_grp)
        self.cur_q_label = QLabel("—")
        self.cur_q_label.setWordWrap(True)
        self.cur_q_label.setFont(QFont("Arial", 11))
        self.cur_q_label.setStyleSheet("color: #2c3e50; padding: 5px; background: #fef9e7; border-radius: 4px;")
        cg.addWidget(self.cur_q_label)
        pt_layout.addWidget(cur_q_grp)

        self.countdown = CountdownWidget()
        self.countdown.phase_finished.connect(self._on_phase_done)
        pt_layout.addWidget(self.countdown)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("▶  Start Practice")
        self.start_btn.setStyleSheet(BTN_START)
        self.start_btn.clicked.connect(self._start)
        self.reset_btn = QPushButton("↺  Reset")
        self.reset_btn.setStyleSheet(BTN_RESET)
        self.reset_btn.clicked.connect(self._reset)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.reset_btn)
        btn_row.addStretch()
        pt_layout.addLayout(btn_row)
        self.tabs.addTab(practice_tab, "Practice")

        # Tab 2: Edit Questions
        edit_tab = QWidget()
        et_layout = QVBoxLayout(edit_tab)
        et_layout.setSpacing(8)
        lbl = QLabel("Edit question texts and reference answers for Questions 8–10:")
        lbl.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        et_layout.addWidget(lbl)

        self.q_edits: List[QTextEdit] = []
        self.a_edits: List[QTextEdit] = []
        q_labels = ["Question 8", "Question 9", "Question 10"]
        for i, ql in enumerate(q_labels):
            qg = QGroupBox(f"{ql} — Question Text")
            qgl = QVBoxLayout(qg)
            qe = QTextEdit()
            qe.setMaximumHeight(70)
            qe.setFont(QFont("Arial", 10))
            qe.setStyleSheet(STYLE_READ)

            def make_q_sync(ix):
                def f():
                    if not self.edit_mode:
                        return
                    qs = cfg.part4().get('questions', [])
                    if ix < len(qs):
                        qs[ix]['text'] = self.q_edits[ix].toPlainText()
                return f

            qe.textChanged.connect(make_q_sync(i))
            qgl.addWidget(qe)
            et_layout.addWidget(qg)
            self.q_edits.append(qe)

            ag = QGroupBox(f"{ql} — Reference Answer")
            agl = QVBoxLayout(ag)
            ae = QTextEdit()
            ae.setMaximumHeight(70)
            ae.setFont(QFont("Arial", 10))
            ae.setStyleSheet(STYLE_READ)

            def make_a_sync(ix):
                def f():
                    if not self.edit_mode:
                        return
                    qs = cfg.part4().get('questions', [])
                    if ix < len(qs):
                        qs[ix]['answer'] = self.a_edits[ix].toPlainText()
                return f

            ae.textChanged.connect(make_a_sync(i))
            agl.addWidget(ae)
            et_layout.addWidget(ag)
            self.a_edits.append(ae)

        et_layout.addStretch()
        self.tabs.addTab(edit_tab, "Edit Questions")

    def load_question(self, index: int):
        self.current_index = 0
        data = cfg.part4()
        self.material_edit.blockSignals(True)
        self.material_edit.setPlainText(data.get('material', ''))
        self.material_edit.blockSignals(False)

        qs = data.get('questions', [])
        for i, (qe, ae) in enumerate(zip(self.q_edits, self.a_edits)):
            qe.blockSignals(True)
            ae.blockSignals(True)
            if i < len(qs):
                qe.setPlainText(qs[i].get('text', ''))
                ae.setPlainText(qs[i].get('answer', ''))
            qe.blockSignals(False)
            ae.blockSignals(False)
        self._reset()

    def refresh(self):
        self.load_question(0)

    def set_edit_mode(self, on: bool):
        self.edit_mode = on
        self.material_edit.setReadOnly(not on)
        self.material_edit.setStyleSheet(STYLE_EDIT if on else STYLE_MATERIAL)
        for qe, ae in zip(self.q_edits, self.a_edits):
            qe.setReadOnly(not on)
            ae.setReadOnly(not on)
            qe.setStyleSheet(STYLE_EDIT if on else STYLE_READ)
            ae.setStyleSheet(STYLE_EDIT if on else STYLE_READ)

    def _questions(self) -> List[Dict]:
        return cfg.part4().get('questions', [])

    def _start(self):
        if self.countdown.is_running():
            return
        self._state = P4State.READING
        self._q_idx = 0
        self.start_btn.setEnabled(False)
        self.status_label.setText("Reading time — read the information carefully")
        self.cur_q_label.setText("Please read the information material above carefully.")
        tts.speak("Begin preparing now")
        self.countdown.start(Phase.READING, 45)

    def _on_phase_done(self, phase):
        qs = self._questions()
        if self._state == P4State.READING:
            self._begin_question()
        elif self._state == P4State.Q_PREP:
            tts.speak("Begin speaking now")
            self._state = P4State.Q_SPEAK
            st = qs[self._q_idx].get('speaking_time', 15) if self._q_idx < len(qs) else 15
            self.countdown.start(Phase.SPEAKING, st)
        elif self._state == P4State.Q_SPEAK:
            self._q_idx += 1
            if self._q_idx < 3:
                self._begin_question()
            else:
                self._state = P4State.DONE
                self.countdown.mark_done()
                self.status_label.setText("All questions answered — PART 4 complete!")
                self.cur_q_label.setText("✓ Complete")
                self.start_btn.setEnabled(True)

    def _begin_question(self):
        qs = self._questions()
        q_names = ["Question 8", "Question 9", "Question 10"]
        if self._q_idx >= len(qs):
            return
        q = qs[self._q_idx]
        q_text = q.get('text', '')
        name = q_names[self._q_idx] if self._q_idx < len(q_names) else f"Question {self._q_idx + 8}"
        self.status_label.setText(f"Now: {name}")
        self.cur_q_label.setText(f"{name}:  {q_text}")

        tts.speak(q_text)
        if self._q_idx == 2:
            tts.speak(q_text)
        tts.speak("Begin preparing now")
        self._state = P4State.Q_PREP
        self.countdown.start(Phase.PREPARATION, 3)

    def _reset(self):
        self._state = P4State.IDLE
        self._q_idx = 0
        self.countdown.reset()
        self.start_btn.setEnabled(True)
        self.status_label.setText("Ready — press Start Practice to begin")
        self.cur_q_label.setText("—")

    def _sync_material(self):
        if not self.edit_mode:
            return
        cfg.part4()['material'] = self.material_edit.toPlainText()


# ============================================================
# PART 5 WIDGET — Express an Opinion
# ============================================================
class Part5Widget(QWidget):
    TITLE = "Question 11: Express an opinion"
    BODY = (
        "In this part of the test, you will give your opinion about a specific topic. "
        "Be sure to say as much as you can in the time allowed. "
        "You will have 45 seconds to prepare. Then you will have 60 seconds to speak."
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit_mode = False
        self.current_index = 0
        self._build_ui()
        self.load_question(0)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 12, 15, 12)

        self.intro = InstructionBox(self.TITLE, self.BODY)
        layout.addWidget(self.intro)

        self.q_label = QLabel("Question 11 of 11")
        self.q_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.q_label.setStyleSheet("color: #2c3e50; padding: 4px 0;")
        layout.addWidget(self.q_label)

        q_grp = QGroupBox("Question")
        q_grp.setStyleSheet("QGroupBox { font-weight: bold; }")
        ql = QVBoxLayout(q_grp)
        self.q_edit = QTextEdit()
        self.q_edit.setMinimumHeight(100)
        self.q_edit.setFont(QFont("Arial", 12))
        self.q_edit.setStyleSheet(STYLE_READ)
        self.q_edit.textChanged.connect(self._sync_question)
        ql.addWidget(self.q_edit)
        layout.addWidget(q_grp)

        self.answer_box = AnswerBox()
        self.answer_box.content.textChanged.connect(self._sync_answer)
        layout.addWidget(self.answer_box)

        self.countdown = CountdownWidget()
        self.countdown.phase_finished.connect(self._on_phase_done)
        layout.addWidget(self.countdown)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("▶  Start Practice")
        self.start_btn.setStyleSheet(BTN_START)
        self.start_btn.clicked.connect(self._start)
        self.reset_btn = QPushButton("↺  Reset")
        self.reset_btn.setStyleSheet(BTN_RESET)
        self.reset_btn.clicked.connect(self._reset)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.reset_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        layout.addStretch()

    def load_question(self, index: int):
        self.current_index = index
        data = cfg.part5()
        self.q_edit.blockSignals(True)
        if index < len(data):
            self.q_edit.setPlainText(data[index].get('question', ''))
            self.answer_box.set_text(data[index].get('answer', ''))
        self.q_edit.blockSignals(False)
        self._reset()

    def refresh(self):
        self.load_question(self.current_index)

    def set_edit_mode(self, on: bool):
        self.edit_mode = on
        self.q_edit.setReadOnly(not on)
        self.q_edit.setStyleSheet(STYLE_EDIT if on else STYLE_READ)
        self.answer_box.set_read_only(not on)

    def _start(self):
        if self.countdown.is_running():
            return
        tts.speak("Begin preparing now")
        self.start_btn.setEnabled(False)
        self.countdown.start(Phase.PREPARATION, 45)

    def _on_phase_done(self, phase):
        if phase == Phase.PREPARATION:
            tts.speak("Begin speaking now")
            self.countdown.start(Phase.SPEAKING, 60)
        elif phase == Phase.SPEAKING:
            self.countdown.mark_done()
            self.start_btn.setEnabled(True)

    def _reset(self):
        self.countdown.reset()
        self.start_btn.setEnabled(True)

    def _sync_question(self):
        if not self.edit_mode:
            return
        data = cfg.part5()
        if self.current_index < len(data):
            data[self.current_index]['question'] = self.q_edit.toPlainText()

    def _sync_answer(self):
        if not self.edit_mode:
            return
        data = cfg.part5()
        if self.current_index < len(data):
            data[self.current_index]['answer'] = self.answer_box.get_text()


# ============================================================
# NAVIGATION TREE
# ============================================================
class NavTree(QTreeWidget):
    question_selected = pyqtSignal(int, int)  # part (0–5), index

    _PARTS = [
        # (label, part_num, q_count, child_labels)
        # part_num=0 → Directions (top-level item navigable directly)
        # part_num=1 → PART1 parent navigates to intro (index=-1)
        ("TOEIC Speaking Test Directions", 0, 0, []),
        ("PART1: Read a text aloud",       1, 2, ["Question 1", "Question 2"]),
        ("PART 2  Describe Picture",        2, 2, ["Question 3", "Question 4"]),
        ("PART 3  Respond to Questions",    3, 3, ["Question 5", "Question 6", "Question 7"]),
        ("PART 4  Info Questions",          4, 1, ["Questions 8 – 10"]),
        ("PART 5  Express Opinion",         5, 1, ["Question 11"]),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabel("Navigation")
        self.setMinimumWidth(210)
        self.setMaximumWidth(260)
        self.setAnimated(True)
        self.setStyleSheet(
            "QTreeWidget { background: white; border: none; font-size: 12px; }"
            "QTreeWidget::item { padding: 4px 2px; }"
            "QTreeWidget::item:selected { background: #3498db; color: white; border-radius: 3px; }"
            "QTreeWidget::item:hover { background: #ebf5fb; }"
        )
        self._build()
        self.itemClicked.connect(self._on_click)

    def _build(self):
        self.blockSignals(True)
        self.clear()
        for label, part_num, count, q_labels in self._PARTS:
            part_item = QTreeWidgetItem(self, [label])
            part_item.setFont(0, QFont("Arial", 10, QFont.Bold))
            part_item.setExpanded(True)

            if part_num == 0:
                # Directions — the parent itself is the navigation target
                part_item.setData(0, Qt.UserRole, (0, 0))
            elif part_num == 1:
                # PART1 parent navigates to intro page (index = -1)
                part_item.setData(0, Qt.UserRole, (1, -1))
            else:
                part_item.setData(0, Qt.UserRole, None)

            for j, ql in enumerate(q_labels):
                qi = QTreeWidgetItem(part_item, [f"  {ql}"])
                qi.setData(0, Qt.UserRole, (part_num, j))

        self.blockSignals(False)

    def _on_click(self, item: QTreeWidgetItem, _col: int):
        data = item.data(0, Qt.UserRole)
        if data is not None:
            self.question_selected.emit(data[0], data[1])

    def select(self, part: int, index: int):
        """Visually highlight the tree item for (part, index)."""
        target = (part, index)
        self.blockSignals(True)
        self.clearSelection()
        for i in range(self.topLevelItemCount()):
            top = self.topLevelItem(i)
            if top.data(0, Qt.UserRole) == target:
                top.setSelected(True)
                self.scrollToItem(top)
                break
            for j in range(top.childCount()):
                child = top.child(j)
                if child.data(0, Qt.UserRole) == target:
                    child.setSelected(True)
                    self.scrollToItem(child)
                    break
        self.blockSignals(False)


# ============================================================
# MAIN WINDOW
# ============================================================
class MainWindow(QMainWindow):
    # question counts per part (0 = Directions)
    _COUNTS = {0: 1, 1: 2, 2: 2, 3: 3, 4: 1, 5: 1}
    _TOTAL = 11

    def __init__(self):
        super().__init__()
        self.edit_mode = False
        self._part = 0
        self._idx = 0
        self._setup_ui()
        self._go_to(0, 0)  # Start at Directions

    def _setup_ui(self):
        self.setWindowTitle("TOEIC Speaking Practice")
        self.setMinimumSize(1200, 800)
        self.resize(1280, 850)

        self.setStyleSheet("""
            QMainWindow, QWidget { font-family: Arial; }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 6px;
                margin-top: 8px;
                background: white;
                padding-top: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
                color: #555;
            }
            QTabWidget::pane { border: 1px solid #ddd; border-radius: 4px; }
            QTabBar::tab {
                padding: 6px 16px;
                background: #ecf0f1;
                border: 1px solid #ddd;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                color: #666;
            }
            QTabBar::tab:selected { background: white; color: #2c3e50; font-weight: bold; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._build_toolbar()

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)

        # Left nav
        self.nav = NavTree()
        self.nav.question_selected.connect(self._go_to)
        splitter.addWidget(self.nav)

        # Center stacked widget
        self.stack = QStackedWidget()
        self.part_widgets: Dict[int, QWidget] = {}

        # Index 0: Directions
        dirs_widget = DirectionsWidget()
        dirs_sa = QScrollArea()
        dirs_sa.setWidget(dirs_widget)
        dirs_sa.setWidgetResizable(True)
        dirs_sa.setFrameShape(QFrame.NoFrame)
        self.part_widgets[0] = dirs_widget
        self.stack.addWidget(dirs_sa)  # stack index 0

        # Indices 1–5: Part widgets
        for part_num, WidgetClass in [
            (1, Part1Widget), (2, Part2Widget), (3, Part3Widget),
            (4, Part4Widget), (5, Part5Widget)
        ]:
            w = WidgetClass()
            sa = QScrollArea()
            sa.setWidget(w)
            sa.setWidgetResizable(True)
            sa.setFrameShape(QFrame.NoFrame)
            self.part_widgets[part_num] = w
            self.stack.addWidget(sa)  # stack index = part_num

        # Connect Part1 auto-advance signal
        self.part_widgets[1].question_changed.connect(self._on_part1_question_changed)

        splitter.addWidget(self.stack)

        # Right sidebar (reserved for recording)
        right = QFrame()
        right.setFixedWidth(155)
        right.setStyleSheet("background: white; border-left: 1px solid #e0e0e0;")
        rl = QVBoxLayout(right)
        rl.addStretch()
        icon_lbl = QLabel("🎙")
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setFont(QFont("Arial", 32))
        rec_lbl = QLabel("Recording\nFunction\n(Reserved)")
        rec_lbl.setAlignment(Qt.AlignCenter)
        rec_lbl.setStyleSheet("color: #bdc3c7; font-size: 11px;")
        rl.addWidget(icon_lbl)
        rl.addWidget(rec_lbl)
        rl.addStretch()
        splitter.addWidget(right)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)

        root.addWidget(splitter, 1)
        self._build_bottom_bar()
        root.addWidget(self.bottom_bar)

    def _build_toolbar(self):
        tb = QToolBar()
        tb.setMovable(False)
        tb.setFloatable(False)
        tb.setIconSize(QSize(20, 20))
        tb.setStyleSheet("""
            QToolBar {
                background: #2c3e50;
                border: none;
                padding: 6px 12px;
                spacing: 8px;
            }
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 6px 14px;
                font-size: 13px;
            }
            QPushButton:hover { background: #2980b9; }
            QCheckBox { color: #ecf0f1; font-size: 13px; spacing: 6px; }
            QLabel { color: white; }
        """)

        title = QLabel("  📖  TOEIC Speaking Practice")
        title.setFont(QFont("Arial", 15, QFont.Bold))
        tb.addWidget(title)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        tb.addWidget(spacer)

        if not TTS_AVAILABLE:
            warn = QLabel("⚠  TTS unavailable — install pyttsx3")
            warn.setStyleSheet("color: #f39c12; font-size: 11px;")
            tb.addWidget(warn)

        self.edit_cb = QCheckBox("Edit Mode")
        self.edit_cb.toggled.connect(self._toggle_edit)
        tb.addWidget(self.edit_cb)

        save_btn = QPushButton("💾  Save")
        save_btn.clicked.connect(self._save)
        tb.addWidget(save_btn)

        load_btn = QPushButton("📂  Load")
        load_btn.clicked.connect(self._load)
        tb.addWidget(load_btn)

        self.addToolBar(tb)

    def _build_bottom_bar(self):
        self.bottom_bar = QWidget()
        self.bottom_bar.setFixedHeight(62)
        self.bottom_bar.setStyleSheet("background: #34495e; border-top: 2px solid #2c3e50;")
        layout = QHBoxLayout(self.bottom_bar)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        def make_btn(text, color, hover):
            b = QPushButton(text)
            b.setMinimumHeight(36)
            b.setStyleSheet(
                f"QPushButton {{ background: {color}; color: white; border: none; "
                f"border-radius: 5px; padding: 4px 14px; font-size: 13px; }}"
                f"QPushButton:hover {{ background: {hover}; }}"
                f"QPushButton:disabled {{ background: #4a5568; color: #718096; }}"
            )
            return b

        self.prev_btn = make_btn("◀  Previous", "#7f8c8d", "#95a5a6")
        self.prev_btn.clicked.connect(self._go_prev)
        self.next_btn = make_btn("Next  ▶", "#7f8c8d", "#95a5a6")
        self.next_btn.clicked.connect(self._go_next)
        self.mark_btn = make_btn("★  Mark", "#8e44ad", "#9b59b6")
        self.mark_btn.clicked.connect(self._toggle_mark)
        quit_btn = make_btn("✕  Quit", "#c0392b", "#e74c3c")
        quit_btn.clicked.connect(self.close)

        self.pos_label = QLabel("")
        self.pos_label.setStyleSheet("color: #bdc3c7; font-size: 12px; font-weight: bold;")

        # ── Center: recording button ──────────────────────────────────────────
        self._record_thread: Optional[RecordThread] = None

        self.record_btn = QPushButton("🎙")
        self.record_btn.setFixedSize(46, 46)
        self.record_btn.setCheckable(True)
        self.record_btn.setToolTip(
            "Click to start recording your voice.\nClick again to stop and save."
            if PYAUDIO_AVAILABLE else
            "Recording unavailable — install pyaudio"
        )
        self.record_btn.setEnabled(PYAUDIO_AVAILABLE)
        self._rec_idle_style = """
            QPushButton {
                background: #c0392b; color: white;
                border-radius: 23px; font-size: 22px;
                border: 3px solid #e74c3c;
            }
            QPushButton:hover { background: #e74c3c; }
            QPushButton:disabled { background: #555; border-color: #666; }
        """
        self._rec_active_style = """
            QPushButton {
                background: #7b241c; color: white;
                border-radius: 23px; font-size: 22px;
                border: 3px solid #f1948a;
            }
        """
        self.record_btn.setStyleSheet(self._rec_idle_style)
        self.record_btn.clicked.connect(self._toggle_recording)

        self.rec_label = QLabel("Ready" if PYAUDIO_AVAILABLE else "No pyaudio")
        self.rec_label.setStyleSheet("color: #bdc3c7; font-size: 11px;")
        self.rec_label.setAlignment(Qt.AlignCenter)

        rec_col = QVBoxLayout()
        rec_col.setSpacing(2)
        rec_col.setContentsMargins(0, 0, 0, 0)
        rec_col.addWidget(self.record_btn, 0, Qt.AlignCenter)
        rec_col.addWidget(self.rec_label, 0, Qt.AlignCenter)

        layout.addWidget(self.prev_btn)
        layout.addWidget(self.next_btn)
        layout.addStretch()
        layout.addLayout(rec_col)
        layout.addStretch()
        layout.addWidget(self.pos_label)
        layout.addWidget(self.mark_btn)
        layout.addWidget(quit_btn)

    # ── Navigation ────────────────────────────────────────────────────────────

    def _current_widget(self) -> Optional[QWidget]:
        return self.part_widgets.get(self._part)

    def _check_timer_and_proceed(self) -> bool:
        """Return True if OK to navigate away from the current view."""
        w = self._current_widget()
        if w is None:
            return True

        running = False
        if hasattr(w, 'is_active'):
            running = w.is_active()
        elif hasattr(w, 'countdown'):
            running = w.countdown.is_running()

        if running:
            if self._part == 1:
                # Silently stop Part 1 without prompting
                if hasattr(w, '_cancel_all'):
                    w._cancel_all()
                elif hasattr(w, 'countdown'):
                    w.countdown.stop()
            else:
                reply = QMessageBox.question(
                    self, "Timer Running",
                    "A timer is currently running.\nStop it and navigate away?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return False
                if hasattr(w, '_cancel_all'):
                    w._cancel_all()
                elif hasattr(w, 'countdown'):
                    w.countdown.stop()
        return True

    def _go_to(self, part: int, index: int):
        if not self._check_timer_and_proceed():
            return

        # Cancel Part1 auto-flow if navigating away from Part1
        if self._part == 1 and part != 1:
            p1w = self.part_widgets.get(1)
            if p1w and hasattr(p1w, '_cancel_all'):
                p1w._cancel_all()

        self._part = part
        self._idx = index

        if part == 0:
            self.stack.setCurrentIndex(0)
        else:
            self.stack.setCurrentIndex(part)  # part 1→index 1, part 2→index 2, etc.
            w = self.part_widgets.get(part)
            if w:
                if part == 1 and index == -1:
                    w.show_intro()
                else:
                    w.load_question(index)

        self.nav.select(part, index)
        self._update_nav()

    def _on_part1_question_changed(self, idx: int):
        """Called when Part1 auto-advances to a new question."""
        self._idx = idx
        self.nav.select(1, idx)
        self._update_nav()

    def _update_nav(self):
        p, i = self._part, self._idx

        # Prev button: disabled only at the very start (Directions)
        can_prev = not (p == 0)
        # Next button: disabled only at the very end (Part5 last question)
        last_part = 5
        last_idx = self._COUNTS.get(last_part, 1) - 1
        can_next = not (p == last_part and i >= last_idx)

        self.prev_btn.setEnabled(can_prev)
        self.next_btn.setEnabled(can_next)

        # Position label
        q_start = {1: 1, 2: 3, 3: 5, 4: 8, 5: 11}
        if p == 0:
            self.pos_label.setText("TOEIC® Speaking Test Directions")
        elif p == 1 and i == -1:
            self.pos_label.setText("PART 1  •  Instructions")
        elif p == 4:
            self.pos_label.setText("PART 4  •  Questions 8 – 10 of 11")
        else:
            qs = q_start.get(p, 1) + i
            self.pos_label.setText(f"PART {p}  •  Question {qs} of {self._TOTAL}")

        # Mark button state
        marked = self._is_marked()
        self.mark_btn.setStyleSheet(
            "QPushButton { background: %s; color: white; border: none; border-radius: 5px; "
            "padding: 4px 14px; font-size: 13px; } QPushButton:hover { background: %s; }" %
            (("#f39c12", "#e67e22") if marked else ("#8e44ad", "#9b59b6"))
        )
        self.mark_btn.setText("★  Marked" if marked else "★  Mark")

    def _go_prev(self):
        if not self._check_timer_and_proceed():
            return
        p, i = self._part, self._idx
        if p == 0:
            return  # already at start
        if p == 1 and i <= -1:
            self._go_to(0, 0)
        elif p == 1 and i == 0:
            self._go_to(1, -1)
        elif i > 0:
            self._go_to(p, i - 1)
        elif p > 1:
            new_p = p - 1
            self._go_to(new_p, self._COUNTS[new_p] - 1)

    def _go_next(self):
        if not self._check_timer_and_proceed():
            return
        p, i = self._part, self._idx
        if p == 0:
            self._go_to(1, -1)
            return
        if p == 1 and i == -1:
            self._go_to(1, 0)
            return
        count = self._COUNTS.get(p, 1)
        if i < count - 1:
            self._go_to(p, i + 1)
        elif p < 5:
            self._go_to(p + 1, 0)

    def _is_marked(self) -> bool:
        p, i = self._part, self._idx
        if p == 0 or i < 0:
            return False
        if p == 2:
            data = cfg.part2()
            return i < len(data) and data[i].get('marked', False)
        if p == 3:
            qs = cfg.part3().get('questions', [])
            return i < len(qs) and qs[i].get('marked', False)
        if p == 5:
            data = cfg.part5()
            return i < len(data) and data[i].get('marked', False)
        return False

    def _toggle_mark(self):
        p, i = self._part, self._idx
        if p == 0 or i < 0:
            return
        if p == 2:
            data = cfg.part2()
            if i < len(data):
                data[i]['marked'] = not data[i].get('marked', False)
        elif p == 3:
            qs = cfg.part3().get('questions', [])
            if i < len(qs):
                qs[i]['marked'] = not qs[i].get('marked', False)
        elif p == 5:
            data = cfg.part5()
            if i < len(data):
                data[i]['marked'] = not data[i].get('marked', False)
        self._update_nav()

    def _toggle_edit(self, on: bool):
        if not on and self.edit_mode:
            reply = QMessageBox.question(
                self, "Save Changes",
                "Do you want to save your changes to the config file?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if reply == QMessageBox.Cancel:
                self.edit_cb.blockSignals(True)
                self.edit_cb.setChecked(True)
                self.edit_cb.blockSignals(False)
                return
            if reply == QMessageBox.Yes:
                self._save()

        self.edit_mode = on
        for w in self.part_widgets.values():
            w.set_edit_mode(on)

        self.edit_cb.setStyleSheet(
            "color: #f39c12; font-weight: bold; font-size: 13px;" if on
            else "color: #ecf0f1; font-size: 13px;"
        )

    def _save(self):
        if cfg.save():
            self.statusBar().showMessage("✓  Configuration saved successfully.", 4000)

    def _load(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Configuration", "", "JSON Files (*.json)"
        )
        if not path:
            return
        if cfg.load(path):
            for w in self.part_widgets.values():
                w.refresh()
            self.statusBar().showMessage(f"✓  Loaded: {os.path.basename(path)}", 4000)

    # ── Recording ─────────────────────────────────────────────────────────────

    def _toggle_recording(self):
        if self._record_thread and self._record_thread.isRunning():
            # Stop recording
            self._record_thread.request_stop()
        else:
            # Start recording
            ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            part = self._part
            idx  = self._idx
            if part == 0:
                q_str = "Directions"
            elif part == 1 and idx == -1:
                q_str = "P1_Intro"
            else:
                q_str = f"P{part}_Q{idx + 1}"
            filepath = os.path.join("recordings", f"{q_str}_{ts}.wav")

            self._record_thread = RecordThread(filepath)
            self._record_thread.record_started.connect(self._on_record_started)
            self._record_thread.record_finished.connect(self._on_record_finished)
            self._record_thread.start()

    def _on_record_started(self):
        self.record_btn.setStyleSheet(self._rec_active_style)
        self.rec_label.setText("● REC")
        self.rec_label.setStyleSheet("color: #e74c3c; font-size: 11px; font-weight: bold;")

    def _on_record_finished(self, filepath: str):
        self.record_btn.setChecked(False)
        self.record_btn.setStyleSheet(self._rec_idle_style)
        if filepath:
            name = os.path.basename(filepath)
            self.rec_label.setText(f"Saved: {name}")
            self.rec_label.setStyleSheet("color: #2ecc71; font-size: 10px;")
            self.statusBar().showMessage(f"✓  Recording saved: {filepath}", 5000)
        else:
            self.rec_label.setText("Error")
            self.rec_label.setStyleSheet("color: #e74c3c; font-size: 11px;")

    def closeEvent(self, event):
        tts.stop()
        # Stop any active recording
        if self._record_thread and self._record_thread.isRunning():
            self._record_thread.request_stop()
            self._record_thread.wait(3000)
        if self.edit_mode:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You are in edit mode. Save before quitting?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if reply == QMessageBox.Cancel:
                event.ignore()
                return
            if reply == QMessageBox.Yes:
                cfg.save()
        event.accept()


# ============================================================
# ENTRY POINT
# ============================================================
def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("recordings", exist_ok=True)

    app = QApplication(sys.argv)
    app.setApplicationName("TOEIC Speaking Practice")
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 246, 250))
    palette.setColor(QPalette.WindowText, QColor(44, 62, 80))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(240, 242, 245))
    palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(230, 232, 235))
    palette.setColor(QPalette.ButtonText, QColor(44, 62, 80))
    app.setPalette(palette)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
