import sys
from PyQt5 import QtWidgets, uic

# --- THUẬT TOÁN RAIL FENCE ---
class RailFenceLogic:
    @staticmethod
    def encrypt(text, rails):
        if rails <= 1: return text
        fence = [['' for _ in range(len(text))] for _ in range(rails)]
        row, step = 0, 1
        for i, char in enumerate(text):
            fence[row][i] = char
            if row == 0: step = 1
            elif row == rails - 1: step = -1
            row += step
        return "".join("".join(r) for r in fence)

    @staticmethod
    def decrypt(cipher, rails):
        if rails <= 1: return cipher
        fence = [['' for _ in range(len(cipher))] for _ in range(rails)]
        # Đánh dấu vị trí ziczac
        row, step = 0, 1
        for i in range(len(cipher)):
            fence[row][i] = '*'
            if row == 0: step = 1
            elif row == rails - 1: step = -1
            row += step
        # Điền ký tự vào hàng rào
        index = 0
        for r in range(rails):
            for c in range(len(cipher)):
                if fence[r][c] == '*' and index < len(cipher):
                    fence[r][c] = cipher[index]
                    index += 1
        # Đọc theo đường ziczac để lấy văn bản gốc
        result = []
        row, step = 0, 1
        for i in range(len(cipher)):
            result.append(fence[row][i])
            if row == 0: step = 1
            elif row == rails - 1: step = -1
            row += step
        return "".join(result)

# --- GIAO DIỆN CHÍNH ---
class RailFenceApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(RailFenceApp, self).__init__()
        # Load file UI đã thiết kế từ Qt Designer
        uic.loadUi('RailFence.ui', self)
        
        # Kết nối các nút bấm (đảm bảo objectName trong Qt Designer đúng như dưới)
        self.btnEncrypt.clicked.connect(self.process_encrypt)
        self.btnDecrypt.clicked.connect(self.process_decrypt)
        self.btnClear.clicked.connect(self.process_clear)

    def process_encrypt(self):
        text = self.txtInput.toPlainText() # Ô Information
        rails = self.spinRails.value()      # Ô Spin Box Rails
        if text:
            result = RailFenceLogic.encrypt(text, rails)
            self.txtResult.setPlainText(result) # Ô Ciphertext

    def process_decrypt(self):
        cipher = self.txtResult.toPlainText()
        rails = self.spinRails.value()
        if cipher:
            original = RailFenceLogic.decrypt(cipher, rails)
            self.txtInput.setPlainText(original)

    def process_clear(self):
        self.txtInput.clear()
        self.txtResult.clear()
        self.spinRails.setValue(2)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())