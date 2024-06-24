import socket
from class_status import Status     # classe dos personagens
import deck                         # info das cartas

Finished = False

class Client:
    def __init__(self, host='127.0.0.1', port=50000):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print(f"Conectado ao servidor em {host}:{port}")

    def read_from_socket(self, turn:int):       # Formato: Carta + Dano + countFlags + Flags
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
        
        Finished = deck.process_data(turn, card, damage, flags, Geralt)
        if turn == -1 and card == 7:
            client.write_to_socket(7,0,'')      # manda confirmacao de conexao

    def write_to_socket(self, Card:int, Damage:int, Effects:str):
        if Card == 8:
            print("Você encerrou a conexão (Código: 8)")
        flags = Effects.encode("utf-8")
        count = len(flags)
        message = Card.to_bytes(1,"big") + Damage.to_bytes(1,"big") + count.to_bytes(1,"big") + flags
        self.client_socket.sendall(message)

    def close(self):
        print("\nFim\n")
        self.client_socket.close()


Geralt = Status()                      # cria personagem
geralts_deck = deck.Deck               # cria deck
Geralt.Name = "Geralt"

client = Client(port=50000)
client.read_from_socket(-1)             # espera servidor enviar Pronto


deck.Text_Intro()                       # texto introdutorio
Geralt.PrintStatus()                    # mostra status do personagem

turn = damage = 0
effect = ''
while Geralt.HP > 0 and not Finished:
    if turn%2==0:                               # cliente joga em turnos pares
        deck.show_deck(geralts_deck)            # apresenta o deck

        card = int(input("\nSua jogada: "))
        card = deck.validate_cmd(card, geralts_deck)              # veficar se é uma jogada válida
        
        if card == 8:
            client.write_to_socket(card, damage, effect)    # codigo 8: encerramento forçado da conexao
            break

        damage, effect = deck.get_data(turn, card, Geralt, geralts_deck)
        client.write_to_socket(card, damage, effect)
    else:
        print("Espere a jogada de Vesemir...")
        client.read_from_socket(turn)

    if not Finished:
        Geralt.PrintStatus()                    # mostra status do personagem
    Geralt.NextTurn()
    turn += 1

if Geralt.HP <= 0:
    card = 9                             # codigo 9 para fim de jogo
    client.write_to_socket(card, damage, effect)
    print("Você perdeu a luta.")
    deck.Vesemir_Ganha()


client.close()
