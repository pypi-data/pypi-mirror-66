class Interest:

    def compound(self, value, interest, periods):
        if interest > 1:
            compound_factor = 1 + interest / 100
        else:
            compound_factor = 1 + interest
        return value * compound_factor**periods
