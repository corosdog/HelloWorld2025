class spending_type:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount
        self.budget_used = 0

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_amount(self):
        return self.amount

    def set_name(self, name):
        self.name = name

    def set_category(self, category):
        self.category = category

    def set_amount(self, amount):
        self.amount = amount

    def calculate_budget_percentage(self):
        return (self.amount / self.budget_used) * 100    