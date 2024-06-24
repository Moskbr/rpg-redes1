from class_status import Status

Deck = {
        1: "Ataque",
        2: "Oleo de Humanoide",
        3: "Igni",
        4: "Quen",
        5: "Sharpness",
        6: "Andorinha"
    }


def show_deck(Deck:dict):
    print("Seu deck atual: ")
    for card_num in Deck:
        print("    ", end='')
        info = "|"+ str(Deck.get(card_num)) + ": "+ str(deck_acao.get(Deck.get(card_num))) +"|"
        tam = len(info)
        while tam:
            print('_', end='')
            tam -= 1
        print('\n'+str(card_num) + " - ", end='')
        print(info)
        print("    ", end='')
        tam = len(info)
        while tam:
            print('-', end='')
            tam -= 1
        print('\n')
        

deck_acao = {
    "Ataque": "Você faz um ataque com espada.",
    "Oleo de Humanoide": "Sua espada causará 5 de dano a mais pelos próximos 2 rounds.",
    "Igni": "Você lança o sinal Igni, incendeando o adversário.",
    "Quen": "Você está imune ao proximo ataque do adversário.",
    "Sharpness": "(Poção) Sua espada causará o dobro de dano no próximo ataque.  Mas você fica mais vulnerável a fogo.",
    "Andorinha": "(Poção) Você cura 20 de vida."
}


deck_feedback = {
    "Ataque": " da um ataque com espada.",
    "Oleo de Humanoide": " usou Óleo de Humanóide em sua espada",
    "Igni": " lançou o sinal Igni, te cobrindo de chamas.",
    "Quen": " usou o sinal Quen.",
    "Sharpness": " tomou a poção Sharpness",
    "Andorinha": " tomou a poção Andorinha"
}


def validate_cmd(Card:int, players_deck:dict) -> int:
    valid = False                               # veficar se é uma jogada válida
    while not valid:
        if Card in [1,2,3,4,5,6,8]:             # comandos aceitos
            if Card in players_deck.keys() or Card == 8:       # cartas restantes ou código 8
                valid = True
            else:
                print("Essa carta ja foi consumida")
                Card = int(input("\nSua jogada: "))

        else:
            print("Jogada inválida")
            Card = int(input("\nSua jogada: "))
    
    return Card


def get_data(turn:int, card:int, Player:Status, players_deck:dict):
    damage = 0
    effect = ''
    match card:
        case 1:
            damage = Player.ATK
            if Player.Oil != 0:         # verifica efeito Oil ativo
                effect += 'O'
            if Player.DoubleDamage != 0:# verifica efeito DD ativo
                effect += 'D'
                damage = damage*2
                Player.DoubleDamage = 0
            print("turno "+str(turn+1)+": "+deck_acao.get("Ataque")+" Dano Causado: "+str(damage)+' '+effect)
        case 2:
            Player.ApplyOil()
            players_deck.pop(2)
            print("turno "+str(turn+1)+": "+deck_acao.get("Oleo de Humanoide"))
        case 3:
            damage = Player.IGNI
            players_deck.pop(3)
            print("turno "+str(turn+1)+": "+deck_acao.get("Igni"))
        case 4:
            Player.Quen()
            players_deck.pop(4)
            print("turno "+str(turn+1)+": "+deck_acao.get("Quen"))
        case 5:
            Player.DrinkPotion("Sharpness")
            players_deck.pop(5)
            players_deck.pop(6)
            print("turno "+str(turn+1)+": "+deck_acao.get("Sharpness"))
        case 6:
            Player.DrinkPotion("Andorinha")
            players_deck.pop(5)
            players_deck.pop(6)
            print("turno "+str(turn+1)+": "+deck_acao.get("Andorinha"))
        case _:
            print("Carta inválida ou inexistente. Verifique se já foi utilizada.")
    
    return damage, effect


