from pydantic import BaseModel


class Quote(BaseModel):
    instrument: str
    ask: float | str
    bid: float | str

    def __str__(self):
        string = f'{self.instrument}\n\nask: {self.ask}\n\nbid: {self.bid}'
        return string


class Order(BaseModel):
    instrument: str
    side_of_deal: str
    price: int
    amount: int

    def __str__(self):
        order_str = ''
        line = '{}: {}\n'
        for attribute_name, attribute_value in self:
            order_str += line.format(attribute_name, attribute_value)
        return order_str
