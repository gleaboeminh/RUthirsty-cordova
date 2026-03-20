#!/usr/bin/env python3
"""
TOEIC Speaking Practice Tool
Supports PART 1-5 question/answer management with edit mode and JSON persistence.
"""

import sys
import json
import shutil
import os
import traceback
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QSplitter, QMessageBox, QFrame, QSizePolicy, QToolBar, QAction,
    QStatusBar, QScrollArea
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QIcon, QPalette

# When frozen by PyInstaller the exe lives in sys.executable's folder;
# otherwise use the directory of this script.
if getattr(sys, "frozen", False):
    _APP_DIR = os.path.dirname(sys.executable)
else:
    _APP_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(_APP_DIR, "toeic_speaking_config.json")

DEFAULT_DATA = {
    "part1": [
        {
            "question": "Read the following sentence aloud:\n\n\"The quarterly sales report shows a significant increase in revenue compared to last year.\"",
            "answer": "Focus on clear pronunciation of each word. Stress key words: 'quarterly', 'significant', 'increase', 'revenue'. Maintain a steady pace—neither too fast nor too slow. Aim for a natural rising-falling intonation.",
            "marked": False
        },
        {
            "question": "Read the following sentence aloud:\n\n\"Passengers are reminded to keep their belongings with them at all times during the flight.\"",
            "answer": "Pronounce 'passengers' and 'belongings' clearly. Use a polite, informational tone as if making an announcement. Pause slightly after 'reminded' for emphasis.",
            "marked": False
        },
        {
            "question": "Read the following sentence aloud:\n\n\"The new community center will open its doors to residents next Monday morning.\"",
            "answer": "Emphasize 'new', 'community center', and 'next Monday morning'. Use a warm, welcoming tone. Keep the delivery smooth without rushing through proper nouns.",
            "marked": False
        }
    ],
    "part2": [
        {
            "question": "Describe the photograph below in as much detail as possible.\n\n[Photo: A busy office environment with several people working at computers, some standing near a whiteboard covered in diagrams.]",
            "answer": "Sample response:\n\"In this photo, I can see a busy office setting. Several people are seated at their desks, working on computers. In the background, a group of colleagues appears to be having a discussion near a whiteboard that has various diagrams and charts drawn on it. The office looks modern, with open-plan seating. Everyone seems focused on their tasks, suggesting a productive work environment.\"",
            "marked": False
        },
        {
            "question": "Describe the photograph below in as much detail as possible.\n\n[Photo: An outdoor farmers' market with vendors selling fresh produce, shoppers browsing stalls, and colorful banners overhead.]",
            "answer": "Sample response:\n\"This photograph shows an outdoor farmers' market on what appears to be a sunny day. There are several vendors' stalls lined up, displaying a wide variety of fresh fruits and vegetables in colorful arrangements. Shoppers are walking along the market, examining the produce and speaking with vendors. Overhead, I can see colorful banners or flags decorating the area, adding to the festive atmosphere. The scene conveys a lively and community-oriented event.\"",
            "marked": False
        }
    ],
    "part3": [
        {
            "question": "You will be asked three questions about a topic. The topic is: Planning a team-building event for your department.\n\nQuestion 1: What kind of team-building activities do you think are most effective, and why?",
            "answer": "Sample response:\n\"I think outdoor activities like group challenges or sports are most effective because they require real cooperation and communication. For example, a scavenger hunt or an escape room forces team members to rely on each other's strengths, which directly improves workplace dynamics. These activities are memorable and fun, which helps build positive relationships beyond the office setting.\"",
            "marked": False
        },
        {
            "question": "Topic: Planning a team-building event for your department.\n\nQuestion 2: What factors should a manager consider when planning such an event?",
            "answer": "Sample response:\n\"A manager should consider several factors. First, the budget — the event must be affordable and justifiable. Second, the diversity of team members — activities should be inclusive for all fitness levels and backgrounds. Third, timing — the event should not conflict with busy work periods. Finally, the manager should gather team input beforehand to ensure the activity is something people genuinely want to do, which increases engagement and participation.\"",
            "marked": False
        },
        {
            "question": "Topic: Planning a team-building event for your department.\n\nQuestion 3: Describe a team-building event you participated in or would like to organize.",
            "answer": "Sample response:\n\"I once participated in a cooking class team-building event. Each group was assigned a dish to prepare together within a time limit. It was surprisingly effective — we had to delegate tasks, communicate clearly under pressure, and support each other when things went wrong. The best part was sharing the meal afterward. I'd love to organize something similar because it's low-pressure, creative, and universally enjoyable.\"",
            "marked": False
        }
    ],
    "part4": [
        {
            "question": "Respond to a voicemail message.\n\nYou will hear a voicemail from a client, Mr. Johnson, asking about the status of a product shipment that was supposed to arrive last Wednesday. He says he needs the items urgently for a presentation on Friday. He asks you to call him back at 555-0123.\n\nPlease respond to the voicemail as if you are the customer service representative.",
            "answer": "Sample response:\n\"Hello, Mr. Johnson. This is [your name] calling from [Company Name] in response to your voicemail. I sincerely apologize for the delay with your shipment. I've checked our system and I can confirm that your order was dispatched yesterday and is currently in transit. Based on the tracking information, it should be delivered by tomorrow afternoon, which means you'll have it well before your Friday presentation. If there are any further delays, please don't hesitate to contact us at 555-0199 and we'll arrange an express alternative. Again, I'm sorry for the inconvenience, and thank you for your patience.\"",
            "marked": False
        },
        {
            "question": "Respond to a voicemail message.\n\nYou receive a voicemail from a colleague, Sarah, asking if the weekly team meeting scheduled for 3 PM on Thursday has been moved. She says she heard a rumor it might be rescheduled and wants to confirm, as she has a client call at 4 PM.\n\nPlease respond to the voicemail as her team member.",
            "answer": "Sample response:\n\"Hi Sarah, it's [your name] returning your call. Yes, you heard correctly — the Thursday team meeting has been moved. It's now scheduled for 10 AM on Thursday instead of 3 PM. The change was made to accommodate the manager's schedule. So your 4 PM client call won't be affected at all. I'll also forward you the updated calendar invite. Let me know if you have any other questions!\"",
            "marked": False
        }
    ],
    "part5": [
        {
            "question": "Express an opinion on the following topic and support your view with reasons and examples. You have 60 seconds to respond.\n\nTopic: Do you think remote work is more beneficial or more harmful for employees? Use specific reasons and examples to support your answer.",
            "answer": "Sample response:\n\"I believe remote work is overall more beneficial for employees, and I'd like to explain why.\n\nFirst, remote work significantly improves work-life balance. Employees save commuting time — sometimes two or more hours per day — which they can use for exercise, family, or rest. This directly improves mental health and job satisfaction.\n\nSecond, studies have shown that many people are actually more productive at home. Without the constant interruptions of an open-plan office, workers can focus deeply on complex tasks.\n\nHowever, I do acknowledge challenges, particularly around collaboration and social isolation. To address this, companies can implement regular video meetings and occasional in-person meetups.\n\nIn conclusion, when managed properly with clear communication tools and flexible policies, remote work offers employees greater autonomy and wellbeing, making it a net positive.\"",
            "marked": False
        },
        {
            "question": "Express an opinion on the following topic and support your view with reasons and examples. You have 60 seconds to respond.\n\nTopic: Some people believe that companies should prioritize hiring experienced workers over recent graduates. Do you agree or disagree? Give reasons and examples.",
            "answer": "Sample response:\n\"I partially disagree with the idea that companies should always prioritize experienced workers over graduates. While experience is undeniably valuable, recent graduates bring unique advantages that shouldn't be overlooked.\n\nOn one hand, experienced workers can contribute immediately without extensive training, reducing onboarding costs and time. Their industry knowledge helps avoid common mistakes.\n\nOn the other hand, recent graduates tend to be up-to-date with the latest technologies and research. For example, in fields like software development or digital marketing, a fresh graduate may have more current technical skills than someone who graduated ten years ago.\n\nMoreover, graduates are often more adaptable and open to a company's specific culture and processes, since they haven't developed rigid habits from previous roles.\n\nTherefore, the ideal approach is a balanced hiring strategy — experienced employees for senior roles requiring judgment, and graduates for roles requiring fresh perspectives and technical currency.\"",
            "marked": False
        }
    ]
}


class TOEICSpeakingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.parts_data = {}
        self.edit_mode = False
        self.modified = False
        self.current_part = "part1"
        self.current_index = 0

        self.load_or_init_data()
        self.init_ui()
        self.refresh_tree()
        self.select_question("part1", 0)

    # ── Data I/O ──────────────────────────────────────────────────────────────

    def load_or_init_data(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.parts_data = json.load(f)
                return
            except Exception as e:
                QMessageBox.warning(self, "加载失败", f"配置文件读取失败，将使用默认数据。\n{e}")
        self.parts_data = json.loads(json.dumps(DEFAULT_DATA))
        self.save_data(silent=True)

    def save_data(self, silent=False):
        try:
            if os.path.exists(CONFIG_FILE):
                shutil.copy(CONFIG_FILE, CONFIG_FILE + ".bak")
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.parts_data, f, ensure_ascii=False, indent=2)
            self.modified = False
            self.update_title()
            if not silent:
                self.statusBar().showMessage("已保存到 " + CONFIG_FILE, 3000)
        except Exception as e:
            QMessageBox.critical(self, "保存失败", str(e))

    # ── UI Construction ───────────────────────────────────────────────────────

    def init_ui(self):
        self.setWindowTitle("TOEIC Speaking Practice")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(self._stylesheet())

        # ── Toolbar ───────────────────────────────────────────────────────────
        toolbar = QToolBar("主工具栏")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        title_label = QLabel("  TOEIC Speaking Practice  ")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        toolbar.addWidget(title_label)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        self.edit_btn = QPushButton("编辑模式: 关")
        self.edit_btn.setCheckable(True)
        self.edit_btn.setFixedWidth(130)
        self.edit_btn.setStyleSheet(
            "QPushButton{background:#bdc3c7;color:#2c3e50;border-radius:4px;padding:4px 8px;font-weight:bold;}"
            "QPushButton:checked{background:#e67e22;color:white;}"
        )
        self.edit_btn.toggled.connect(self.toggle_edit_mode)
        toolbar.addWidget(self.edit_btn)

        toolbar.addSeparator()

        save_btn = QPushButton("💾 保存")
        save_btn.setFixedWidth(80)
        save_btn.clicked.connect(self.on_save)
        toolbar.addWidget(save_btn)

        load_btn = QPushButton("📂 加载")
        load_btn.setFixedWidth(80)
        load_btn.clicked.connect(self.on_load)
        toolbar.addWidget(load_btn)

        toolbar.addWidget(QLabel("  "))

        # ── Status Bar ────────────────────────────────────────────────────────
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("就绪")

        # ── Central Widget ────────────────────────────────────────────────────
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        main_layout.addWidget(splitter, 1)

        # Left sidebar
        left_widget = self._build_left_sidebar()
        splitter.addWidget(left_widget)

        # Center area
        center_widget = self._build_center_area()
        splitter.addWidget(center_widget)

        # Right sidebar
        right_widget = self._build_right_sidebar()
        splitter.addWidget(right_widget)

        splitter.setSizes([220, 740, 240])
        splitter.setStretchFactor(1, 1)

        # ── Bottom toolbar ────────────────────────────────────────────────────
        bottom_bar = self._build_bottom_bar()
        main_layout.addWidget(bottom_bar)

        # Shortcuts
        from PyQt5.QtWidgets import QShortcut
        from PyQt5.QtGui import QKeySequence
        QShortcut(QKeySequence("Ctrl+S"), self, self.on_save)
        QShortcut(QKeySequence("Ctrl+E"), self, self.edit_btn.toggle)
        QShortcut(QKeySequence(Qt.Key_Left), self, self.on_prev)
        QShortcut(QKeySequence(Qt.Key_Right), self, self.on_next)

    def _build_left_sidebar(self):
        widget = QWidget()
        widget.setMinimumWidth(180)
        widget.setMaximumWidth(280)
        widget.setStyleSheet("background:#2c3e50;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("  题目导航")
        header.setFixedHeight(36)
        header.setStyleSheet("background:#1a252f;color:white;font-weight:bold;font-size:13px;padding-left:8px;")
        layout.addWidget(header)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet(
            "QTreeWidget{background:#2c3e50;color:white;border:none;font-size:13px;}"
            "QTreeWidget::item{padding:4px 2px;}"
            "QTreeWidget::item:selected{background:#e67e22;color:white;border-radius:3px;}"
            "QTreeWidget::item:hover{background:#34495e;}"
            "QTreeWidget::branch{background:#2c3e50;}"
        )
        self.tree.itemClicked.connect(self.on_tree_item_clicked)
        layout.addWidget(self.tree, 1)

        self.add_question_btn = QPushButton("＋ 添加题目")
        self.add_question_btn.setFixedHeight(36)
        self.add_question_btn.setStyleSheet(
            "QPushButton{background:#27ae60;color:white;border:none;font-weight:bold;font-size:13px;}"
            "QPushButton:hover{background:#2ecc71;}"
        )
        self.add_question_btn.clicked.connect(self.on_add_question)
        self.add_question_btn.setVisible(False)
        layout.addWidget(self.add_question_btn)

        return widget

    def _build_center_area(self):
        widget = QWidget()
        widget.setStyleSheet("background:#f5f6fa;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(12)

        # Question number label
        self.question_label = QLabel("PART 1 – 第 1 题")
        self.question_label.setFont(QFont("Arial", 15, QFont.Bold))
        self.question_label.setStyleSheet("color:#2c3e50;")
        layout.addWidget(self.question_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#dfe6e9;")
        layout.addWidget(sep)

        # Question text
        q_header = QLabel("题目内容")
        q_header.setFont(QFont("Arial", 11, QFont.Bold))
        q_header.setStyleSheet("color:#7f8c8d;text-transform:uppercase;")
        layout.addWidget(q_header)

        self.question_edit = QTextEdit()
        self.question_edit.setFont(QFont("Arial", 13))
        self.question_edit.setMinimumHeight(140)
        self.question_edit.setMaximumHeight(240)
        self.question_edit.setReadOnly(True)
        self.question_edit.setStyleSheet(
            "QTextEdit{background:white;border:1px solid #dfe6e9;border-radius:6px;"
            "padding:10px;color:#2c3e50;line-height:1.5;}"
        )
        self.question_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.question_edit)

        # Answer section
        answer_frame = QFrame()
        answer_frame.setStyleSheet(
            "QFrame{background:white;border:1px solid #dfe6e9;border-radius:8px;}"
        )
        answer_layout = QVBoxLayout(answer_frame)
        answer_layout.setContentsMargins(0, 0, 0, 0)
        answer_layout.setSpacing(0)

        answer_header_widget = QWidget()
        answer_header_widget.setStyleSheet(
            "QWidget{background:#3498db;border-radius:7px 7px 0 0;}"
        )
        answer_header_layout = QHBoxLayout(answer_header_widget)
        answer_header_layout.setContentsMargins(12, 8, 12, 8)

        ans_title = QLabel("参考答案")
        ans_title.setFont(QFont("Arial", 11, QFont.Bold))
        ans_title.setStyleSheet("color:white;background:transparent;border:none;")
        answer_header_layout.addWidget(ans_title)

        answer_header_layout.addStretch()

        self.toggle_answer_btn = QPushButton("▼ 展开")
        self.toggle_answer_btn.setFixedSize(70, 26)
        self.toggle_answer_btn.setStyleSheet(
            "QPushButton{background:rgba(255,255,255,0.2);color:white;border-radius:4px;"
            "font-size:12px;border:none;}"
            "QPushButton:hover{background:rgba(255,255,255,0.35);}"
        )
        self.toggle_answer_btn.clicked.connect(self.toggle_answer_visibility)
        answer_header_layout.addWidget(self.toggle_answer_btn)

        answer_layout.addWidget(answer_header_widget)

        self.answer_edit = QTextEdit()
        self.answer_edit.setFont(QFont("Arial", 12))
        self.answer_edit.setReadOnly(True)
        self.answer_edit.setMinimumHeight(180)
        self.answer_edit.setStyleSheet(
            "QTextEdit{background:white;border:none;border-radius:0 0 7px 7px;"
            "padding:12px;color:#2c3e50;line-height:1.6;}"
        )
        self.answer_edit.setVisible(False)
        self.answer_edit.textChanged.connect(self.on_text_changed)
        answer_layout.addWidget(self.answer_edit)

        layout.addWidget(answer_frame, 1)

        return widget

    def _build_right_sidebar(self):
        widget = QWidget()
        widget.setMinimumWidth(200)
        widget.setMaximumWidth(300)
        widget.setStyleSheet("background:#ecf0f1;border-left:1px solid #dfe6e9;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(12)

        title = QLabel("操作面板")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("color:#2c3e50;")
        layout.addWidget(title)

        view_ans_btn = QPushButton("👁  查看参考答案")
        view_ans_btn.setFixedHeight(38)
        view_ans_btn.setStyleSheet(
            "QPushButton{background:#3498db;color:white;border-radius:6px;"
            "font-size:13px;font-weight:bold;border:none;}"
            "QPushButton:hover{background:#2980b9;}"
        )
        view_ans_btn.clicked.connect(lambda: self.set_answer_visible(True))
        layout.addWidget(view_ans_btn)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#bdc3c7;")
        layout.addWidget(sep)

        record_label = QLabel("🎙  录音功能")
        record_label.setFont(QFont("Arial", 11, QFont.Bold))
        record_label.setStyleSheet("color:#7f8c8d;")
        layout.addWidget(record_label)

        record_placeholder = QLabel("（预留扩展区域）\n\n录音、回放、波形\n显示等功能将在\n后续版本中添加。")
        record_placeholder.setAlignment(Qt.AlignCenter)
        record_placeholder.setStyleSheet(
            "color:#95a5a6;background:#dfe6e9;border-radius:8px;padding:20px;"
            "font-size:12px;line-height:1.5;"
        )
        record_placeholder.setFixedHeight(140)
        layout.addWidget(record_placeholder)

        layout.addStretch()

        # Stats panel
        stats_frame = QFrame()
        stats_frame.setStyleSheet(
            "QFrame{background:white;border-radius:8px;border:1px solid #dfe6e9;}"
        )
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setContentsMargins(12, 10, 12, 10)

        stats_title = QLabel("题库统计")
        stats_title.setFont(QFont("Arial", 10, QFont.Bold))
        stats_title.setStyleSheet("color:#7f8c8d;background:transparent;border:none;")
        stats_layout.addWidget(stats_title)

        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color:#2c3e50;font-size:12px;background:transparent;border:none;")
        self.stats_label.setWordWrap(True)
        stats_layout.addWidget(self.stats_label)

        layout.addWidget(stats_frame)

        return widget

    def _build_bottom_bar(self):
        bar = QWidget()
        bar.setFixedHeight(52)
        bar.setStyleSheet("background:#2c3e50;border-top:1px solid #1a252f;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(10)

        btn_style = (
            "QPushButton{background:#34495e;color:white;border-radius:5px;"
            "font-size:13px;padding:4px 16px;border:none;}"
            "QPushButton:hover{background:#4a6278;}"
            "QPushButton:pressed{background:#1a252f;}"
        )

        prev_btn = QPushButton("◀  上一题")
        prev_btn.setFixedHeight(36)
        prev_btn.setStyleSheet(btn_style)
        prev_btn.clicked.connect(self.on_prev)
        layout.addWidget(prev_btn)

        next_btn = QPushButton("下一题  ▶")
        next_btn.setFixedHeight(36)
        next_btn.setStyleSheet(btn_style)
        next_btn.clicked.connect(self.on_next)
        layout.addWidget(next_btn)

        layout.addStretch()

        self.mark_btn = QPushButton("☆  标记本题")
        self.mark_btn.setFixedHeight(36)
        self.mark_btn.setStyleSheet(
            "QPushButton{background:#8e44ad;color:white;border-radius:5px;"
            "font-size:13px;padding:4px 16px;border:none;}"
            "QPushButton:hover{background:#9b59b6;}"
        )
        self.mark_btn.clicked.connect(self.on_mark)
        layout.addWidget(self.mark_btn)

        layout.addStretch()

        quit_btn = QPushButton("✕  退出")
        quit_btn.setFixedHeight(36)
        quit_btn.setStyleSheet(
            "QPushButton{background:#c0392b;color:white;border-radius:5px;"
            "font-size:13px;padding:4px 16px;border:none;}"
            "QPushButton:hover{background:#e74c3c;}"
        )
        quit_btn.clicked.connect(self.close)
        layout.addWidget(quit_btn)

        return bar

    def _stylesheet(self):
        return """
            QMainWindow { background: #f5f6fa; }
            QToolBar { background: #ecf0f1; border-bottom: 1px solid #dfe6e9; padding: 4px; spacing: 6px; }
            QToolBar QPushButton { border-radius: 4px; padding: 4px 12px; font-size: 13px; border: none;
                background: #3498db; color: white; }
            QToolBar QPushButton:hover { background: #2980b9; }
            QSplitter::handle { background: #dfe6e9; }
            QScrollBar:vertical { border: none; background: #ecf0f1; width: 8px; }
            QScrollBar::handle:vertical { background: #bdc3c7; border-radius: 4px; }
            QStatusBar { background: #ecf0f1; color: #7f8c8d; font-size: 12px; }
        """

    # ── Tree ──────────────────────────────────────────────────────────────────

    def refresh_tree(self):
        self.tree.blockSignals(True)
        self.tree.clear()
        part_names = {
            "part1": "PART 1  朗读句子",
            "part2": "PART 2  图片描述",
            "part3": "PART 3  应答问题",
            "part4": "PART 4  回应留言",
            "part5": "PART 5  表达观点",
        }
        for part_key, part_label in part_names.items():
            part_item = QTreeWidgetItem([part_label])
            part_item.setData(0, Qt.UserRole, ("part", part_key))
            part_item.setFont(0, QFont("Arial", 12, QFont.Bold))
            part_item.setForeground(0, QColor("#ecf0f1"))
            questions = self.parts_data.get(part_key, [])
            for i, q in enumerate(questions):
                label = f"  {'★' if q.get('marked') else '○'}  第 {i+1} 题"
                q_item = QTreeWidgetItem([label])
                q_item.setData(0, Qt.UserRole, ("question", part_key, i))
                q_item.setForeground(0, QColor("#bdc3c7"))
                q_item.setFont(0, QFont("Arial", 11))
                part_item.addChild(q_item)
            self.tree.addTopLevelItem(part_item)
            part_item.setExpanded(True)
        self.tree.blockSignals(False)
        self.update_stats()

    def on_tree_item_clicked(self, item, column):
        data = item.data(0, Qt.UserRole)
        if data and data[0] == "question":
            _, part_key, idx = data
            self.select_question(part_key, idx)

    def highlight_tree_item(self, part_key, idx):
        root = self.tree.invisibleRootItem()
        part_keys = list(["part1", "part2", "part3", "part4", "part5"])
        for pi in range(root.childCount()):
            p_item = root.child(pi)
            p_data = p_item.data(0, Qt.UserRole)
            if p_data and p_data[1] == part_key:
                for qi in range(p_item.childCount()):
                    q_item = p_item.child(qi)
                    q_data = q_item.data(0, Qt.UserRole)
                    if q_data and q_data[2] == idx:
                        self.tree.setCurrentItem(q_item)
                        return

    # ── Question display ──────────────────────────────────────────────────────

    def select_question(self, part_key, idx):
        questions = self.parts_data.get(part_key, [])
        if not questions:
            self.current_part = part_key
            self.current_index = 0
            self.question_label.setText(self._part_display(part_key) + " – （暂无题目）")
            self.question_edit.blockSignals(True)
            self.question_edit.setText("")
            self.question_edit.blockSignals(False)
            self.answer_edit.blockSignals(True)
            self.answer_edit.setText("")
            self.answer_edit.blockSignals(False)
            return

        idx = max(0, min(idx, len(questions) - 1))
        self.current_part = part_key
        self.current_index = idx
        q = questions[idx]

        self.question_label.setText(
            f"{self._part_display(part_key)} – 第 {idx+1} 题  "
            + ("★" if q.get("marked") else "")
        )

        self.question_edit.blockSignals(True)
        self.question_edit.setText(q.get("question", ""))
        self.question_edit.blockSignals(False)

        self.answer_edit.blockSignals(True)
        self.answer_edit.setText(q.get("answer", ""))
        self.answer_edit.blockSignals(False)

        self.set_answer_visible(False)
        self.highlight_tree_item(part_key, idx)
        self._update_mark_btn(q.get("marked", False))

    def _part_display(self, part_key):
        names = {
            "part1": "PART 1",
            "part2": "PART 2",
            "part3": "PART 3",
            "part4": "PART 4",
            "part5": "PART 5",
        }
        return names.get(part_key, part_key.upper())

    def _update_mark_btn(self, marked):
        if marked:
            self.mark_btn.setText("★  取消标记")
            self.mark_btn.setStyleSheet(
                "QPushButton{background:#f39c12;color:white;border-radius:5px;"
                "font-size:13px;padding:4px 16px;border:none;}"
                "QPushButton:hover{background:#e67e22;}"
            )
        else:
            self.mark_btn.setText("☆  标记本题")
            self.mark_btn.setStyleSheet(
                "QPushButton{background:#8e44ad;color:white;border-radius:5px;"
                "font-size:13px;padding:4px 16px;border:none;}"
                "QPushButton:hover{background:#9b59b6;}"
            )

    # ── Edit mode ─────────────────────────────────────────────────────────────

    def toggle_edit_mode(self, checked):
        if not checked and self.modified:
            reply = QMessageBox.question(
                self, "未保存的修改",
                "当前有未保存的修改，是否保存？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Cancel:
                self.edit_btn.blockSignals(True)
                self.edit_btn.setChecked(True)
                self.edit_btn.blockSignals(False)
                return
            elif reply == QMessageBox.Save:
                self.save_data()

        self.edit_mode = checked
        self.edit_btn.setText("编辑模式: 开" if checked else "编辑模式: 关")
        self.question_edit.setReadOnly(not checked)
        self.answer_edit.setReadOnly(not checked)
        self.add_question_btn.setVisible(checked)

        # Show/hide delete icons by rebuilding tree
        self.refresh_tree()
        self.highlight_tree_item(self.current_part, self.current_index)
        self.statusBar().showMessage("编辑模式已" + ("开启" if checked else "关闭"), 2000)

    def on_text_changed(self):
        if not self.edit_mode:
            return
        questions = self.parts_data.get(self.current_part, [])
        if not questions or self.current_index >= len(questions):
            return
        q = questions[self.current_index]
        q["question"] = self.question_edit.toPlainText()
        q["answer"] = self.answer_edit.toPlainText()
        self.modified = True
        self.update_title()

    # ── Add / Delete ──────────────────────────────────────────────────────────

    def on_add_question(self):
        if not self.edit_mode:
            return
        new_q = {"question": "新题目（请在此输入题目内容）", "answer": "", "marked": False}
        self.parts_data[self.current_part].append(new_q)
        self.modified = True
        idx = len(self.parts_data[self.current_part]) - 1
        self.refresh_tree()
        self.select_question(self.current_part, idx)

    def delete_question(self, part_key, idx):
        if not self.edit_mode:
            return
        questions = self.parts_data.get(part_key, [])
        if not questions:
            return
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除 {self._part_display(part_key)} 第 {idx+1} 题吗？此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            questions.pop(idx)
            self.modified = True
            new_idx = min(idx, len(questions) - 1) if questions else 0
            self.refresh_tree()
            self.select_question(part_key, new_idx)

    def contextMenuEvent(self, event):
        if not self.edit_mode:
            return
        item = self.tree.itemAt(self.tree.mapFromGlobal(event.globalPos()))
        if item is None:
            return
        data = item.data(0, Qt.UserRole)
        if data and data[0] == "question":
            from PyQt5.QtWidgets import QMenu
            menu = QMenu(self)
            delete_action = menu.addAction("🗑  删除此题")
            action = menu.exec_(event.globalPos())
            if action == delete_action:
                _, part_key, idx = data
                self.delete_question(part_key, idx)

    # ── Navigation ────────────────────────────────────────────────────────────

    def on_prev(self):
        self._commit_current_edits()
        part_keys = ["part1", "part2", "part3", "part4", "part5"]
        questions = self.parts_data.get(self.current_part, [])
        if self.current_index > 0:
            self.select_question(self.current_part, self.current_index - 1)
        else:
            ci = part_keys.index(self.current_part)
            if ci > 0:
                prev_part = part_keys[ci - 1]
                prev_qs = self.parts_data.get(prev_part, [])
                self.select_question(prev_part, max(0, len(prev_qs) - 1))

    def on_next(self):
        self._commit_current_edits()
        part_keys = ["part1", "part2", "part3", "part4", "part5"]
        questions = self.parts_data.get(self.current_part, [])
        if self.current_index < len(questions) - 1:
            self.select_question(self.current_part, self.current_index + 1)
        else:
            ci = part_keys.index(self.current_part)
            if ci < len(part_keys) - 1:
                self.select_question(part_keys[ci + 1], 0)

    def _commit_current_edits(self):
        """Sync text boxes → data model before navigating away."""
        if self.edit_mode:
            questions = self.parts_data.get(self.current_part, [])
            if questions and self.current_index < len(questions):
                questions[self.current_index]["question"] = self.question_edit.toPlainText()
                questions[self.current_index]["answer"] = self.answer_edit.toPlainText()

    # ── Mark ──────────────────────────────────────────────────────────────────

    def on_mark(self):
        questions = self.parts_data.get(self.current_part, [])
        if not questions or self.current_index >= len(questions):
            return
        q = questions[self.current_index]
        q["marked"] = not q.get("marked", False)
        self.modified = True
        self._update_mark_btn(q["marked"])
        self.question_label.setText(
            f"{self._part_display(self.current_part)} – 第 {self.current_index+1} 题  "
            + ("★" if q["marked"] else "")
        )
        self.refresh_tree()
        self.highlight_tree_item(self.current_part, self.current_index)
        self.update_title()

    # ── Answer visibility ─────────────────────────────────────────────────────

    def toggle_answer_visibility(self):
        visible = not self.answer_edit.isVisible()
        self.set_answer_visible(visible)

    def set_answer_visible(self, visible):
        self.answer_edit.setVisible(visible)
        self.toggle_answer_btn.setText("▲ 收起" if visible else "▼ 展开")

    # ── Save / Load ───────────────────────────────────────────────────────────

    def on_save(self):
        self._commit_current_edits()
        self.save_data()

    def on_load(self):
        if self.modified:
            reply = QMessageBox.question(
                self, "未保存的修改",
                "重新加载将丢失当前未保存的修改，确定继续吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        self.load_or_init_data()
        self.modified = False
        self.refresh_tree()
        self.select_question("part1", 0)
        self.statusBar().showMessage("配置文件已重新加载", 3000)

    # ── Stats & title ─────────────────────────────────────────────────────────

    def update_stats(self):
        total = sum(len(v) for v in self.parts_data.values())
        marked = sum(
            1 for qs in self.parts_data.values()
            for q in qs if q.get("marked")
        )
        lines = []
        for pk in ["part1", "part2", "part3", "part4", "part5"]:
            count = len(self.parts_data.get(pk, []))
            lines.append(f"PART {pk[-1]}: {count} 题")
        lines.append(f"\n共 {total} 题  |  已标记 {marked} 题")
        self.stats_label.setText("\n".join(lines))

    def update_title(self):
        mark = " *" if self.modified else ""
        self.setWindowTitle(f"TOEIC Speaking Practice{mark}")

    # ── Close ─────────────────────────────────────────────────────────────────

    def closeEvent(self, event):
        if self.modified:
            reply = QMessageBox.question(
                self, "退出确认",
                "当前有未保存的修改，退出前是否保存？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.save_data()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("TOEIC Speaking Practice")
        app.setStyle("Fusion")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f5f6fa"))
        palette.setColor(QPalette.WindowText, QColor("#2c3e50"))
        app.setPalette(palette)

        window = TOEICSpeakingApp()
        window.show()
        sys.exit(app.exec_())
    except Exception:
        # In --windowed mode there is no console; surface the error visually.
        try:
            err = traceback.format_exc()
            app2 = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.critical(None, "启动失败", err)
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
