import sys


from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QScrollArea,
                             QVBoxLayout, QWidget, QGraphicsDropShadowEffect, 
                             QTextEdit, QSizePolicy)


from PyQt5.QtGui import QColor, QTextOption

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # set window title and size
        self.setWindowTitle("Gwapo Ko")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("Background-color: white;")

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
        self.title.setText('Recording 1')
        self.main_layout.addWidget(self.title)

        # Buttons
        self.buttons_widget = QWidget()
        self.button_layout = QHBoxLayout(self.buttons_widget)

        self.save_btn = QPushButton("save")
        self.import_btn = QPushButton("imoprt")
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
                background-color: #115687;
            }
        """)
        self.save_btn.setFixedSize(QSize(85, 25))

        # import_btn 
        self.import_btn.setStyleSheet("""
            background-color: #4b4b4b; 
            Border: none; 
            border-radius: 12px;
            color: white;
            font-size: 18px;
            padding-bottom: 2px;
        """)

        self.import_btn.setFixedSize(QSize(85, 25))

        # Export btn
        self.export_btn.setStyleSheet("""
            background-color: #4b4b4b; 
            Border: none; 
            border-radius: 12px;
            color: white;
            font-size: 18px;
            padding-bottom: 2px;
        """)

        self.export_btn.setFixedSize(QSize(85, 25))

# ------------------------------------------------------------
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.import_btn)
        self.button_layout.addWidget(self.export_btn)
        self.button_layout.addWidget(self.save_btn)
        
        self.main_layout.addWidget(self.buttons_widget)
        

  
        # create scroll area and add to main layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Scroll Area Layout Designs
        # self.scroll_area.setMinimumHeight(300)
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
        self.add_frame_button = QPushButton("add")

        self.add_frame_button.setStyleSheet("""
            background-color: #1d86d0; 
            Border: none; 
            border-radius: 12px;
            color: white;
            font-size: 18px;
            padding-bottom: 2px;
            
        """)

        self.dummy_label = QLabel(" ") # added empty label for spacing hahah
        self.main_layout.addWidget(self.dummy_label)
        self.add_frame_button.setFixedSize(QSize(85, 25))

        self.add_frame_button.clicked.connect(self.add_new_frame)
        self.main_layout.addWidget(self.add_frame_button)

        # Visulizer Module
        # Recording Widget
        self.visualizer = QFrame()
        self.visualizer_layout = QHBoxLayout(self.visualizer)

        # Dummy Content
        self.label_visualizer = QLabel("Audio Visulizer Module")
        self.visualizer_layout.addWidget(self.label_visualizer)

        self.visualizer.setMinimumHeight(150)
        self.visualizer.setStyleSheet("background-color: gray;")

        self.record_widget = QWidget()
        self.record_widget_layout = QHBoxLayout(self.record_widget)

        self.pause_play_btn = QPushButton("Plat/puase")
        self.restart = QPushButton("Restart")
        self.play = QPushButton("Play")

        self.record_widget_layout.addWidget(self.visualizer)
        self.record_widget_layout.addWidget(self.restart)
        self.record_widget_layout.addWidget(self.pause_play_btn)
        self.record_widget_layout.addWidget(self.play)


        self.main_layout.addWidget(self.visualizer)
        self.main_layout.addWidget(self.record_widget)

        


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
        new_frame.setFixedHeight(100)
        new_frame.setGraphicsEffect(shadow)
        new_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        new_frame.setStyleSheet("""
        border-radius: 10px;
        background-color: #b7bbbb;
        """)


        # Btn Layout

        frame_btn = QPushButton("X")
        frame_btn.setStyleSheet("background-color:red;")
        frame_btn.clicked.connect(lambda: delete_frame(new_frame))
        new_frame_layout.addWidget(frame_btn,0, Qt.AlignRight)
        
        frame_btn.setFixedSize(QSize(20, 20))
        text_place_holder = QTextEdit()
        # text_place_holder Design
        text_place_holder.setPlaceholderText("Enter your text here...")
        text_place_holder.setFontPointSize(10)

        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WrapAnywhere)
        text_place_holder.document().setDefaultTextOption(text_option)

        text_place_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        text_place_holder.setStyleSheet("""
        background-color: white;
        """)
  
        new_frame_layout.addWidget(text_place_holder)

        self.scroll_area_layout.addWidget(new_frame)

        def delete_frame(frame):

            frame.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
