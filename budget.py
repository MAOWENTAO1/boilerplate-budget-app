class Category:
    def __init__(self,name):
        self.name = name
        self.ledger = list()
        self.ledger_withdraw_total = 0
    def deposit(self,amount,description = ''):
        self.ledger.append({
        "amount":amount,
        "description":description
        })

    def withdraw(self,amount,description = ''):
        if self.check_funds(amount) == True:
            self.ledger.append({
            "amount": - amount,
            "description":description
            })
            self.ledger_withdraw_total += amount
            return True
        else:
            return False

    def get_balance(self):
        total = 0
        for i in self.ledger:
            total += i['amount']
        return total

    def transfer(self,amount,other):
        if self.check_funds(amount) == True:
            self.ledger.append({
            "amount": - amount,
            "description": "Transfer to {}".format(other.name)
            })
            other.ledger.append({
            "amount": amount,
            "description": "Transfer from {}".format(self.name)
            })
            self.ledger_withdraw_total += amount
            return True
        else:
            return False

    def check_funds(self,amount):
        if amount > self.get_balance():
            return False
        else:
            return True

    def __str__(self):
        lines = '*'*int((30 - len(self.name)) * 0.5) + self.name + '*' * int((30 - len(self.name)) * 0.5)
        for i in self.ledger:
            if type(i['amount']) == int:
                number = str(i['amount'])+'.00'
            else:
                number = str(i['amount'])
            lines += '\n' + (i['description']
            + ' ' * 23)[0:23] + ' '*(7-len(number[0:7])) + number[0:7]
        lines += f"\nTotal: {self.get_balance()}"
        return lines

def create_spend_chart(categories):
    # make a dictionary for percentages of each category
    percentages = {}
    total = sum(i.ledger_withdraw_total for i in categories)
    # calculate the percentages
    for i in categories:
        percentages[i.name] = percentages.get(i.name,0) + i.ledger_withdraw_total/total
    #turn them to the right format like :72.4 → 70, 46 → 40...
    for key,value in percentages.items():
        value = value*100
        value = 10 * (value//10)
        percentages[key] = value
    # the text above the line
    lines = "Percentage spent by category"
    for i in range(100,-1,-10):
        lines += "\n"
        lines += (" "*4+str(i)+"|")[-4:]
        for j in percentages:
            if percentages[j] >= i:
                lines += " o "
            else:
                lines += "   "
        lines += " "
    lines += "\n" + " "*4+"-"*len(percentages)*3+"-\n" #the lines
    # find the max of the lengths of each category's name
    max_len = sorted([len(key) for key in percentages.keys()])[-1]
    # the text blow the line
    for i in range(max_len):
        lines += " "*4
        for j in percentages.keys():
            try:
                lines += " " + j[i] + " "
            except:
                lines += " " * 3
        if i < max_len-1:
            lines += " \n"
        else:
            lines += ' '
    return lines
