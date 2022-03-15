
class ScourgeModel:

    def city_encounter(self):
        self.title = "Encounter 1: The City"
        self.map = "https://cms.ccb-destiny.com/wp-content/uploads/sotp_encounter_1.png"
        self.description = "WIP"

    def underground_maze(self):
        self.title = "Encounter 2: Underground Maze"
        self.map = "https://cms.ccb-destiny.com/wp-content/uploads/2019/05/nz8pcS6.png"
        self.description = "WIP"

    def sparrow_race(self):
        self.title = "Encounter 3: Sparrow Race"
        self.description = "WIP"

    def revealing_the_boss(self):
        self.title = "Encounter 4: Baiting the Boss?"
        self.description = "WIP"

    def final_boss(self):
        self.title = "Encounter 5: Final Boss"
        self.description = "WIP"
        self.map ="https://cms.ccb-destiny.com/wp-content/uploads/2019/05/sotp_boss_map.png"
        self.thumbnail = "https://cms.ccb-destiny.com/wp-content/uploads/4A891000-7D90-461B-8E0D-3BE2D50464F1.png"

    def __init__(self, encounter=1):

        self.encounters = {}
        self.encounters[1] = self.city_encounter
        self.encounters[2] = self.underground_maze
        self.encounters[3] = self.sparrow_race
        self.encounters[4] = self.revealing_the_boss
        self.encounters[5] = self.final_boss

        self.name = "Scourge of the Past"
        self.title = None
        self.description = ""
        self.map = None
        self.thumbnail = None
        self.fields = []

        self.encounters[encounter]()
