import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent,QKeySequence
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,QLineEdit,
                             QMainWindow,  QPushButton, QScrollArea,
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
        self.setFocusPolicy(Qt.StrongFocus)
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
        # self.add_frame_button.clicked.connect(self.add_new_frame)

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


        # Connections
        self.record.clicked.connect(self.rec_button)


        
        self.recording_buttons_layout.addWidget(self.pause)
        self.recording_buttons_layout.addWidget(self.record)
        self.recording_buttons_layout.addWidget(self.play)

        self.record_widget_layout.addWidget(self.timer)
        self.record_widget_layout.addWidget(self.recording_buttons_widget)

        self.record_widget_layout.setAlignment(Qt.AlignCenter)


        self.main_layout.addWidget(self.visualizer)
        self.main_layout.addWidget(self.record_widget)

<<<<<<< HEAD
        
        # New Frome Instance
        
        self.new_frame = newFrame(self.scroll_area_widget)
        self.active_frame = self.new_frame
        self.new_frame.setActiveFrame(self.active_frame)
        
        self.scroll_area_layout.addWidget(self.new_frame)
        
    
=======

        # New Frome Instance
        self.new_frame = newFrame()

        self.scroll_area_layout.addWidget(self.new_frame)
>>>>>>> 998f135f4e824f7d8994998ca6402296ae954b23
    
        # set central widget
        self.setCentralWidget(self.central_widget)
        self.new_frame.text_place_holder.setFocus()

       

    def seperatorSentence(self):
        seperated = " ".join(self.new_frame.text_place_holder.toPlainText().split(".")[1:])
        print(type(seperated))
      
        return seperated

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            
            if len(self.new_frame.text_place_holder.toPlainText().splitlines()) > 1:
                
                for add_frame in range(1,len(self.new_frame.text_place_holder.toPlainText().splitlines())):
                    setFrameText = self.new_frame.text_place_holder.toPlainText().splitlines()[add_frame]
                    
                    # create new frame and add to scroll area
<<<<<<< HEAD
                    newFrame_instance = newFrame(self.scroll_area_widget)
                    newFrame_instance.setActiveFrame(self.active_frame)
=======
                    newFrame_instance = newFrame()
>>>>>>> 998f135f4e824f7d8994998ca6402296ae954b23
                    newFrame_instance.setFrameText(setFrameText)
                    

                    self.scroll_area_layout.addWidget(newFrame_instance)
                    
                    
            self.new_frame.text_place_holder.setText(self.new_frame.text_place_holder.toPlainText().splitlines()[0])  

                
        else:
            super().keyPressEvent(event)
<<<<<<< HEAD
        

    def rec_button(self):
        self.activeFrameSelector()
        pass

        # Dummy Event

    # Loop throught all the Frame 
    def activeFrameSelector(self):
        for i in range(self.scroll_area_layout.count()):

            item = self.scroll_area_layout.itemAt(i)

            active_fave = item.widget()

            if active_fave.isActive == True:

                self.active_frame = active_fave
                
                text = active_fave.text_place_holder.toPlainText()
                print(text)
            # else:
            #     # print("No Active Frame")

    

class newFrame(QFrame):
    def __init__(self, scroll_area):
        super().__init__()

        self.active_frame_selected = None
        self.for_scroll_counter = scroll_area

        self.isActive = False

        self.setFrameShape(QFrame.Box)
        

=======






class newFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.Box)
        
>>>>>>> 998f135f4e824f7d8994998ca6402296ae954b23
        self.new_frame_layout = QVBoxLayout(self)

        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))

    

        # QFrame Layout Design 
        self.setMinimumHeight(150)
        self.setMaximumHeight(200)
        self.setGraphicsEffect(shadow)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("""
<<<<<<< HEAD
        
        QFrame {
            border: none;
            border-radius: 10px;
            background-color: white;
        }
        QFrame:hover {
            border: 1px solid gray;
        }
=======
        border-radius: 10px;
        background-color: #b7bbbb;
>>>>>>> 998f135f4e824f7d8994998ca6402296ae954b23
        """)

        # Btn Layout
        self.frame_btn = QPushButton("X")
        self.frame_btn.setStyleSheet("""
        QPushButton {
            background-color:red;
            border-radius: 10px;
        }

        QPushButton:hover{
            background-color:#ff3d3d;
            border: 1 solid #e10000;

        }
        QPushButton:pressed {
            background-color:red;
        }
        """)
        self.frame_btn.clicked.connect(lambda: delete_frame(self))
        self.new_frame_layout.addWidget(self.frame_btn,0, Qt.AlignRight)
        
        self.frame_btn.setFixedSize(QSize(20, 20))
        self.text_place_holder = QTextEdit()
        self.text_place_holder.setPlaceholderText("Enter your text here...")
        
        # text_place_holder Design
        self.font = QFont()
        self.font.setPointSize(12)
        self.text_place_holder.setFont(self.font)
        self.text_place_holder.setFontPointSize(12)
        self.text_place_holder.setMinimumHeight(60)

        self.text_option = QTextOption()
        self.text_option.setWrapMode(QTextOption.WrapAnywhere)
        self.text_place_holder.document().setDefaultTextOption(self.text_option)

        self.text_place_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.text_place_holder.setStyleSheet("""
<<<<<<< HEAD
        QTextEdit {
            border-radius: 5px;
            background-color: white;
        }
        QTextEdit:hover {
            border: none;
        }
=======
        background-color: white;
>>>>>>> 998f135f4e824f7d8994998ca6402296ae954b23
        """)

        self.new_frame_layout.addWidget(self.text_place_holder)
        # Timer
        self.timer = QLabel()
        self.timer.setText("00:00:00")
        self.timer.setAlignment(Qt.AlignRight)
        self.timer.setStyleSheet("""
<<<<<<< HEAD
        QLabel {
            margin-right: 10px;
            font-size: 16px;
            color:gray;
        }

        QLabel:hover {
            border: none;
        }
        
=======
        margin-right: 10px;
        font-size: 16px;
        color: white;

        """)
        self.new_frame_layout.addWidget(self.timer)

>>>>>>> 998f135f4e824f7d8994998ca6402296ae954b23

        """)
        self.new_frame_layout.addWidget(self.timer)


        def delete_frame(frame):

            frame.deleteLater()

<<<<<<< HEAD
    def setActiveFrame(self,active_frave):
        self.active_frame_selected = active_frave

    def setFrameText(self, setFrameText):

        self.text_place_holder.setText(setFrameText)
    
    # Added onClick Event

    def scroll_area_frame_counter(self, frame):
       for i in range(frame.layout().count()):
        widget = frame.layout().itemAt(i).widget()

        if isinstance(widget, newFrame):
            widget.isActive = False
            widget.setStyleSheet("""
            background-color: white;
            """)
            
            
    def onClick(self, event):
        if event.button() == Qt.LeftButton:
            # loop throught list of frame
            # Create a list of frames
            # This function will produce an error becasue its not finish
            self.scroll_area_frame_counter(self.for_scroll_counter)
        
            self.isActive = True
            self.setStyleSheet("""
            background-color: red;
            """)
            
        super().mousePressEvent(event)

    def mousePressEvent(self, event):
        self.onClick(event)
=======
    def setFrameText(self, setFrameText):

        self.text_place_holder.setText(setFrameText)


>>>>>>> 998f135f4e824f7d8994998ca6402296ae954b23



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
