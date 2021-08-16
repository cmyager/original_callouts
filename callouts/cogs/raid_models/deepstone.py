
############################################################################################################################
class DeepStoneModel:
    
    ####################################################################################################################
    def locate(self):
        self.title = "Locate the Deep Stone Crypt"
        # self.map = "https://i.imgur.com/4fypSqh.png"
        self.map = "https://i.imgur.com/NxV8Vvl.jpg"

        self.description = "There are 7 heat bubbles scattered along the route to the Deep Stone Crypt.\n"
        self.description += "While outside of a heat bubble you gain stacks of the *Frostbite* debuff.\n"
        self.description += "Being inside a bubble removes the debuff.\n"
        self.description += "**10** stacks of Frostbite kills you.\n"
        self.description += "\nDefeat the squad of Fallen and Brigs in at the last bubble to enter the Crypt."

        self.fields = [("Kinetic","Any", True),
                       ("Energy","Any", True),
                       ("Power","Any", True),
                       ("Enemies", "Basic Fallen\nBrigs", False),
                       ("Hidden Chest", "Located in the cliff next to the last heat bubble.", False),
                       ("Triumphs", "**Not a Scratch**: Bring all Pikes from the starting heat bubble to the final heat bubble.", False),
                       ("Collectibles", "Behind a crate in the facility before entering the second encounter.", False)]

    ####################################################################################################################
    def disable_security(self):
        self.title = "Disable Crypt Security"
        self.map = "https://i.imgur.com/fZJ9BKH.png"

        self.description = "__**Buffs**__\n"
        self.description += "**Operator Buff (Red)**\n"
        self.description += "Shoot/punch buttons that open doors and trigger the damage phase\n"
        self.description += "**Scanner Buff (Yellow)**\n"
        self.description += "See what buttons buttons the operator needs to trigger\n"
        self.description += "See what fuses need to be destroyed\n"
        self.description += "\n**This method will get the triumph if you can one phase the fuses\nNever use the Right/Light terminal**\n"
        self.description += "\n__**Strategy**__\n"
        self.description += "Two Teams of 3 (Left/Dark) (Right/Light)\n\n"
        self.description += "1: Pickup the operator buff in the **Left/Dark** room.\n\n"
        self.description += "2: Clear enemies until the scanner buff is obtained on the left room.\nMake sure to get rid of the servitors\n\n"
        self.description += "3: Scanner looks through the windows into the basement and identifies the 2 left side keypads.\n\n"
        self.description += "4: Operator and Scanner meet at the door in the back.\nScanner move to the right side and Operator goes downstairs.\n\n"
        self.description += "5: Scanner identifies the 2 right side keypads.\n\n"
        self.description += "6: Operator shoots all 4 keypads and puts the operator buff into the downstairs terminal.\n\n"
        self.description += "7: Someone takes the operator buff from the terminal in the **LEFT** room and the Scanner puts their buff in the same terminal.\n\n"
        self.description += "8: The person downstairs picks up the scanner buff and calls out what fuses to shoot.\n"
        self.description += "players upstairs DPS the fuses in the middle of the room till they blow up.\nYou have 60 seconds to destroy as many as possible.\n"
        self.description += "Be careful of exploding shanks\n\n"
        self.description += "9: After Damage the person downstairs puts the scanner buff into the terminal\nThe previous scanner picks it up from the **Left** room terminal and heads back to the left side.\n\n"
        self.description += "10: The person with the operator buff unlocks the doors so the person downstairs can exit before the room purges\n"
        self.description += "\nRepeat as needed."

        self.fields = [("Kinetic","Any", True),
                       ("Energy","Shotgun\n", True),
                       ("Power","Xenophage\nGrenade Launcher\nVoid Sword", True),
                       ("Enemies", "Basic Fallen\nDisruptor Servitors\nOverload Fallen Captains\nExploder Shanks", False),
                       ("Triumphs", "**Resource Contention**: Shut down Crypt security while only using 2 of the 3 augmentation terminals.", False),
                       ("Collectibles", "In the room with the big statue before the next encounter.", False)]


    ####################################################################################################################
    def atraks(self):
        self.title = "Clarity Control (WIP)"
        self.map = "https://i.imgur.com/CvL6lpF.png"

        self.description = "__**Buffs**__\n"
        self.description += "**Operator Buff (Red)**\n"
        self.description += "Shoot buttons that:\n"
        self.description += "* Send launch pods between the two areas\n"
        self.description += "* Opens the airlocks that purge the Atriks debuff\n"
        self.description += "**Scanner Buff (Yellow)**\n"
        self.description += "See what atriks replicant needs to be shot\n"
        self.description += "\n__**Strategy**__\n"

        self.description += "1. Separate into two teams, Space and Ground team.\nAt the start of the encounter two members of Space team will immediately launch up to begin clearing enemies while the third stays down to wait for the operator buff.\n\n"
        self.description += "2. Once the Operator has their buff and is in the Space begin to kill servitors until the Scanner spawns in the Space room.\nOnce the last servitor is killed the mechanic will start so do not finish the last one until the Scanner has their buff.\n\n"
        self.description += "3. The Scanner will be tasked with calling out which copy of Atraks is glowing.\nThe team will need to do as much damage to this copy and the residual cloud until it drops a Replication Debuff.\n\n"
        self.description += "4. Once Space teams’ Atraks copy is destroyed pass the Scanner buff down to the Ground via the terminal so the next team can kill their copy and bring their debuff to space.\n\n"
        self.description += "5. While this is happening the Operator needs to make sure no ones debuff expires by shooting their teammates which will drop and recharge the debuff that a player will need to pick back up.\n\n"
        self.description += "6. Once there are four debuffs in the Space the Operator will need to shoot the four players in an airlock and drop their buffs to be sucked into space. Players will need to run against to pull to ensure they are not vacuumed out.\n\n"
        self.description += "7. Doing this enough times will trigger Atraks-1’s last stand where all players will need to be in space to shoot the glowing copies till enough damage is done to kill the boss.\n\n"

        self.fields = [("Kinetic","Any", True),
                       ("Energy","Shotgun", True),
                       ("Power","Xenophage\nSword", True),
                       ("Enemies", "Basic Fallen\nDisruptor Servitors\nMajor Tracer Shanks", False),
                       ("Triumphs", "**5 Seconds to Paradise**: Defeat Atraks-1 while destroying all Servitors within 5 seconds of each other.", False),]

    ####################################################################################################################
    def jumping_puzzle(self):
        self.title = "Descent"
        self.map = ""
        self.description = "Jumping Puzzle in space. There is some cool dialog from Clovis AI."

        self.fields = [("Kinetic","Any", True),
                       ("Energy","Any", True),
                       ("Power","Any", True),
                       ("Enemies", "Basic Fallen\nBrigs", False),
                       ("Hidden Chest", "Located on the left side early on.", False),
                       ("Collectibles", "1: On the bottom of a thing after the hidden chest\n2: Before going inside on the far right\n3: On top of a red tank before the next encounter.", False)]

    ####################################################################################################################
    def confront_taniks(self):
        self.title = "Prevent Europa’s Destruction"
        self.map = "https://i.imgur.com/1Lb52GU.png"

        self.description = "__**Buffs**__\n"
        self.description += "**Operator Buff (Red)**\n"
        self.description += "Shoot Nuclear Core spawn to release 2 cores\n"
        self.description += "**Scanner Buff (Yellow)**\n"
        self.description += "See what deposit bins are open\n"
        self.description += "**Disruptor Buff (Blue)**\n"
        self.description += "Stun Taniks and allow cores to be deposited\n"
        self.description += "\n__**Strategy**__\n"
        self.description += "Collect Scanner, Operator, and Suppressor buffs from Vandals\n\n"
        self.description += "Scanner checks which bucket accepts Nuclear Cores\n"
        self.description += "Operator shoots keypads to get Nuclear Cores\n"
        self.description += "Suppressor waits under drones\n\n"
        self.description += "Nuclear Cores are collected, swapped to other players as needed\n\n"
        self.description += "Suppressor shoots Taniks while standing under all three drones, then Nuclear Cores are deposited\n\n"
        self.description += "Player with the disabled Augment swaps it at an Augmentation Terminal\n\n"
        self.description += "Process is repeated until center hatch unlocks at which point all players drop down and run\n"

        self.fields = [("Kinetic","Any", True),
                       ("Energy","Any", True),
                       ("Power","Any", True),
                       ("Enemies", "Basic Fallen\nOverload Captains", False),
                       ("Triumphs", "**Short Circuit**: Confront Taniks while depositing all 4 nuclear cores within 10 seconds of each other.", False),]

    ####################################################################################################################
    def taniks_the_abomination(self):
        self.title = "Defeat Taniks: The Abomination (WIP)"
        self.map = "https://i.imgur.com/aHvFbrf.png"

        self.description = "__**Buffs**__\n"
        self.description += "**Operator Buff (Red)**\n"
        self.description += "Break containment field around core runners\n"
        self.description += "**Scanner Buff (Yellow)**\n"
        self.description += "See what deposit bins are open\n"
        self.description += "**Disruptor Buff (Blue)**\n"
        self.description += "Stun Taniks and allow cores to be deposited\n"
        self.description += "\n__**Strategy**__\n"
        self.description += "Split into three teams of two, one team for each corner\n\n"
        self.description += "Acquire the Scanner, Operator, and Suppressor Augments from enemies\n\n"
        self.description += "Scanner calls out which 2 Nuclear Core buckets are active\n\n"
        self.description += "All players shoot 2/4 of Taniks’ wings to drop Nuclear Cores\n\n"
        self.description += "2/4 players grab the Nuclear Cores and carry them to the buckets (swapping with a buddy if Radiation approaches x10)\n\n"
        self.description += "Operator shoots any trapped Nuclear Core carriers (purple force field)\n\n"
        self.description += "Suppressor finds 3 drones to stand under and shoots Taniks from each one (Nuclear Core carriers can now deposit nukes)\n\n"
        self.description += "Repeat until 4 Nuclear Cores are deposited\n\n"
        self.description += "Taniks moves to middle, damage phase begins\n\n"
        self.description += "If all 4 cores were deposited in one round you get an extra damage phase\n\n"
        self.description += "An Augment will be deactivated, use Augmentation Terminal to swap with another player\n\n"
        self.description += "Repeat the steps until the last notch of health\n\n"
        self.description += "Taniks will begin teleporting around the map. Deal damage to him until he’s defeated"

        self.fields = [("Kinetic","Any", True),
                       ("Energy","Divinity\nSlug Shotgun", True),
                       ("Power","Xenophage\nAnarchy", True),
                       ("Enemies", "Basic Fallen", False),
                       ("Triumphs", "**Ready, Set, Go!**: Defeat Taniks, the Abomination while activating pairs of conduit nodes within 5 seconds of each other.", False),]

    ####################################################################################################################
    def __init__(self, encounter=1):

        self.encounters = {}
        self.encounters[1] = self.locate
        self.encounters[2] = self.disable_security
        self.encounters[3] = self.atraks
        self.encounters[4] = self.jumping_puzzle
        self.encounters[5] = self.confront_taniks
        self.encounters[6] = self.taniks_the_abomination

        self.name = "The Deep Stone Crypt"
        self.title = None
        self.description = ""
        self.map = None
        self.thumbnail = None
        self.fields = []

        self.encounters[encounter]()
