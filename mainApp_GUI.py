import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QScrollArea,
                             QVBoxLayout, QWidget, QGraphicsDropShadowEffect, 
                             QTextEdit, QSizePolicy)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtGui import QColor, QTextOption, QIcon, QFont, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # set window title and size

        self.setWindowTitle("Logo Brand")
        self.setWindowIcon(QIcon("play_btn.png"))
        self.setMinimumSize(800, 600)
        self.setStyleSheet("Background-color: White;")
        QApplication.setWindowIcon(QIcon('play_btn.png'))
        

        # Shadows
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))

        # create main widget and layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)

        # tile Widget
        self.title = QLabel()
        self.title.setText('Title')
        self.title.setStyleSheet("""
        font-size: 18px;
        font-weight: 350;
        letter-spacing: 2px;
        """)
        # self.main_layout.addWidget(self.title)

        # Title and Button
        self.title_and_button = QWidget()
        self.title_and_button_layout = QHBoxLayout(self.title_and_button)
        self.title_and_button_layout.addWidget(self.title)
        

        # Buttons
        self.buttons_widget = QWidget()
        self.button_layout = QHBoxLayout(self.buttons_widget)

        self.save_btn = QPushButton("save")
        self.import_btn = QPushButton("import")
        self.export_btn = QPushButton("export")

        # Set Shadow to buttons
        ## Bug for for adding shadow
        
        self.save_btn.setGraphicsEffect(self.shadow)
        self.import_btn.setGraphicsEffect(self.shadow)
        self.export_btn.setGraphicsEffect(self.shadow)

        # Buttons Design
        # save_btn
        self.save_btn.setMouseTracking(True)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1d86d0; 
                Border: none; 
                border-radius: 12px;
                color: white;
                font-size: 18px;
                padding-bottom: 2px;

            }
            QPushButton:hover {
                background-color:#1d41FF;
            }
            QPushButton:pressed {
                background-color: #1d86d0;
            }
        """)
        self.save_btn.setFixedSize(QSize(85, 25))

        # import_btn 
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #4b4b4b; 
                Border: none; 
                border-radius: 12px;
                color: white;
                font-size: 18px;
                padding-bottom: 2px;
                }
            QPushButton:hover {
                background-color:black;
            }
            QPushButton:pressed {
                background-color: #4b4b4b;
            }
        """)

        self.import_btn.setFixedSize(QSize(85, 25))

        # Export btn
        self.export_btn.setStyleSheet("""
           QPushButton {
                background-color: #4b4b4b; 
                Border: none; 
                border-radius: 12px;
                color: white;
                font-size: 18px;
                padding-bottom: 2px;
                }
            QPushButton:hover {
                background-color:black;
            }
            QPushButton:pressed {
                background-color: #4b4b4b;
            }
        """)

        self.export_btn.setFixedSize(QSize(85, 25))
        self.add_frame_button = QPushButton("+")
        self.add_frame_button.setFixedSize(QSize(25, 25))
        self.add_frame_button.clicked.connect(self.add_new_frame)
        self.add_frame_button.setStyleSheet("""
            QPushButton {
                background-color: #1d86d0; 
                Border: none; 
                border-radius: 12px;
                color: white;
                font-size: 18px;
                padding-bottom: 2px;
             }
             QPushButton:hover {
                background-color: #1d41FF; 
             }
             QPushButton:pressed {
                background-color: #1d86d0;
            }

            
         """)

