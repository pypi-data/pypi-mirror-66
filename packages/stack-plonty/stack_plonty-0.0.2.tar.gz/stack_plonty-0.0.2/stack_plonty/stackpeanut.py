class Peanut:
    peanut = "the plant of the pea family that bears the peanut!"
    def __init__(self, pea_inside=5, pea_type = 'ground_nut'):
        self.pea_inside = pea_inside
        self.pea_type = pea_type
    def cracking(self):
        return [self.pea_type]*self.pea_inside
taste_of_peanut = 'Delicious'