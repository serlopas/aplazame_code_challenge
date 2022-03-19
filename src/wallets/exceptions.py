class NotEnoughMoneyException(Exception):
    default_detail = 'Not enough money'

    def __init__(
        self,
        detail: str = None
    ):
        if detail is None:
            detail = self.default_detail

        self.detail = detail

    def __str__(self) -> str:
        return self.detail
