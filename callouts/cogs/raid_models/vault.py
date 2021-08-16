
############################################################################################################################
class VaultModel:
    
    ####################################################################################################################
    def ruins(self):
        self.title = "The Waking Ruins"
        self.map = "https://i.imgur.com/kJPYx2g.png"
        self.thumbnail = None

        self.description = "**Stand on the plates to form the spire.**\n"
        self.description += "1: Send two players to each plate\n"
        self.description += "2: Step into the ring until the white wall around it is built\n"
        self.description += "3: Defeat Praetorians before they touch the plates\n"
        self.description += "4: Reclaim any Vex sync plates that are lost\n"
        self.description += "5: Hold until the Spire forms and the Vault of Glass opens\n"

        self.fields = [("Kinetic","TBD", True),
                       ("Energy","TBD", True),
                       ("Power","TBD", True),
                       ("Enemies", "Basic Vex\nVoid Shield Praetorian\nCyclops", False),
                       ("Hidden Chest", "After the encounter on the way to Templar.", False),
                       ("Triumphs", "**Break No Plates**: Complete the Waking Ruins encounter while not losing a single sync plate to the Vex.", False),
                       ("Collectibles", "A Couple for the shader", False)]

    ####################################################################################################################
    def wellConflux(self):
        self.title = "Protect the Confluxes"
        self.map = "https://destinyraider.files.wordpress.com/2015/03/vog_maps_templars-well-conflux-3.png"

        self.description = "**Protect the confluxes**\n"
        self.description +="1: Defend Confluxs from Vex. I dunno.\n"

        self.fields = [("Kinetic","TBD", True),
                       ("Energy","TBD", True),
                       ("Power","TBD", True),
                       ("Enemies", "Basic Vex\nOverload Minotaur\nWyvern", False),
                       ("Triumphs", "**TBD**: TBD", False),
                       ("Collectibles", "TBD", False)]

    ####################################################################################################################
    def wellOracles(self):
        self.title = "Destroy the Oracles"
        self.map = "https://i.imgur.com/M1hBUZA.png"
        self.thumbnail = None

        self.description = "**Destroy the Oracles**\n\n"

        self.fields = [("Kinetic","TBD", True),
                       ("Energy","TBD", True),
                       ("Power","TBD", True),
                       ("Enemies", "Basic Vex", False),
                       ("Triumphs", "**TBD**: TBD", False),
                       ("Collectibles", "TBD", False)]

    ####################################################################################################################
    def wellTemplar(self):
        self.title = "Defeat the Templar"
        self.map = None
        self.thumbnail = None

        self.description = "**Defeat the Templar**\n\n"
        
        self.description +="1: Grab the Relic to begin the Templar fight\n"
        self.description +="2: Destroy three Oracles in the correct order\n"
        self.description +="3: Use the Relic’s Super to remove the Templar’s shield\n"
        self.description +="4: Stand in the glowing circle to bloe the Templar's teleport\n"
        self.description +="5: break players out of Detainment\n"
        self.description +="6: Deal damage to the Templar, repeat the steps as necessary\n"


        self.fields = [("Kinetic","TBD", True),
                       ("Energy","TBD", True),
                       ("Power","TBD", True),
                       ("Enemies", "Basic Vex", False),
                       ("Triumphs", "**TBD**: TBD", False),
                       ("Collectibles", "TBD", False)]

    ####################################################################################################################
    def labyrinth(self):
        self.title = "Gorgons’ Labyrinth"
        self.map = "https://destinyraider.files.wordpress.com/2015/01/gorgon-map_normal.png"
        self.description = "Escape the Gorgons' Labrynth\n\n"

        self.fields = [("Kinetic","Any", True),
                       ("Energy","Any", True),
                       ("Power","Any", True),
                       ("Enemies", "Basic Fallen\nBrigs", False),
                       ("Hidden Chest", "Located on the left side early on.", False),
                       ("Collectibles", "1: On the bottom of a thing after the hidden chest\n2: Before going inside on the far right\n3: On top of a red tank before the next encounter.", False)]
        self.fields = []

    ####################################################################################################################
    def jumpingpuzzle(self):
        self.title = "Jumping Puzzle!"

    ####################################################################################################################
    def gatekeeper(self):
        self.title = "Gatekeeper"

    ####################################################################################################################
    def atheon(self):
        self.title = "Boss Time!"
        self.map = "https://pbs.twimg.com/media/E2GeO-8XoAA2mrq?format=jpg&name=medium"

        self.description = "I ran out of time and there are so many images!\n\n"


        self.fields = [("Kinetic","Any", True),
                       ("Energy","Any", True),
                       ("Power","Any", True),
                       ("Enemies", "TBD", False),
                       ("Triumphs", "TBD", False),]

    
    ####################################################################################################################
    def __init__(self, encounter=1):

        self.encounters = {}
        self.encounters[1] = self.ruins
        self.encounters[2] = self.wellConflux
        self.encounters[3] = self.wellOracles
        self.encounters[4] = self.wellTemplar
        self.encounters[5] = self.labyrinth
        self.encounters[6] = self.jumpingpuzzle
        self.encounters[7] = self.gatekeeper
        self.encounters[8] = self.atheon

        self.name = "Vault of Glass"
        self.title = None
        self.description = ""
        self.map = None
        self.thumbnail = None
        self.fields = []

        self.encounters[encounter]()
