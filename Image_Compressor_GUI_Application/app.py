import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PIL import Image
import PIL
import os
import time
import sys, os
os.chdir(sys._MEIPASS)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Image Compressor'
        self.left = 10
        self.top = 10
        self.width = 250
        self.height = 360
        self.statusBar().showMessage("Message")
        self.statusBar().setObjectName("status")
        self.image_width = 0
        self.setFixedSize(self.width, self.height)
        self.setObjectName("main_window")
        styleSheet = ''
        with open("design.qss", "r") as f:
            styleSheet = f.read()

        self.setStyleSheet(styleSheet)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        ###---------------- Main Window ------------------
        ## 1 frame work
        self.single_bubble =QFrame(self)
        self.single_bubble.setObjectName("bubble")
        self.single_bubble.move(25,70)
        self.single_bubble.mousePressEvent = self.single_bubble_clicked

        self.single_bubble_heading = QLabel(self.single_bubble)
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.move(59,4)

        self.single_bubble_para = QLabel(self.single_bubble)
        self.single_bubble_para.setObjectName("bubble_para")
        self.single_bubble_para.setText("Click here to compress single image")
        self.single_bubble_para.move(15,30)

        ## 2 frame work
        self.dir_bubble =QFrame(self)
        self.dir_bubble.setObjectName("bubble")
        self.dir_bubble.move(25,190)
        self.dir_bubble.mousePressEvent = self.dir_bubble_clicked

        self.dir_bubble_heading = QLabel(self.dir_bubble)
        self.dir_bubble_heading.setObjectName("bubble_heading")
        self.dir_bubble_heading.setText("Compress Multiple Image")
        self.dir_bubble_heading.move(40,4)

        self.dir_bubble_para = QLabel(self.dir_bubble) 
        self.dir_bubble_para.setObjectName("bubble_para")
        self.dir_bubble_para.setText("Compress multiple images at onces select the folder and get compressed version of the images in another folder")
        self.dir_bubble_para.setWordWrap(True)
        self.dir_bubble_para.move(10,20)



        #-------------- Single Bubble expanded ----------------
        self.single_bubble_expanded =QFrame(self)
        self.single_bubble_expanded.setObjectName("bubble_expanded")
        self.single_bubble_expanded.move(25,70)
        self.single_bubble_expanded.setVisible(False)

        self.back_arrow_s = QLabel(self.single_bubble_expanded)
        self.back_arrow_s.move(5,0)
        self.back_arrow_s.setObjectName("back_arrow")
        self.back_arrow_s.setTextFormat(Qt.RichText)
        self.back_arrow_s.setText("&#8592;")
        self.back_arrow_s.mousePressEvent= self.back_arrow_clicked

        self.single_bubble_heading = QLabel(self.single_bubble_expanded)
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.move(59,4)

        self.select_image_label = QLabel(self.single_bubble_expanded)
        self.select_image_label.setObjectName("bubble_para")
        self.select_image_label.setText("Choose Image")
        self.select_image_label.move(20,30)

        self.image_path = QLineEdit(self.single_bubble_expanded)
        self.image_path.setObjectName("path_text")
        self.image_path.move(35,48)

        self.browse_button = QPushButton(self.single_bubble_expanded)
        self.browse_button.setText("...")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.select_file)
        self.browse_button.move(160,48)

        self.select_image_quality = QLabel(self.single_bubble_expanded)
        self.select_image_quality.setObjectName("bubble_para")
        self.select_image_quality.setText("Choose Quality")
        self.select_image_quality.move(20,80)

        self.quality_path = QLineEdit(self.single_bubble_expanded)
        self.quality_path.setObjectName("quality_path_text")
        self.quality_path.move(35,98)

        self.quality_combo = QComboBox(self.single_bubble_expanded)
        self.quality_combo.addItem("High")
        self.quality_combo.addItem("Medium")
        self.quality_combo.addItem("Low")
        self.quality_combo.setObjectName("quality_combo")
        self.quality_combo.move(128,98)
        self.quality_combo.resize(58,18)
        self.quality_combo.currentIndexChanged.connect(self.quality_current_value)


        self.compress_image = QPushButton(self.single_bubble_expanded)
        self.compress_image.setText("Compess")
        self.compress_image.setObjectName("compress_button")
        self.compress_image.clicked.connect(self.resize_pic)
        self.compress_image.move(70,140)


        #-------------- Single Bubble expanded End ----------------
        
        #-------------- dir Bubble expanded ----------------
        self.dir_bubble_expanded =QFrame(self)
        self.dir_bubble_expanded.setObjectName("bubble_expanded")
        self.dir_bubble_expanded.move(25,70)
        self.dir_bubble_expanded.setVisible(False)

        self.back_arrow_d = QLabel(self.dir_bubble_expanded)
        self.back_arrow_d.move(5,0)
        self.back_arrow_d.setObjectName("back_arrow")
        self.back_arrow_d.setTextFormat(Qt.RichText)
        self.back_arrow_d.setText("&#8592;")
        self.back_arrow_d.mousePressEvent = self.back_arrow_clicked

        self.dir_bubble_heading = QLabel(self.dir_bubble_expanded)
        self.dir_bubble_heading.setObjectName("bubble_heading")
        self.dir_bubble_heading.setText("Compress Multiple Image")
        self.dir_bubble_heading.move(30,4)

        self.select_source_label = QLabel(self.dir_bubble_expanded)
        self.select_source_label.setObjectName("bubble_para")
        self.select_source_label.setText("Choose Source Directory")
        self.select_source_label.move(20,30)

        self.source_path = QLineEdit(self.dir_bubble_expanded)
        self.source_path.setObjectName("path_text")
        self.source_path.move(35,48)

        self.browse_source_button = QPushButton(self.dir_bubble_expanded)
        self.browse_source_button.setText("...")
        self.browse_source_button.setObjectName("browse_button")
        self.browse_source_button.clicked.connect(self.select_folder_source)
        self.browse_source_button.move(160,48)

    
        self.select_dest_label = QLabel(self.dir_bubble_expanded)
        self.select_dest_label.setObjectName("bubble_para")
        self.select_dest_label.setText("Choose Destination Directory")
        self.select_dest_label.move(20,80)

        self.dest_path = QLineEdit(self.dir_bubble_expanded)
        self.dest_path.setObjectName("path_text")
        self.dest_path.move(35,98)

        self.browse_dest_button = QPushButton(self.dir_bubble_expanded)
        self.browse_dest_button.setText("...")
        self.browse_dest_button.setObjectName("browse_button")
        self.browse_dest_button.clicked.connect(self.select_folder_dest)
        self.browse_dest_button.move(160,98)


        self.select_dir_quality = QLabel(self.dir_bubble_expanded)
        self.select_dir_quality.setObjectName("bubble_para")
        self.select_dir_quality.setText("Choose Quality")
        self.select_dir_quality.move(20,130)

        self.quality_dir_path = QLineEdit(self.dir_bubble_expanded)
        self.quality_dir_path.setObjectName("quality_path_text")
        self.quality_dir_path.move(35,148)

        self.quality_dir_combo = QComboBox(self.dir_bubble_expanded)
        self.quality_dir_combo.addItem("High")
        self.quality_dir_combo.addItem("Medium")
        self.quality_dir_combo.addItem("Low")
        self.quality_dir_combo.currentIndexChanged.connect(self.quality_current_value)
        self.quality_dir_combo.setObjectName("quality_combo")
        self.quality_dir_combo.move(128,148)
        self.quality_dir_combo.resize(58,18)

        self.compress_dir = QPushButton(self.dir_bubble_expanded)
        self.compress_dir.setText("Compess")
        self.compress_dir.setObjectName("compress_button")
        self.compress_dir.clicked.connect(self.resize_folder)
        self.compress_dir.move(70,190)
        #-------------- dir Bubble expanded End ----------------
    
        ###---------------- Main Window End --------------------
        self.show()
    
    #----------------------- Functions -----------------------
    
    def single_bubble_clicked(self,event):
        print("single_bubble_clicked")
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.single_bubble_expanded.setVisible(True)
        self.dir_bubble_expanded.setVisible(False)

    def dir_bubble_clicked(self,event):
        print("dir_bubble_clicked")
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.single_bubble_expanded.setVisible(False)
        self.dir_bubble_expanded.setVisible(True)

    def back_arrow_clicked(self,event):
        self.single_bubble.setVisible(True)
        self.dir_bubble.setVisible(True)
        self.single_bubble_expanded.setVisible(False)
        self.dir_bubble_expanded.setVisible(False)
    

    def select_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;JPEG (*.jpeg);;PNG (*.png);;JPG (*.jpg)")
        if fileName:
            print(fileName,_)
            self.image_path.setText(fileName)
            img = Image.open(fileName)
            self.image_width = img.width
            self.quality_path.setText(str(self.image_width))

    def select_folder_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        print(folder)
        self.source_path.setText(folder)

        files = os.listdir(folder)
        #for file in files:
        first_pic = folder + '/' + files[0]
        img = Image.open(first_pic)
        self.image_width = img.width
        self.quality_dir_path.setText(str(self.image_width))
    

    def select_folder_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        print(folder)
        self.dest_path.setText(folder)

    def quality_current_value(self):
        if self.quality_combo.currentText() == "High":
            self.quality_path.setText(str(self.image_width))

        if self.quality_combo.currentText() == "Medium":
            self.quality_path.setText(str(self.image_width//2))

        if self.quality_combo.currentText() == "Low":
            self.quality_path.setText(str(self.image_width//4))

        if self.quality_dir_combo.currentText() == "High":
            self.quality_dir_path.setText(str(self.image_width))

        if self.quality_dir_combo.currentText() == "Medium":
            self.quality_dir_path.setText(str(self.image_width//2))

        if self.quality_dir_combo.currentText() == "Low":
            self.quality_dir_path.setText(str(self.image_width//4))

    def compression_code(self, old_pic, new_pic, mywidth):
        try :
            img = Image.open(old_pic)  
            wpercent = (mywidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((mywidth,hsize), PIL.Image.ANTIALIAS)
            img.save(new_pic) 
        except Exception as e:
            self.statusBar().showMessage("Message : " + str(e))
            

    def resize_pic(self):
        old_pic = self.image_path.text()

        if old_pic == '':
            self.statusBar().showMessage("Message: Please choose an image")
            return

        print(old_pic)
        print(int(self.quality_path.text()))
        directories = self.image_path.text().split('/')
        print(directories)

        new_pic_name, okPressed = QInputDialog.getText(self, "Save image as","Image name:", QLineEdit.Normal, "")
        if okPressed and new_pic_name != '':
            print(new_pic_name)
            if old_pic[-4:] == '.jpg':
                new_pic_name += '.jpg'

            elif  old_pic[-4:] == '.jpeg':
                new_pic_name += '.jpeg'
            
            elif  old_pic[-4:] == '.png':
                new_pic_name += '.png'
            else:
                new_pic_name += '.jpeg'

            new_pic = '/'.join(directories[:-1])+'/'+new_pic_name
            print(new_pic)
        
        self.compression_code(old_pic, new_pic,int(self.quality_path.text()))
        self.statusBar().showMessage("Compress Image Done")
        print("Compress")

    def resize_folder(self):   
        source_directory = self.source_path.text()        
        dest_directory = self.dest_path.text()

        if dest_directory == '' or source_directory == '':
            self.statusBar().showMessage("Message: Please filled Correctly")
            return

        files = os.listdir(source_directory)

        # i = 0
        for file in files:
            # i+=1
            if file[-4:] == '.jpg' or file[-5:] == '.jpeg' or file[-4:] == '.png' or file[-4:] == '.JPG' or file[-5:] == '.JPEG' or file[-4:] == '.PNG':
                print(file)
                old_pic = source_directory + "/" + file
                new_pic = dest_directory + "/" + file
                img = Image.open(old_pic)

                print(old_pic)
                print(new_pic)
                self.image_width = img.width
                self.quality_dir_path.setText(str(self.image_width))
                
                self.compression_code(old_pic,new_pic,self.image_width)

                # total_images = len(files)
                # image_done = i
                # self.statusBar().showMessage("Compress Image Done : "+str(int(image_done/total_images)*100)+"%")
                # QApplication.processEvents()
            else:
                print("ignored "+ file)  
                continue
        self.statusBar().showMessage("Image Compress Completed")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())