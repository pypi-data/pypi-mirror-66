from PyQt5.QtWidgets import QScrollBar,QSlider
import takagiabm.visualize.takagiwidgets.colorutils as colorUtils
class TakScrollBar(QSlider):
    def __init__(self,*args):
        super().__init__(*args)

        self.setStyleSheet(
'''
QScrollBar:horizontal {
	border:0.5px %s;
	background:%s;
	height:15px;
	margin:0px 20px 0px 20px;
}'''%(colorUtils.globalBorderColor,colorUtils.globalBackgroundColor)+'''

QScrollBar::add-line:horizontal {
	/* 外边框 */
	border:2px %s;
		
	/* 宽度 */
	width:20px;
	
	/* 位置 */
	subcontrol-position:right;
	
	/* 画线区域选择 */
	subcontrol-origin:margin;
}'''%(colorUtils.globalBorderColor)+'''
QScrollBar::handle:horizontal {
	/* 颜色 */
	background:white;
	/*两边形状椭圆形*/
	 border-radius:4px;  
	
	/* 长度 */
	min-width:20px;
	max-width:30px;
}

QScrollBar::sub-line:horizontal {    /*add-line的意思就是向右的那个箭头，sub-line同。*/ 
	background:%s;
	width:20px;
	subcontrol-position:left;
	subcontrol-origin:margin;
}'''%(colorUtils.globalBackgroundColor)+'''
QScrollBar::left-arrow:horizontal,QScrollBar::right-arrow:horizontal {
	width:3px;
	height:3px;
	background:white;
}

/* 滑块左边 */
QScrollBar::add-page:horizontal,QScrollBar {
	background:%s;
	  
}

/* 滑块右边 */
QScrollBar::sub-page:horizontal {
	background:%s;
	  
}
'''%(colorUtils.globalHoverBackgroundColor,colorUtils.globalHoverBackgroundColor)
        )