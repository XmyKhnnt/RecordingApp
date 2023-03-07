from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor



save_button_shadow = QGraphicsDropShadowEffect()
save_button_shadow.setBlurRadius(10)
save_button_shadow.setXOffset(0)
save_button_shadow.setYOffset(0)
save_button_shadow.setColor(QColor(0, 0, 0, 40))

separate_button_shadow = QGraphicsDropShadowEffect()
separate_button_shadow.setBlurRadius(10)
separate_button_shadow.setXOffset(0)
separate_button_shadow.setYOffset(0)
separate_button_shadow.setColor(QColor(0, 0, 0, 40))


add_button_shadow = QGraphicsDropShadowEffect()
add_button_shadow.setBlurRadius(10)
add_button_shadow.setXOffset(0)
add_button_shadow.setYOffset(0)
add_button_shadow.setColor(QColor(0, 0, 0, 40))
