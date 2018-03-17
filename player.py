class Player:
    def __init__(self, n, r, fa=False, is_f=False, s=None):
        assert isinstance(n, str)
        assert isinstance(r, int)
        assert isinstance(fa, bool)
        assert isinstance(is_f, bool)
        assert isinstance(s, int) or s is None

        self.name = n
        self.rating = r

        self.is_free_agent = fa
        self.is_female = is_f

        self.strength = s

    @property
    def get_rating(self):
        rtg = self.rating - int(self.is_female) * 100
        return max(2000, min(2700, rtg))

    @property
    def get_stregth(self):
        if not self.strength == None:
            return self.strength
        else:
            return self.rating
