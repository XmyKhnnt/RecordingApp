import os
import sys
import time
import pyaudio
import pyaudio
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import (QColor, QFont, QIcon, QKeyEvent, QKeySequence,
                         QPixmap, QTextOption)
from PyQt5.QtWidgets import (QApplication, QDialog, QFrame,
                             QGraphicsDropShadowEffect, QHBoxLayout, QLabel,
                             QLineEdit, QMainWindow, QPushButton, QScrollArea,
                             QSizePolicy, QTextEdit, QVBoxLayout, QWidget, QComboBox, QMessageBox, QSpacerItem, QCheckBox)
from pyaudio import PyAudio
from timer import timer_class
from microphone import AudioHandler
from audioEditor import AudioTrimmer


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

        # title Widget
        self.title_string = "Untitle-f"
        self.title = QLabel()
        self.title.setText(self.title_string)
        self.edit_title = QLineEdit(self.title_string)
        self.edit_title.setHidden(True)
        
        self.title.setStyleSheet("""
        QLabel {
            font-size: 18px;
            font-weight: 350;
            letter-spacing: 2px;
        }
        """)
        self.edit_title.setStyleSheet("""
        font-size: 18px;
        font-weight: 350;
        letter-spacing: 2px;
        border: none;
        """)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.edit_title)

        # Title and Button
        self.title_and_button = QWidget()
        self.title_and_button_layout = QHBoxLayout(self.title_and_button)
        self.title_and_button_layout.addWidget(self.title)
        self.title_and_button_layout.addWidget(self.edit_title)
        
        # Editable title click events
        # self.title.mouseMoveEvent = self.start_editing_title

        # Buttons
        self.buttons_widget = QWidget()
        self.button_layout = QHBoxLayout(self.buttons_widget)
        self.title.mousePressEvent = self.start_editing_title
        self.buttons_widget.mousePressEvent = self.start_editing_title
       

        self.save_btn = QPushButton("save")
        # self.import_btn = QPushButton("import")
        # self.export_btn = QPushButton("export")

        # Create Folder For storing recording
        

        # Set Shadow to buttons
        ## Bug for for adding shadow
        
        self.save_btn.setGraphicsEffect(self.shadow)
        # self.import_btn.setGraphicsEffect(self.shadow)
        # self.export_btn.setGraphicsEffect(self.shadow)

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
        self.save_btn.clicked.connect(self.save_and_combine_files)

        self.add_frame_button = QPushButton("separate")

        self.add_frame_button.setFixedSize(QSize(80, 25))
        self.add_frame_button.clicked.connect(self.addFrame)

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
        # Pyaduio Instance
        self.audio_handler =AudioHandler()
        self.input_device = PyAudio()
        self.input_device_count = self.input_device.get_device_count()
        # Input Device List Combo Box
        self.input_device_combo = QComboBox()
        for input_device in range(self.input_device_count):
            device_info = self.input_device.get_device_info_by_index(input_device)
            if device_info["maxInputChannels"] > 0:
                self.input_device_combo.addItem(device_info["name"])

        # word gap Combo
        self.recording_gap_combo = QComboBox()
        self.recording_gap_combo.addItem("0.5")
        self.recording_gap_combo.addItem("0.75")
        self.recording_gap_combo.addItem("1.5")
        self.recording_gap_combo.addItem("2")
        
        # QCSS
        combo_css = '''
        QComboBox {
            height: 25px;
            outline: 0;
            border: none;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            background-color: white;
        }
        QComboBox::down-arrow {
            image: url(drop_down.png);
            width: 30px;
            height: 16px;
        }
'''
        # Design combo Boxes
        combo_box_shadow = QGraphicsDropShadowEffect()
        combo_box_shadow.setBlurRadius(10)
        combo_box_shadow.setXOffset(0)
        combo_box_shadow.setYOffset(0)
        combo_box_shadow.setColor(QColor(0, 0, 0, 30))

        word_box_shadow = QGraphicsDropShadowEffect()
        word_box_shadow.setBlurRadius(10)
        word_box_shadow.setXOffset(0)
        word_box_shadow.setYOffset(0)
        word_box_shadow.setColor(QColor(0, 0, 0, 30))

        self.input_device_combo.setGraphicsEffect(combo_box_shadow)
        
        self.input_device_combo.setStyleSheet(combo_css)
        self.recording_gap_combo.setStyleSheet(combo_css)

        self.recording_gap_combo.setGraphicsEffect(word_box_shadow)

            
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.recording_gap_combo)
        self.button_layout.addWidget(self.input_device_combo)
        self.button_layout.addWidget(self.add_frame_button)
        # self.button_layout.addWidget(self.import_btn)
        # self.button_layout.addWidget(self.export_btn)
        self.button_layout.addWidget(self.save_btn)

        self.title_and_button_layout.addWidget(self.buttons_widget)
        self.main_layout.addWidget(self.title_and_button)
   
        # create scroll area and add to main layout
        self.scroll_area = QScrollArea()
        
        # Scroll area Layout Manager
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(300)
        scroll_barv = self.scroll_area.verticalScrollBar()
        scroll_barv.setStyleSheet("""
        QScrollBar:vertical {width: 10px; height: 15px;}
        """)
      
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
        # self.visualizer.setMinimumHeight(0)

        self.play = QPushButton()
        self.visualizer_layout = QHBoxLayout(self.visualizer)
        self.visualizer_layout.addWidget(self.play)
        self.visualizer.setStyleSheet("""
        background-color: green;
        """)



        """
        Visualizer
        """
        self.pa = pyaudio.PyAudio()
        self.chunk_size = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.stream = self.pa.open(format=self.sample_format,
                                    channels=self.channels,
                                    rate=self.rate,
                                    input=True,
                                    frames_per_buffer=self.chunk_size)
  
        self.waveform_data = None
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(-32768, 32767)
        self.ax.set_xlim(0, self.chunk_size)
        self.line, = self.ax.plot([], [], '-')



        self.visualizer_layout.addWidget(self.canvas)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.stream = self.pa.open(format=self.sample_format,
                                   channels=self.channels,
                                   rate=self.rate,
                                   input=True,
                                   frames_per_buffer=self.chunk_size)
        self.timer.start(50)
        self.record_widget = QWidget()
        self.record_widget_layout = QVBoxLayout(self.record_widget)
        

        # Record Widget Layout Size
        self.record = QPushButton("REC")
        
        self.redo = QPushButton()
        self.next_buton = QPushButton("Next")

        # Record Buttons States
        self.play.setEnabled(False)
        self.redo.setEnabled(False)

       

        self.next_buton.clicked.connect(self.go_to_next_adjacent_frame)
        self.record.clicked.connect(self.start_recording_worker)
        self.play.clicked.connect(self.play_recording_worker)
        self.redo.clicked.connect(self.redo_recording)

        # Buttons Design PLAY/RECORD/RESTART


        self.redo.setStyleSheet("""
        QPushButton {
            Border: none; 
            border-radius: 20px;
            color: white;
            font-size: 18px;
        }

        QPushButton:hover {
            background-color:#a70000;

        }
        QPushButton:pressed {
            background-color:red;

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
        self.redo.setFixedSize(QSize(40, 40))
        self.play.setFixedSize(QSize(45, 45))


        #Set Icons To buttons
        self.redo.setIcon(QIcon("reload.png"))
        self.redo.setIconSize(QSize(41,40))
        self.play.setIcon(QIcon("play_btn.png"))
        self.play.setIconSize(QSize(41,40))

        # Qt Timer
        self.main_timer_label = QLabel("00:00:00")
        self.main_timer_label.setStyleSheet("""
            font-size: 16pt;
        """)
        self.main_timer_label.setAlignment(Qt.AlignCenter)

        self.record_widget_layout.addWidget(self.visualizer)

        # Recording Button Layout
        self.recording_buttons_widget = QWidget()
        self.recording_buttons_layout = QHBoxLayout(self.recording_buttons_widget)


        self.recording_buttons_layout.addWidget(self.redo)
        self.recording_buttons_layout.addWidget(self.record)
        self.recording_buttons_layout.addWidget(self.next_buton)
        # self.recording_buttons_layout.addWidget(self.play)
        # self.record_widget_layout.addWidget(self.next_buton)

        self.record_widget_layout.addWidget(self.main_timer_label)
        self.record_widget_layout.addWidget(self.recording_buttons_widget)

        self.record_widget_layout.setAlignment(Qt.AlignCenter)

        self.visualizer_and_record_spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.visualizer.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.record_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        
        self.main_layout.addWidget(self.visualizer)
       
        self.main_layout.addWidget(self.record_widget)

        # Frame Counter
        # New Frome Instance
        self.frame_count = 0
        self.new_frame = newFrame(self.scroll_area_widget,0, self.frame_counter)
        self.new_frame.folder = self.title_string

        self.active_frame = self.new_frame
        self.new_frame.isActive = True
        self.new_frame.setActiveFrame(self.active_frame)
        
        self.scroll_area_layout.addWidget(self.new_frame)

        # set central widget
        self.setCentralWidget(self.central_widget)
        self.new_frame.text_place_holder.setFocus()



        # Flags 
        self.start_pause = True
        self.playback_start_pause = True
        self.doesFolderExist = True
        self.does_recording_started = False
        self.isTitleCheck = False
        self.isTitleChanged = False
        self.doesMainTimerStarted = False
        self.doesPlaybackStarted = False

        self.device_mic_error = False
        # Message box show again
        self.message_box_popup = False
        #ms to current dit
        self.dir_pop = False
    def update_plot(self):
        data = self.stream.read(self.chunk_size, exception_on_overflow=False)
        data_int = np.frombuffer(data, dtype=np.int16)
        self.line.set_data(np.arange(len(data_int)), data_int)
        self.canvas.draw()
    def save_and_combine_files(self):
        path = self.title_string
        audio_trimmer = AudioTrimmer(path)
        timer_interval = self.recording_gap_combo.currentText()
        audio_trimmer.trim_files(float(timer_interval))
        audio_trimmer.combine_files()
        
        msg_box = QMessageBox()
        msg_box.setText("Task or process is done.")
        msg_box.exec_()

        
            

    def go_to_next_adjacent_frame(self):
        try:
            active_frame = self.activeFrameSelector()
            main_frome_count = self.count_number_of_frame()
            next_frame_count = active_frame.sequence + 1
            if  next_frame_count < main_frome_count:
                active_frame.inActiveSate()

                next_frame = self.frameSelector(next_frame_count)
                next_frame.isActive = True
            
                next_frame_count += 1
                self.active_frame = next_frame
                self.active_frame.selected_state()
        except:

            pass

    def call_frame_timer_start(self):
        ative_frame = self.activeFrameSelector()
        self.frame_timer = timer_class(ative_frame.timer)
        self.frame_timer.startTimer()

    def call_frame_timer_stop(self):
        self.frame_timer.stopRecording()

    def call_main_timer_start(self, label):
        self.main_timer = timer_class(label)
        self.main_timer.startTimer()
        try:
            self.new_frame.paren_timer = self.main_timer
            self.new_frame.frame0_timer = self.frame_timer
        except:

            print("Problema nasabb")
            pass

    
    def start_pause_main_timer(self):
        if self.doesMainTimerStarted == False:
            self.call_main_timer_start(self.main_timer_label)
            print('nag create syag new instance')
        elif self.does_recording_started == True:
            self.main_timer.startTimer()
            print('ang problema naa sa resume')
        else:
            pass



    def DirChecker(self, folder_name):
        if not os.path.exists(folder_name):
            return False
        else:
            return True
        

    def folderCreator(self):
        # Create a Folder For storing the Recording
        self.folder_name = self.title.text()
        if not os.path.exists(self.folder_name) and self.does_recording_started == False:
            os.mkdir(self.folder_name)
            self.does_recording_started = True
        elif os.path.exists(self.folder_name) == True and self.does_recording_started == False:
            self.doesFolderExist = False
            title = "Folder Already Exist"
            message = "Please change the dir name"
            self.displayModal(title, message)
        else:
            pass
           
            

    def displayModal(self, title, message):
        Modal(self,title,message)

    def seperatorSentence(self):
        seperated = " ".join(self.new_frame.text_place_holder.toPlainText().split(".")[1:])
        print(type(seperated))
      
        return seperated

    def keyPressEvent(self, event: QKeyEvent) -> None:
        try:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
              
                if self.frame_count > 1:
                    self.add_frame_button.setEnabled(False)
                else:
                    self.addFrame()
            else:
                super().keyPressEvent(event)
        except:
            pass
            
        # Dummy Event
    def addFrame(self):

        try:
            if len(self.new_frame.text_place_holder.toPlainText().splitlines()) > 1:
                        
                for add_frame in range(1,len(self.new_frame.text_place_holder.toPlainText().splitlines())):
                    setFrameText = self.new_frame.text_place_holder.toPlainText().splitlines()[add_frame]
                    
                    # create new frame and add to scroll area
                    newFrame_instance = newFrame(self.scroll_area_widget, add_frame, self.frame_counter)
                    newFrame_instance.setActiveFrame(self.active_frame)
                    newFrame_instance.setFrameText(setFrameText)
                    newFrame_instance.folder = self.title_string
                    try:
                        newFrame_instance.paren_timer = self.main_timer
                    except:
                        pass
                    self.scroll_area_layout.addWidget(newFrame_instance)
                    print(newFrame_instance.sequence)
                            
            self.new_frame.text_place_holder.setText(self.new_frame.text_place_holder.toPlainText().splitlines()[0])  
        except:
            pass

    # Select Frame
    def recording_name(self):
        self.activeFrameSelector()
        filename = f'frame_{self.active_frame.sequence}'
        return filename

    def frameSelector(self, frame_sequence_no):
        for i in range(self.scroll_area_layout.count()):
            item = self.scroll_area_layout.itemAt(i)
            active_fave = item.widget()
            if active_fave.sequence == frame_sequence_no:
                return active_fave
    def count_number_of_frame(self):
        count = 0
        for _ in range(self.scroll_area_layout.count()):
            count += 1
        print("Total frame count: ", count)
        return count

    def frame_counter(self, i):
        self.frame_count += i
        if self.frame_count > 1:
            self.add_frame_button.setEnabled(False)
        else:
            self.add_frame_button.setEnabled(True)
        return self.frame_count

    # Loop throught all the Frame 
    def activeFrameSelector(self):
        for i in range(self.scroll_area_layout.count()):

            item = self.scroll_area_layout.itemAt(i)
            active_fave = item.widget()
            if active_fave.isActive == True:
                self.active_frame = active_fave
                return self.active_frame

    def start_recording(self):

        file = self.recording_name()
        try:
            self.audio_handler.audio_device_index = self.input_device_combo.currentIndex()
            self.audio_handler.start_recording(self.folder_name,f"{file}.wav")
        except:
            self.device_mic_error = True
            print("yes dri ang error")

        
    def redo_recording(self):
        if self.message_box_popup == False:
            msbox = self.show_message_box()

            if msbox == True:
                self.redo.setEnabled(False)
                self.active_frame.subMainTime()
                self.start_worker.quit()
                self.start_recording_worker()
            else:
                pass

        elif self.message_box_popup == True:
            self.redo.setEnabled(False)
            self.active_frame.subMainTime()
            self.start_worker.quit()
            self.start_recording_worker()
        else:
            pass


    def show_message_box(self):
        # Create a message box
        self.redo_msg_box = QMessageBox()
        self.redo_msg_box.setWindowTitle("Message")
        self.redo_msg_box.setText("Do you wan't to overide the current recoring?")
        
        # Add a "Don't show again" checkbox to the message box
        checkbox = QCheckBox("Don't show this message again",self.redo_msg_box)
        self.redo_msg_box.setCheckBox(checkbox)
        
        # Add buttons to the message box
        self.redo_msg_box.addButton(QMessageBox.Ok)
        self.redo_msg_box.addButton(QMessageBox.Cancel)

        # Show the message box and get the result
        result = self.redo_msg_box.exec_()
        
        # Check if the checkbox was checked and save its state
        if checkbox.isChecked():
            # Save the state to a file or a settings object
            self.message_box_popup = True 
        else:
            self.message_box_popup = False
        
        # Process the result
        if result == QMessageBox.Ok:
            return True
        elif result == QMessageBox.Cancel:
            return False
        


    def play_recording(self):
        file = self.recording_name()
        self.audio_handler.start_playback(f"{self.folder_name}/{file}.wav")
        if self.audio_handler.playing == False:
            self.play.setIcon(QIcon("play_btn.png"))
            self.playback_start_pause = True
            self.play_worker.quit()
            self.redo.setEnabled(True)
            self.record.setEnabled(True)
            print('Recording Stopped')

    

    def play_recording_worker(self):
        try:
            if self.playback_start_pause == True:
                self.play.setIcon(QIcon("pause-btn.png"))
                self.play_worker = Worker(self.play_recording)
                self.play_worker.start()
                self.playback_start_pause = False
                self.redo.setEnabled(False)
                self.record.setEnabled(False)

            elif self.playback_start_pause == False:
                print("Stop")
                self.play.setIcon(QIcon("play_btn.png"))
                self.audio_handler.stop_playback()
                self.play_worker.quit()
                self.playback_start_pause = True
                self.redo.setEnabled(True)
                self.record.setEnabled(True)
        except:
            print("Record Does not exist")

    def stopper(self):
        self.main_timer.stopRecording()
        self.call_frame_timer_stop()
        self.start_worker.quit()

    def start_recording_worker(self):

        self.folderCreator()
        if self.start_pause == True and self.doesFolderExist == True:
            self.call_frame_timer_start()
            self.start_pause_main_timer()
    
            self.doesMainTimerStarted = True
            self.record.setStyleSheet("""
            QPushButton {
                background-color: #b7b7b7; 
                Border: none; 
                border-radius: 22px;
                color: white;
                font-size: 18px;
                padding-bottom: 0;
                }
            QPushButton:hover {
                background-color:#a70000;
            }
            QPushButton:pressed {
                background-color:#b7b7b7;
            }
        """)
            self.record.setText("")
            self.record.setIcon(QIcon("pause-btn.png"))
            self.record.setIconSize(QSize(32, 32))
            self.active_frame.recording_state()
            print(self.start_pause)
            self.start_pause = False
            self.start_worker = Worker(self.start_recording)
            self.start_worker.start()

            # while True:
            #     if self.device_mic_error == True:
            #         self.stopper()
            #         print("Ni Gana ang stoper")
            #         break
            #     elif self.active_frame.time > 60:
            #         break

        elif self.start_pause == False:

            self.main_timer.stopRecording()
            self.call_frame_timer_stop()

            print(self.active_frame.time)
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
            self.record.setIcon(QIcon())
            self.record.setText("REC")
            self.audio_handler.stop_recording()
            self.start_pause = True
            self.start_worker.quit()
            self.play.setEnabled(True)
            self.redo.setEnabled(True)
            self.active_frame.selected_state()
            self.active_frame.time = self.frame_timer.timeElapsed
            print(f' active frame time {self.active_frame.time}')
            print(f' Frame timer elapsed time {self.frame_timer.timeElapsed}')
            self.active_frame.paren_timer = self.main_timer
        else:
            print("Naa ra sa condition and problema")

    def start_editing_title(self, event):
        self.title.setHidden(True)
        self.edit_title.setHidden(False)
        self.edit_title.setFocus(True)
        self.doesFolderExist == True
        # self.edit_title.editingFinished.connect(self.finish_editing_title)
        self.edit_title.focusOutEvent = self.finish_editing_title
    
    def start_editing_title_call(self):
        self.title.setHidden(True)
        self.edit_title.setHidden(False)
        self.edit_title.setFocus(True)
        self.doesFolderExist == True
        # self.edit_title.editingFinished.connect(self.finish_editing_title)
        self.edit_title.focusOutEvent = self.finish_editing_title
    
    def finish_editing_title(self, event):
        self.title.setHidden(False)
        self.edit_title.setHidden(True)
        self.doesFolderExist == True
        self.title_string = self.edit_title.text()
        self.title.setText(self.title_string)
        if self.DirChecker(self.title_string) == True and self.isTitleChanged == False:
            if self.dir_pop == False:
                pop = self.show_message_box_title()
                if pop == False:
                    self.edit_title.focusInEvent = self.finish_editing_title 
                else:
                    try:
                        self.del_files(self.title_string)
                    except:
                        pass
                    
                    
            
        else:
            self.doesFolderExist = True
            self.isTitleCheck = True
            self.isTitleChanged = True
    
    def del_files(self, dir):
        for file in os.scandir(dir):
            print(file)
            os.remove(file)


    def del_items_in_dir(self):
        pass

    def show_message_box_title(self):
        # Create a message box
        self.tile_msg_box = QMessageBox()
        self.tile_msg_box.setWindowTitle("Message")
        self.tile_msg_box.setText("Do you want to use the current dir and delete the content?")
        
        # Add a "Don't show again" checkbox to the message box
        checkbox = QCheckBox("Don't show this message again", self.tile_msg_box)
        self.tile_msg_box.setCheckBox(checkbox)
        
        # Add buttons to the message box
        self.tile_msg_box.addButton(QMessageBox.Ok)
        self.tile_msg_box.addButton(QMessageBox.Cancel)

        # Show the message box and get the result
        result = self.tile_msg_box.exec_()
        
        # Check if the checkbox was checked and save its state
        if checkbox.isChecked():
            # Save the state to a file or a settings object
            self.dir_pop = True 
        else:
            self.dir_pop = False
        
        # Process the result
        if result == QMessageBox.Ok:
            return True
        elif result == QMessageBox.Cancel:
            return False
        
    def closeEvent(self, event):
            # close the modal dialog if it is visible
            try:
                if self.tile_msg_box.isVisible():
                    self.tile_msg_box.close()
            except:
                pass

   
            # call the parent's closeEvent method
            super().closeEvent(event)
        
    
class newFrame(QFrame):
    def __init__(self, scroll_area, count, frame_count, main_timer=0, time=0, frame_timer=0):
        super().__init__()
        self.folder = None
        self.frame0_timer = frame_timer
        self.paren_timer = main_timer
        self.time = time
        self.sequence = count
        self.frame_count = frame_count
        self.frame_count(1)
        self.active_frame_selected = None
        self.for_scroll_counter = scroll_area

        self.isActive = False

        self.setFrameShape(QFrame.Box)
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
        QFrame {
            border: none;
            border-radius: 10px;
            background-color: white;
            
        }
        QFrame:hover {
            border: 1px solid gray;
        }
        """)

        # Btn Layout
        self.frame_btn = QPushButton("clear")
        if self.sequence == 0:
            self.frame_btn.setStyleSheet("""
            QPushButton {
                background-color:blue;
                border-radius: 10px;
                color: white;
            }
            QPushButton:hover{
                background-color:#ff3d3d;
                border: 1 solid #e10000;
            }
            QPushButton:pressed {
                background-color:blue;
            }
            """)
            self.frame_btn.clicked.connect(self.clearText)
        else:

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
        
        self.frame_btn.setFixedSize(QSize(40, 20))
        self.text_place_holder = QTextEdit()
        self.text_place_holder.setPlaceholderText("Enter your text here...")
        textScrollbar = self.text_place_holder.verticalScrollBar()
        textScrollbar.setStyleSheet("""
        QScrollBar:vertical {
            width: 10px;
            height: 10px;
        }
            
        """)
        
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
        QTextEdit {
            border-radius: 5px;
            background-color: white;
        }
        QTextEdit:hover {
            border: none;
        }
        """)

        self.new_frame_layout.addWidget(self.text_place_holder)
        # Timer
        self.timer = QLabel()
        self.timer.setText("00:00:00")
        self.timer.setAlignment(Qt.AlignRight)
        self.timer.setStyleSheet("""
        QLabel {
            margin-right: 10px;
            font-size: 16px;
            color:gray;
        }

        QLabel:hover {
            border: none;
        }
        
        """)
        self.new_frame_layout.addWidget(self.timer)


        def delete_frame(frame):
            self.active_frame_time_reset()
            self.del_recording(self.folder)
            self.subMainTime()
            x = self.frame_count(-1)
            frame.deleteLater()

    def del_recording(self, folder):
        path = f'{folder}/frame_{self.sequence}.wav'
        if os.path.exists(path):
            os.remove(path)
            print("File deleted")


    def recording_state(self):
        inActiveshadow = QGraphicsDropShadowEffect()
        inActiveshadow.setBlurRadius(45)
        inActiveshadow.setXOffset(0)
        inActiveshadow.setYOffset(0)
        inActiveshadow.setColor(QColor(0, 255, 69, 100))
        self.setStyleSheet("""
        QFrame {
            border: none;
            border-radius: 10px;
            background-color: #b3ffc7;
            opacity: 0.5;

        }
        QFrame:hover {
            border: 1px solid #00ff45;;
        }
        """)
        
        self.setGraphicsEffect(inActiveshadow)
    
    def selected_state(self):
        inActiveshadow = QGraphicsDropShadowEffect()
        inActiveshadow.setBlurRadius(45)
        inActiveshadow.setXOffset(0)
        inActiveshadow.setYOffset(0)
        inActiveshadow.setColor(QColor(255, 0, 128, 100))
        self.setStyleSheet("""
        QFrame {
            border: none;
            border-radius: 10px;
            background-color: white;
            
        }
         QFrame:hover {
                border: 1px solid #ff6eb7;
            }
        """)
        self.setGraphicsEffect(inActiveshadow)
    
    def subMainTime(self):
        try:
            self.paren_timer.timeElapsed -= self.time
            self.paren_timer.updateMainTimer()
        except:
            pass

    def active_frame_time_reset(self):
        try:
            self.frame0_timer.timeElapsed = 0
            self.frame0_timer.updateMainTimer()
        except:
            print("Problem with  self.frame0_timer.timeElapsed = 0 ")
            pass

    def clearText(self):
        self.del_recording(self.folder)
        print(f'{self.folder}/frame_{self.sequence}.wav')
        self.text_place_holder.clear()
        try:
            if not self.paren_timer.timeElapsed < self.time :
                self.subMainTime()
            else:
                pass
        except:
            pass
        self.active_frame_time_reset()
        

    def setActiveFrame(self,active_frave):
        self.active_frame_selected = active_frave

    def setFrameText(self, setFrameText):

        self.text_place_holder.setText(setFrameText)

    
    # Added onClick Event
    # Loop throu all the list in the Scroll Area and set isActive status to False
    def scroll_area_frame_counter(self, frame):

        for i in range(frame.layout().count()):
            widget = frame.layout().itemAt(i).widget()
            if isinstance(widget, newFrame):
                inActiveshadow = QGraphicsDropShadowEffect()
                inActiveshadow.setBlurRadius(15)
                inActiveshadow.setXOffset(0)
                inActiveshadow.setYOffset(0)
                inActiveshadow.setColor(QColor(0, 0, 0, 60))
                widget.isActive = False
                widget.setStyleSheet("""
                QFrame {
                    border: none;
                    border-radius: 10px;
                    background-color: white;
                    
                }
                QFrame:hover {
                    border: 1px solid gray;
                }
                """)
                widget.setGraphicsEffect(inActiveshadow)
                
    def inActiveSate(self):
        inActiveshadow = QGraphicsDropShadowEffect()
        inActiveshadow.setBlurRadius(15)
        inActiveshadow.setXOffset(0)
        inActiveshadow.setYOffset(0)
        inActiveshadow.setColor(QColor(0, 0, 0, 60))
        self.isActive = False
        self.setStyleSheet("""
                QFrame {
                    border: none;
                    border-radius: 10px;
                    background-color: white;
                    
                }
                QFrame:hover {
                    border: 1px solid gray;
                }
                """)
        self.setGraphicsEffect(inActiveshadow)
            
    def onClick(self,event):
        active_shadow = QGraphicsDropShadowEffect()
        active_shadow.setBlurRadius(45)
        active_shadow.setXOffset(0)
        active_shadow.setYOffset(0)
        active_shadow.setColor(QColor(255, 0, 128, 100))
        if event.button() == Qt.LeftButton:
            # scroll area frame counter function to revert the frame to previus state
            self.scroll_area_frame_counter(self.for_scroll_counter)

            self.isActive = True
            self.setStyleSheet("""
            QFrame {
                border: none;
                border-radius: 10px;
                background-color: white;
                
            }
            QFrame:hover {
                border: 1px solid #ff6eb7;
            }
            """)
            self.setGraphicsEffect(active_shadow)
 
        super().mousePressEvent(event)

    def mousePressEvent(self, event):
        self.onClick(event)
    
   

class Worker(QThread):
    finished = pyqtSignal()
    def __init__(self, task_func, parent=None):

        super(Worker, self).__init__(parent)
        self.task_func = task_func
    
    def run(self):
        self.task_func()
        self.finished.emit()


        
class Modal(QDialog):

    def __init__(self,parent=None,title="empy modal", message="empty modal"):
        super().__init__(parent)
        self.title = title
        self.message = message
        self.setWindowTitle(self.title)
        self.setModal(True)

        self.layout = QVBoxLayout()
        self.label = QLabel(self.message)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.setMinimumSize(QSize(350, 150))

        self.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