def process_data(turn, Card, Damage, Flags, Player:Status):
    opponent = ""
    if Player.Name == "Geralt": opponent = "Vesemir"
    else: opponent = "Geralt"

    Finished = False
    match Card:
        case 1:
            print("turno "+str(turn+1)+": " + opponent + str(deck_feedback.get("Ataque"))+" Dano Sofrido: "+str(Damage)+" Efeitos: "+Flags)
            if Player.Q > 0:
                Damage = 0      # imune
                Player.Q = 0    # desliga flag
                print("Mas seu Quen absorve todo o dano sofrido")
            Player.HP -= Damage
        case 2:
            print("turno "+str(turn+1)+": " + opponent + str(deck_feedback.get("Oleo de Humanoide")))
        case 3:
            print("turno "+str(turn+1)+": " + opponent + str(deck_feedback.get("Igni"))+" Dano Sofrido: "+str(Damage)+" Efeitos: "+Flags)
            if Player.IgniDamage > 0:
                Damage += 15            # dano = 25(igni) + 15
                Player.IgniDamage = 0
                print("Pelo efeito colateral da poção Sharpness, você tomou mais 15 de dano de fogo")
            if Player.Q > 0:
                Damage = 0      # imune
                Player.Q = 0    # desliga flag
                print("Mas seu Quen absorve todo o dano sofrido")
            Player.HP -= Damage
        case 4:
            print("turno "+str(turn+1)+": " + opponent + str(deck_feedback.get("Quen")))
        case 5:
            print("turno "+str(turn+1)+": " + opponent + str(deck_feedback.get("Sharpness")))
        case 6:
            print("turno "+str(turn+1)+": " + opponent + str(deck_feedback.get("Andorinha")))
        case 7:
            print("Pronto")
        case 8:                           # se cliente encerrar conexao forçadamente
            print("Conexão encerrada pelo destinatário (Código: 8)")
            Finished = True
        case 9:
            print("Você ganhou a luta!")
            if Player.Name == "Geralt":
                Geralt_Ganha()
            else:
                Vesemir_Ganha()
            Finished = True
        case _: print("Error: "+str(Card))
    return Finished


def Geralt_Ganha():
    print("\nGeralt levanta Vesemir do chão com um sorriso, dizendo:")
    print("- Está ficando lento. Será a sua idade?")
    print("Vesemir responde:")
    print("- Você que esta mais rápido rapaz. Vamos eu pago as cervejas.\n")


def Vesemir_Ganha():
    print("\nVesemir ajuda Geralt a se levantar do chão dizendo:")
    print("- Ainda precisa treinar muito meu rapaz.")


def Text_Intro():
    print("\n----------------- THE WITCHER: O TREINAMENTO DE GERALT ------------------\n")
    print("Geralt de Rívia cesceu na fortaleza de Kaern Mohern sendo treinado para se tornar um bruxo, pelo seu")
    print("mestre Vesemir. Dentre as outras crianças, Geralt sempre foi o mais promissor, se saía melhor nos")
    print("diversos treinamentos, seja combate, herbalismo, estudo do bestiário, e outros. Essa aptidão o")
    print("tornou mais próximo de Vesemir, que adorava sua companhia. Quando jovem, Geralt ainda treinava com")
    print("seu mestre, mas agora com algumas técnicas mais avançadas, dignas de um bruxo experiente, como o uso de")
    print("poções e óleos na espada, e os sinais (poderes especiais de bruxo).")
    print('\n')
    print("Esse pequeno \"RPG de texto\" se passa em um dos treinamentos de combate avançado de Geralt.")
    print("O Servidor controla as ações de Vesemir e o Cliente, as de Geralt. O jogo é no estilo RPG de cartas:")
    print("em cada turno os jogadores devem digitar o número da carta presente em seu Deck para fazer uma jogada.")
    print("Ambos recebem o mesmo Deck.")
    print("\nIMPORTANTE:")
    print("- a carta ATAQUE não é consumível, poranto poderá ser jogada várias vezes. Todas as outras são consumíveis.")
    print("- Devido ao nível máximo de Toxicidade que os bruxos podem consumir, Geralt só pode tomar uma poção")
    print("pois como ainda é jovem e inexperiente, ele tem um nível baixo de toxicidade máxima. Vesemir, para")
    print("garantir uma luta justa, tambem só tomará uma. Portanto: ao tomar uma poção, as duas serão consumidas.")
    print("\n----------------- INICIO DO TREINAMENTO -----------------\n")
    print("Ambos frente a frente dentro do pátio da fortaleza. Vesemir diz:")
    print("- Pode começar meu rapaz\n")


