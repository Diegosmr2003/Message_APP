class ChatApp:
    def __init__(self):
        self.nombre = ""
        self.nickname = ""
        self.grupos = []
        self.modo_oscuro = True 

        

    def set_usuario(self, nombre, nickname):
        self.nombre = nombre
        self.nickname = nickname
