"""
Slot Machine
"""

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
    "A": 30,
    "B": 15,
    "C": 9,
    "D": 4,
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
        bet = input(
            f"Enter the amount you would like to bet per line (${MIN_BET}-${max_bet}): $"
        )

        if not bet.isdigit():
            print("Please enter a number.")
            continue

        bet = int(bet)

        if not MIN_BET <= bet <= max_bet:
            print(f"Please enter an amount between ${MIN_BET} and ${max_bet}.")
            continue

        total_bet = lines * bet
        print(f"\nYou are betting ${bet} on {lines} lines. Total bet: ${total_bet}")

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


def get_slot_machine_spin(cols, spinner):
    """
    Returns a random slot machine spin.
    """

    spin = [[], [], []]
    for _ in range(cols):
        index = random.randint(0, len(spinner) - 1)
        # print(f"Column[{col}] Spin: {index}")
        spin[0].append(spinner[index - 1 if index > 0 else len(spinner) - 1])
        spin[1].append(spinner[index])
        spin[2].append(spinner[index + 1 if index < len(spinner) - 1 else 0])

    return spin


def calculate_winnings(spin, bet, lines):
    """
    Calculates the user's winnings based on the slot machine spin.
    """

    winnings = 0
    winning_lines = []

    for line in range(lines):
        if spin[line][0] == spin[line][1] == spin[line][2]:
            winnings += SYMBOL_VALUES[spin[line][0]] * bet
            winning_lines.append(line)

    print(f"Winnings: ${winnings}")
    return winnings, winning_lines


def print_spinner(lines, spin, winning_lines):
    """
    Prints the slot machine spin.

    Args:
        lines (int): the number of lines bet on
        spin (list): the slot machine spin results
        winning_lines (list): indices of the winning lines
    """

    print()
    for row_idx, row in enumerate(spin):
        print(" | ".join(row), end="")
        if row_idx in winning_lines:
            print(" <<< WINNER")
        elif lines > row_idx:
            print(" < ")
        else:
            print()

    print()


def game(balance, spinner):
    """
    Plays a game of slots.

    Args:
        balance (int): player's balance
        spinner (list): slot machine spinner

    Returns:
        bool: true if the player wants to exit the game
        int: player's balance
    """

    # Find out how many lines the user would like to bet on
    lines = prompt_lines()

    # Find out the user's bet for each line
    bet = prompt_bet(balance, lines)

    # Print out the user's balance, number of lines, and bet
    total_bet = lines * bet
    balance -= total_bet
    print(f"Balance: ${balance}, Lines: {lines}, Bet: ${bet}, Total Bet: ${total_bet}")

    # Spin the slot machine
    input("\nPress Enter to spin the slot machine.")
    while True:
        spin = get_slot_machine_spin(COLS, spinner)

        # Calculate the user's winnings
        winnings, winning_lines = calculate_winnings(spin, bet, lines)

        # Print out the slot machine spin
        print_spinner(lines, spin, winning_lines)

        # Update the user's balance
        balance += winnings
        print(f"Balance: ${balance}")
        if balance <= 0:
            print("You are out of money.")
            return True, balance

        # Ask the user if they want to spin again
        action = input(
            """
(ENTER) to spin again
(C)hange Bet
(E)xit
$ """
        )
        match action.lower():
            case "c":
                return False, balance
            case "e":
                return True, balance

        # Pay for spin
        if balance >= total_bet:
            balance -= total_bet
            print(
                f"\nBalance: ${balance}, Lines: {lines}, Bet: ${bet}, Total Bet: ${total_bet}"
            )
        else:
            print(f"Insufficient funds. Balance: ${balance}")
            return False, balance


def main():
    """
    Main function to play the slot machine
    """

    # Generate the spinner
    spinner = generate_spinner(SYMBOL_COUNT)
    # print(f"Spinner: {spinner}")

    # Find out how much money the user would like to deposit
    balance = prompt_deposit()

    while True:
        do_exit, balance = game(balance, spinner)
        if do_exit:
            break


if __name__ == "__main__":
    main()
