from player import Character

NPC1 = Character("Greg", 5, 11)
NPC2 = Character("Greg", 10, 22)
NPC3 = Character("Greg", 15, 33)
NPC4 = Character("Greg", 20, 44)
Player = Character("Luba", 2, 2)
enemies = [NPC1, NPC2, NPC3, NPC4]

while(True):
    decision = input("Press 'A' to attack\n")
    NPC = None
    for NPC in enemies:
        if(NPC.alive == True):

            break
    if(decision == 'A'):
        damage = Player.attack()
        NPC.take_damage(damage, Player)
        print("Greg takes -" + str(damage) + " dmg")
        print("Greg hp[" + str(NPC.show_hp()) + "]")
        print("Player xp[" + str(Player.show_xp()) + "]\n")


