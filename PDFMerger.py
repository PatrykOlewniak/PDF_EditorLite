"""
    PDFMerger can merge two PDF Files, extract selected pages 
    from source PDF file and create new one
    with the choosen pages.
"""

from PyPDF2 import PdfFileWriter, PdfFileReader
import sys
import os
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QDialog, QLabel, QLineEdit, \
    QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QFont


class PDFEditorLite(QDialog):
    """
    Main class of Editor, inherits from QDialog class
    Use Qt Designer Layout as GUI
    """
    def __init__ (self, parent=None):
        super(PDFEditorLite, self).__init__(parent)
        self.QTLayout()

    def QTLayout (self):
        """
        Basic layout made with QT Designer
         
        """
        self.setWindowTitle("PDF Editor")
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)  # removes the"?"
        self.layout = QVBoxLayout(self)
        self.labelH1 = QLabel("PDF Creation")
        font = QFont()
        font.setPointSize(9)
        self.labelH1.setFont(font)
        self.pathButton = QPushButton("Source PDF file")
        self.pathButton.clicked.connect(self.setSourcePath)

        self.layout.addWidget(self.pathButton)
        self.labelPagesCount = QLabel()
        self.labelPagesCount.setText("{Empty}")
        self.labelN = QLabel("\n")
        self.labelN1 = QLabel("\n")
        self.layout.addWidget(self.labelN)
        self.labelSourceFile1 = QLabel()
        self.labelSourceFile1.setText("Source file path:")
        self.layout.addWidget(self.labelSourceFile1)
        self.layout.addWidget(self.labelSourceFile1)
        self.layout.addWidget(self.labelPagesCount)
        self.labelCountPages1 = QLabel("0")
        self.layout.addWidget(self.labelPagesCount)
        self.layout.addWidget(self.labelCountPages1)
        self.layout.addWidget(self.labelN)
        self.destinationButton = QPushButton("Destination path:")
        self.layout.addWidget(self.destinationButton)
        self.destinationButton.clicked.connect(self.destinationFileSave)
        self.lavbelSave = QLabel("Selec estination path:")
        self.layout.addWidget(self.lavbelSave)
        self.labelSave2 = QLabel("{Empty}")
        self.layout.addWidget(self.labelSave2)
        self.layout.addWidget(self.labelN1)
        self.labelStr = QLabel("Input selected pages \n[separated with comma]")
        self.layout.addWidget(self.labelStr)
        self.lineEditCountOfPages = QLineEdit()
        self.layout.addWidget(self.lineEditCountOfPages)
        self.saveButton2 = QPushButton("SAVE FILE")
        self.layout.addWidget(self.saveButton2)
        self.saveButton2.clicked.connect(self.saveOutputFile)

        self.mergeButton = QPushButton("MERGE FILES")
        self.mergeButton.clicked.connect(self.mergeTwoFiles)
        self.breakLabel = QLabel()
        self.mergeTextLabel = QLabel("Button below merges two PDF files")
        self.layout.addWidget(self.breakLabel)
        self.layout.addWidget(self.breakLabel)
        self.layout.addWidget(self.mergeTextLabel)
        self.layout.addWidget(self.mergeButton)

    def mergeTwoFiles (self):
        firstPDF = QFileDialog.getOpenFileName(self, 'Choose the first PDF file', "*.pdf")
        secondPDF = QFileDialog.getOpenFileName(self, 'Choose the second PDF file ', "*.pdf")
        QMessageBox.information(self, "Select destination place",
                                "Input name of new file and path")
        merged = QFileDialog.getSaveFileName(self, 'Destination file', "*.pdf")

        if os.path.exists(firstPDF) and os.path.exists(secondPDF):
            output = PdfFileWriter()
            firstPDF = PdfFileReader(open(firstPDF, "rb"))
            for page in range(firstPDF.getNumPages()):
                output.addPage(firstPDF.getPage(page))

            secondPDF = PdfFileReader(open(secondPDF, "rb"))
            for page in range(secondPDF.getNumPages()):
                output.addPage(secondPDF.getPage(page))

            outputStream = open(merged, "wb")
            output.write(outputStream)
            outputStream.close()

    def setSourcePath (self):
        self.sourcePath = QFileDialog.getOpenFileName(self, 'Choose the source PDF file to add', "*.pdf")
        self.labelPagesCount.setText(self.sourcePath)
        input1 = PdfFileReader(file(self.labelPagesCount.text(), "rb"))
        self.labelCountPages1.setText("Source file page count: %s " % input1.getNumPages())

    def destinationFileSave (self):
        self.destinationPath = QFileDialog.getSaveFileName(self, 'Destination', "*.pdf")
        self.labelSave2.setText(self.destinationPath)

    def saveOutputFile (self):
        try:
            list1 = str(self.lineEditCountOfPages.text())
            list1 = map(int, list1.split(','))

            if str(self.labelPagesCount.text()) != "{Empty}":
                input1 = PdfFileReader(file(self.labelPagesCount.text(), "rb"))
                output = PdfFileWriter()

                self.labelCountPages1.setText("New file pages amount: %s " % input1.getNumPages())

                for b in list1:
                    if b <= int(input1.getNumPages()):
                        output.addPage(input1.getPage(b - 1))
                    else:
                        QMessageBox.information(self, "Error!", "Wrong page number")

                if str(self.labelSave2.text()) != "{Empty}":
                    outputStream = file(self.labelSave2.text(), "wb")
                    output.write(outputStream)
                    outputStream.close()
                else:
                    QMessageBox.information(self, "Error!", "Choose the save path")
                    outputStream.close()

            else:
                QMessageBox.information(self, "Error", "Choose the right source")



        except ValueError:
            QMessageBox.information(self, "Error", "Wrong pages")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = PDFEditorLite()
    dialog.exec_()
    sys.exit(app.exec_())
