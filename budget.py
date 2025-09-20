import spending_type

class budget:
    def __init__(self, budget_name, monthly_budget):
        self.budget_name = budget_name
        self.monthly_budget = monthly_budget
        self.spending_categories = [spending_type.spending_type("Unallocated Spending", "Unallocated Spending", self.monthly_budget)]
        self.total_spent = 0
        self.total_remaining = self.monthly_budget

    def get_budget_name(self):
        return self.budget_name
    
    def get_monthly_budget(self):
        return self.monthly_budget

    def add_new_spending_category(self, spending_category):
        self.spending_categories.append(spending_category)
        self.spending_categories[0].set_amount(self.spending_categories[0].get_amount() - spending_category.get_amount())

    def get_spending_category(self, category_index):
        return self.spending_categories[category_index]

    def remove_spending_category(self, category_index):
        if category_index == 0:
            print("You cannot remove the unallocated spending category")
            return
        self.total_spent -= self.spending_categories[category_index].get_budget_used()
        self.total_remaining += self.spending_categories[category_index].get_budget_used()
        self.spending_categories[0].set_amount(self.spending_categories[0].get_amount() + self.spending_categories[category_index].get_amount())
        self.spending_categories.pop(category_index)

    def spend_money(self, spending_category, amount):
        spending_category.spend(amount)
        self.total_remaining -= amount
        self.total_spent += amount
