from dataclasses import dataclass, field

@dataclass
class Company():
    code: str
    social_name: str
    short_name: str
    stocks: list = field(default_factory=list)

    def __post_init__(self):
        self.social_name = self.social_name.strip()

    def __str__(self):
        return(f"{self.code} : {self.social_name} : {self.short_name} + {self.stocks}")

    def add_stock(self, stock):
        self.stocks.append(stock)
        

@dataclass
class Stock():
    ticker: str
    bdi: str
    desc_bdi: str
    spec: str

    def __post_init__(self):
        for var in vars(self):
            setattr(self, var, getattr(self, var).strip())
