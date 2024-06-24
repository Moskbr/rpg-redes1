
class Status:               # Formato da mensagem: CARTA + Dano + FlagsEfeito; tamanho 1 byte cada
    Name = ""
    HP = 100
    ATK = 20
    IGNI = 40
    Q = DoubleDamage = IgniDamage = Oil = 0     # efeitos ativos
    
    # Deck inicial = [1:6]
    def NextTurn(self):
        if self.Oil > 0:    # se efeito do oleo esta ativo, decrementa
            self.Oil -= 1
            if self.Oil <= 0:
                self.ATK -= 5 # efeito do oleo termina
                self.Oil = 0

    def ApplyOil(self):  # 2: Oil -> ATK+5 pelos proximos 2 rounds
        self.Oil = 5        # 5 - round atual - 2 round do adversario = 2 rounds
        self.ATK += 5
    
    def Quen(self):         # 4: Escudo Quen
        self.Q = 1          # imune no proximo ataque adversário
    
    def DrinkPotion(self, potion_name):     # 5/6: Poções -> apenas uma pode ser tomada
        if potion_name == "Sharpness":
            self.DoubleDamage = 1           # dobro de dano no proximo ataque com espada
            self.IgniDamage = 15            # mas incrementa 15 de dano recebido do sinal Igni
        elif potion_name == "Andorinha":
            self.HP += 20                   # Alternativamente, a poção que cura 20 de HP
            if self.HP > 100: self.HP = 100
        else: print("Nome Invalido")
    def PrintStatus(self):
        print("\n\tStatus: "+self.Name+" - HP:"+str(self.HP)+" - Dano Atual:"+str(self.ATK)+" - Efeitos Ativos:", end=' ')
        if self.Oil: print('O', end='')
        if self.Q: print('Q', end='')
        if self.DoubleDamage: print('D', end='')
        if self.IgniDamage: print('I', end='')
        print('\n')
