import socket
from class_status import Status     # classe dos personagens
import deck                         # info das cartas

Finished = False

class Server:
    def __init__(self, host='127.0.0.1', port=50000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f"Servidor iniciado em {host}:{port}")
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Conexão estabelecida com {self.client_address}")

    def read_from_socket(self, turn):           # Formato: Carta + Dano + countFlags + Flags
        global Finished

        data = self.client_socket.recv(1)
        card = int.from_bytes(data, 'big')

        data = self.client_socket.recv(1)
        damage = int.from_bytes(data, 'big')
        data = self.client_socket.recv(1)
        count = int.from_bytes(data, 'big')
        flags = ''
        if count > 0:
            data = self.client_socket.recv(count)
            flags = data.decode('utf-8')
        
        Finished = deck.process_data(turn, card, damage, flags, Vesemir)

    def write_to_socket(self, Card:int, Damage:int, Effects:str):
        flags = Effects.encode("utf-8")
        count = len(flags)
        message = Card.to_bytes(1,"big") + Damage.to_bytes(1,"big") + count.to_bytes(1,"big") + flags
        self.client_socket.sendall(message)

    def close(self):
        print("\nFim\n")
        self.client_socket.close()
        self.server_socket.close()



Vesemir = Status()                      # cria personagem
vedemirs_deck = deck.Deck               # cria deck
Vesemir.Name = "Vesemir"

server = Server(port=50000)
server.write_to_socket(7,0,'')          # codigo 7: pronto
server.read_from_socket(-1)             # espera "ACK" do cliente


deck.Text_Intro()                        # texto introdutorio
Vesemir.PrintStatus()                    # mostra status do personagem

turn = damage = 0
effect = ''
while Vesemir.HP > 0 and not Finished:
    if turn%2==0:                       # servidor lê em turnos pares
        print("Espere a jogada de Geralt...")
        server.read_from_socket(turn)
    else:
        deck.show_deck(vedemirs_deck)            # apresenta o deck

        card = int(input("\nSua jogada: "))
        card = deck.validate_cmd(card, vedemirs_deck)              # veficar se é uma jogada válida
        
        if card == 8:
            server.write_to_socket(card, damage, effect)    # codigo 8: encerramento forçado da conexao
            break
        damage, effect = deck.get_data(turn, card, Vesemir, vedemirs_deck)
        server.write_to_socket(card, damage, effect)

    if not Finished:
        Vesemir.PrintStatus()
    Vesemir.NextTurn()
    turn += 1

if Vesemir.HP <= 0:
    card = 9                             # codigo para fim de jogo
    server.write_to_socket(card, damage, effect)
    print("Você perdeu a luta.")
    print("\nMas isso significa que Vesemir está treinando seu aprendiz muito bem e que Geralt será um grande bruxo!")
    deck.Geralt_Ganha()

server.close()
