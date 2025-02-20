import random

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100

ROWS = 3
COLS = 3

SYMBOL_COUNT = {
    "A": 2, 
    "B": 4,
    "C": 6,
    "D": 8,
}

SYMBOL_VALUES = {
    "A": 10,
    "B": 5,
    "C": 3,
    "D": 2,
}

def prompt_deposit():
    """
    Prompts the user to enter the amount they want to deposit.
    """
    
    while True:
        deposit = input("Enter the amount you want to deposit: $")
    
        if not deposit.isdigit():
            print("Please enter a number.")
            continue
        
        deposit = int(deposit)
            
        if deposit <= 0:
            print("Please enter a positive number.")
            continue
        
        return deposit
        
        
def prompt_lines():
    """
    Prompts the user to enter the number of lines they want to bet on.
    """
    
    while True:
        lines = input(f"Enter the number of lines you want to bet on (1-{MAX_LINES}): ")
    
        if not lines.isdigit():
            print("Please enter a number.")
            continue
        
        lines = int(lines)
            
        if not 1 <= lines <= MAX_LINES:
            print("Please enter a positive number.")
            continue
            
        return lines
    
def prompt_bet(balance, lines):
    """
    Prompts the user to enter the they would like to bet per line.
    """
    
    max_bet = min(MAX_BET, balance / lines)
    max_bet = int(max_bet)
        
    while True:
        bet = input(f"Enter the amount you would like to bet of lines you want to bet on (${MIN_BET}-${max_bet}): $")
    
        if not bet.isdigit():
            print("Please enter a number.")
            continue
        
        bet = int(bet)
            
        if not MIN_BET <= bet <= max_bet:
            print(f"Please enter an amount between ${MIN_BET} and ${max_bet}.")
            continue
        
        total_bet = lines * bet
        print(f"You are betting ${bet} on {lines} lines. Total bet: ${total_bet}")
            
        return bet
    
def generate_spinner(symbols):
    """
    Generates a spinner for the slot machine.
    """
    
    new_spinner = []
    
    for symbol, count in symbols.items():
        new_spinner.extend([symbol] * count)
    
    random.shuffle(new_spinner)
        
    return new_spinner
    
def get_slot_machine_spin(rows, cols, spinner):
    """
    Returns a random slot machine spin.
    """
        
    spin = [[], [], []]
    for col in range(cols):
        index = random.randint(0, len(spinner)-1)
        #print(f"Column[{col}] Spin: {index}")
        spin[0].append(spinner[index-1 if index > 0 else len(spinner)-1])
        spin[1].append(spinner[index])
        spin[2].append(spinner[index+1 if index < len(spinner)-1 else 0])
          
    return spin

def calculate_winnings(spin, bet, lines):
    """
    Calculates the user's winnings based on the slot machine spin.
    """
    
    winnings = 0
    
    for line in range(lines):
        if spin[line][0] == spin[line][1] == spin[line][2]:
            winnings += SYMBOL_VALUES[spin[line][0]] * bet * lines
            
    print(f"Winnings: ${winnings}")
    return winnings

def game(balance, spinner):
    
    # Find out how many lines the user would like to bet on
    lines = prompt_lines()
    
    # Find out the user's bet for each line
    bet = prompt_bet(balance, lines)
    
    # Print out the user's balance, number of lines, and bet
    total_bet = lines * bet
    balance -= total_bet
    print (f'Balance: ${balance}, Lines: {lines}, Bet: ${bet}, Total Bet: ${total_bet}')
    
    # Spin the slot machine
    input("Press Enter to spin the slot machine.")
    spin_again = True
    while spin_again:
        spin = get_slot_machine_spin(ROWS, COLS, spinner)
    
        # Print out the slot machine spin
        for row_idx, row in enumerate(spin):
            print(' | '.join(row), end="")
            if lines > row_idx:
                print(" <<< ")
            else:
                print()
            
        # Calculate the user's winnings
        balance += calculate_winnings(spin, bet, lines)
        print(f"Balance: ${balance}")
        if balance <= 0:
            print("You are out of money.")
            return True, balance
            
        action = input("What would you like to do? \n\tPress ENTER to spin again\n\t'c' = (C)hange Bet\n\t'e' = (E)xit: ")
        match action.lower():
            case 'c': return False, balance
            case 'e': return True, balance
        
        # Pay for spin
        if balance >= total_bet:
            balance -= total_bet
            print (f'Balance: ${balance}, Lines: {lines}, Bet: ${bet}, Total Bet: ${total_bet}')
        else:
            print(f"Insufficient funds. Balance: ${balance}")
            return False, balance
        
        
            
def main():
    
    # Generate the spinner
    spinner = generate_spinner(SYMBOL_COUNT)
    #print(f"Spinner: {spinner}")
    
    # Find out how much money the user would like to deposit
    balance = prompt_deposit()
    
    exit = False
    while not exit:
        exit, balance = game(balance, spinner)
    
    
if __name__ == "__main__":
    main()