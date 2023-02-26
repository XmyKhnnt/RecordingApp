from PyQt5.QtCore import QTimer
class timer_class(QTimer):
    def __init__(self, label):
        super().__init__()

        self.timer_label = label
        self.timeout.connect(self.updateTimer)
        self.timeElapsed = 0

    def startTimer(self) -> int:
        print("timer is runnning")
        self.start(100)


    def stopRecording(self):
        self.stop()
    
    def updateTimer(self):
        self.timeElapsed += 1
        time = '{:02d}:{:02d}:{:02d}'.format(self.timeElapsed // 3600,
                                              (self.timeElapsed // 60) % 60,
                                              self.timeElapsed % 60)
        self.timer_label.setText(time)      
    def updateMainTimer(self):
        time = '{:02d}:{:02d}:{:02d}'.format(self.timeElapsed // 3600,
                                        (self.timeElapsed // 60) % 60,
                                        self.timeElapsed % 60)
        self.timer_label.setText(time)