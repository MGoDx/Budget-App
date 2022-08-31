class Category:
    
    def __init__(self,name):
        self.name = name
        self.ledger = list()
        self.total = float(0)

    # Represent a class’s objects as a string
    def __repr__(self):
        head = self.name.center(30, "*") + "\n"
        display = ""
        for i in self.ledger:
            # format description and amount
            lineDescription = "{:<23}".format(i["description"])
            lineAmount = "{:>7.2f}".format(i["amount"])
            # Truncate ledger description and amount to 23 and 7 characters respectively
            display += "{}{}\n".format(lineDescription[:23], lineAmount[:7])
        total = "Total: {:.2f}".format(self.total)
        return head + display + total
    
    def deposit(self, qtd, description=""):
        self.ledger.append({
            "amount" : qtd,
            "description" : description
        })
        self.total += qtd

    def withdraw(self, qtd, description=""):
        if self.total - qtd >= 0:
            self.ledger.append({
            "amount" : -qtd,
            "description" : description
            })
            self.total -= qtd
            return True
        else:
            return False
            
    def get_balance(self):
        return self.total

    def transfer(self, qtd, item):
        # Checking if can transfer
        transferable = self.check_funds(qtd)
        
        if transferable:
            self.withdraw(qtd, f"Transfer to {item.name}")
            item.deposit(qtd, f"Transfer from {self.name}")
        
        return transferable

    def check_funds(self, qtd):
        if self.total >= qtd:
            return True
        else:
            return False


def create_spend_chart(categories):
    
    spentAmount = list()
    
    # Geting the total spent in each category:
    for cat in categories:
        spentTotal = 0
        for item in cat.ledger:
            if item["amount"] < 0:
                spentTotal += abs(item["amount"])
        spentAmount.append(round(spentTotal, 2))

    # Calculating the percentage rounded down to the nearest 10
    total = round(sum(spentAmount), 2)
    spentPercentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spentAmount))

    head = "Percentage spent by category\n"

    chart = ""
    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + '|'
        for percentage in spentPercentage:
            if percentage >= i:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (head + chart + footer).rstrip("\n")