# ------------------------------------------------------------
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.add_frame_button)
        self.button_layout.addWidget(self.import_btn)
        self.button_layout.addWidget(self.export_btn)
        self.button_layout.addWidget(self.save_btn)





        self.title_and_button_layout.addWidget(self.buttons_widget)
        self.main_layout.addWidget(self.title_and_button)
        

        
        # create scroll area and add to main layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setMinimumHeight(300)
        # Scroll area Layout Manager
        self.scroll_area.setWidgetResizable(True)


        self.main_layout.addWidget(self.scroll_area)

        # Scroll Area Layout Designs
        self.scroll_area.setStyleSheet("""
            border: none;
            background-color: #e9e9e9;
            border-radius: 20px
        """)
        self.scroll_area.setGraphicsEffect(self.shadow)
        

        # create container widget for scroll area
        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        # create layout for container widget
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_layout.setAlignment(Qt.AlignTop)

        # create button to add new frames
        # self.add_frame_button = QPushButton("add")
        # self.add_frame_button.setStyleSheet("""
        #     background-color: #1d86d0; 
        #     Border: none; 
        #     border-radius: 12px;
        #     color: white;
        #     font-size: 18px;
        #     padding-bottom: 2px;
            
        # """)

        # # self.dummy_label = QLabel(" ") # added empty label for spacing hahah
        # # self.main_layout.addWidget(self.dummy_label)
        # self.add_frame_button.setFixedSize(QSize(85, 25))
        # self.add_frame_button.clicked.connect(self.add_new_frame)
        # self.main_layout.addWidget(self.add_frame_button)

        # Visulizer Module
        # Recording Widget
        self.visualizer = QFrame()
        self.visualizer_layout = QHBoxLayout(self.visualizer)
        self.visualizer.setMaximumHeight(50)

        # Dummy Content
        self.visualizer.setMinimumHeight(150)
        

        # Create a Matplotlib Figure object
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.fig.add_subplot(111)

        # Create a Matplotlib canvas and add it to the main window
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.visualizer)  

        self.visualizer_layout.addWidget(self.canvas)





        self.record_widget = QWidget()
        self.record_widget_layout = QVBoxLayout(self.record_widget)
        

   
        # Record Widget Layout Size
       

        self.record = QPushButton("REC")
        self.play = QPushButton()
        self.pause = QPushButton()

        # Buttons Design PLAY/RECORD/RESTART

        self.pause.setStyleSheet("""
        QPushButton {
            background-color:#b7b7b7; 
            Border: none; 
            border-radius: 20px;
            color: white;
            font-size: 18px;
        }

        QPushButton:hover {
            background-color:black;

        }
        QPushButton:pressed {
            background-color:#b7b7b7;

        }
            

        """)
        
        self.record.setStyleSheet("""
        QPushButton {
            background-color: red; 
            Border: none; 
            border-radius: 22px;
            color: white;
            font-size: 18px;
            padding-bottom: 2px;
            }
        QPushButton:hover {
            background-color:#a70000;

        }
        QPushButton:pressed {
            background-color:red;
        }
        """)

        self.play.setStyleSheet(""" 
        QPushButton {
            Border: none; 
            border-radius: 20px;
            color: black;
            font-size: 18px;
        }
        QPushButton:hover {
            border: 1px solid black;
        }
        QPushButton:pressed {
            border: 0px solid black;
        }
            
               
        """)

        # Set Buttons Sizes
        self.record.setFixedSize(QSize(45, 45))
        self.pause.setFixedSize(QSize(40, 40))
        self.play.setFixedSize(QSize(45, 45))


        #Set Icons To buttons
        self.play.setIcon(QIcon("play_btn.png"))
        self.play.setIconSize(QSize(41,40))

        self.pause.setIcon(QIcon("pause-btn.png"))
        self.pause.setIconSize(QSize(28,28))

        # Qt Timer
        self.timer = QLabel("00:00:00")
        self.timer.setStyleSheet("""
            font-size: 16pt;
        """)
        self.timer.setAlignment(Qt.AlignCenter)

        self.record_widget_layout.addWidget(self.visualizer)

        # Recording Button Layout
        self.recording_buttons_widget = QWidget()
        self.recording_buttons_layout = QHBoxLayout(self.recording_buttons_widget)



        
        self.recording_buttons_layout.addWidget(self.pause)
        self.recording_buttons_layout.addWidget(self.record)
        self.recording_buttons_layout.addWidget(self.play)

        self.record_widget_layout.addWidget(self.timer)
        self.record_widget_layout.addWidget(self.recording_buttons_widget)

        self.record_widget_layout.setAlignment(Qt.AlignCenter)


        self.main_layout.addWidget(self.visualizer)
        self.main_layout.addWidget(self.record_widget)


        # Timer
        self.add_new_frame()
        # set central widget
        self.setCentralWidget(self.central_widget)

    def add_new_frame(self):
        # create new frame and add to scroll area
        new_frame = QFrame()
        new_frame.setFrameShape(QFrame.Box)
        new_frame_layout = QVBoxLayout(new_frame)

        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))

        # QFrame Layout Design 
        new_frame.setMinimumHeight(150)
        new_frame.setMaximumHeight(200)
        new_frame.setGraphicsEffect(shadow)
        new_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        new_frame.setStyleSheet("""
        border-radius: 10px;
        background-color: #b7bbbb;
        """)

        # Sequence No. and X Button
        # Btn Layout
        frame_btn = QPushButton("X")
        frame_btn.setStyleSheet("""
        QPushButton {
            background-color:red;
        }

        QPushButton:hover{
            background-color:#ff3d3d;
            border: 1 solid #e10000;

        }
        QPushButton:pressed {
            background-color:red;
        }
        """)
        frame_btn.clicked.connect(lambda: delete_frame(new_frame))
        new_frame_layout.addWidget(frame_btn,0, Qt.AlignRight)
        
        frame_btn.setFixedSize(QSize(20, 20))
        text_place_holder = QTextEdit()
        # text_place_holder Design
        text_place_holder.setPlaceholderText("Enter your text here...")
        font = QFont()
        font.setPointSize(12)
        text_place_holder.setFont(font)
        text_place_holder.setFontPointSize(12)
        text_place_holder.setMinimumHeight(60)

        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WrapAnywhere)
        text_place_holder.document().setDefaultTextOption(text_option)

        text_place_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        text_place_holder.setStyleSheet("""
        background-color: white;
        """)
  
        new_frame_layout.addWidget(text_place_holder)
        # Timer
        timer = QLabel()
        timer.setText("00:00:00")
        timer.setAlignment(Qt.AlignRight)
        timer.setStyleSheet("""
        margin-right: 10px;
        font-size: 16px;
        color: white;
      
        """)
        new_frame_layout.addWidget(timer)

        self.scroll_area_layout.addWidget(new_frame)
        

        def delete_frame(frame):

            frame.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
