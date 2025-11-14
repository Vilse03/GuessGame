from guess_game import(
    GuessGame,
    load_results,
    save_result,
    results_summary,
)

#Heltal check
def ask_int(prompt: str, min_value: int | None = None, max_value: int | None = None) -> int:
    while True:
        s = input(prompt)
        try:
            value = int(s)
        except ValueError:
            print("Ogiltig inmatning, skriv ett heltal.")
            continue

        if min_value is not None and value < min_value:
            print(f"Värdet måste vara minst {min_value}.")
            continue
        if min_value is not None and value > max_value:
            print(f"Värdet får vara högst {max_value}.")
            continue

        return value
    
def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer in("j", "ja"):
            return True
        if answer in("n", "nej"):
            return False
        print("Skriv 'j' för ja eller 'n' för nej.")

#Svårighetsgrad  
def choose_difficulty() -> tuple[str, int]:
    print("\nVälj svårighet:")
    print("1. Lätt (tal mellan 1 och 10)")
    print("2. Medelsvår (tal mellan 1 och 50)")
    print("3. Svår (tal mellan 1 och 100)")

    choice = ask_int("Ditt val (1-3): ", 1, 3)

    if choice == 1:
        return "Lätt", 10
    elif choice == 2:
        return "Medelsvår", 50
    else:
        return "Svår", 100
    
def run_game() -> None:
    print("\n=== Guess the Number ===")
    name = input("Ange ditt namn: ").strip()
    if not name:
        name = "Gäst"

    difficulty_name, max_number = choose_difficulty()

    print("\nHur många försök vill du ha? (1-10)")
    max_attempts = ask_int("Antal försök: ", 1, 10)

    game = GuessGame(
        player_name = name,
        difficulty = difficulty_name,
        max_number = max_number,
        max_attempts = max_attempts,
    )

    print(
        f"\nOkej {name}! Jag tänker på ett tal mellan 1 och {max_number}. "
        f"Du har {max_attempts} försök, lycka till!"
    )

    while not game.is_over():
        guess = ask_int("\nGissa ett tal: ", 1, max_number)
        result = game.make_guess(guess)

        if result == "low":
            print("För lågt!")
        elif result == "high":
            print("För högt!")
        elif result == "correct":
            print("Du har gissat rätt, grattis!")
        elif result == "game_over":
            break

    final_result = game.to_result()
    print("\n=== Sammanfattning ===")
    if final_result.success:
        print(
            f"Grattis {final_result.player_name}! Du gissade rätt tal "
            f"{final_result.secret_number} på {final_result.attempts_used} försök."
        )
    else: 
        print(
            f"Tyvärr, du gissade inte rätt. Talet var {final_result.secret_number}. "
            f"Du använde alla {final_result.max_attempts} försök."
        )

    save_result(final_result)
    print("Ditt resultat har sparats i scoreboarden (db.json)\n")

def main() -> None:
    print("Välkommen till Guess the Number!")
    existing = load_results()
    print(results_summary(existing))

    while True:
        run_game()

        if not ask_yes_no("Vill du spela igen? (j/n): "):
            print("Tack för att du spelade! hej då!")
            break


if __name__ == "__main__":
    main()