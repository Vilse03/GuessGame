from guess_game import GuessGame, GameResult

def check_game_success():
    game = GuessGame(
        player_name = "Test",
        difficulty = "Lätt",
        max_number = 10,
        max_attempts = 5,
        secret_number = 7,
    )

    result = game.make_guess(7)

    assert result == "correct"
    assert game.success is True
    assert game.attempts_used == 1
    assert game.is_over() is True

def check_game_low_high():
    game = GuessGame(
        player_name = "Test",
        difficulty = "Medel",
        max_number = 50,
        max_attempts = 5,
        secret_number = 33
    )

    res_low = game.make_guess(10)
    res_high = game.make_guess(40)

    assert res_low == "low"
    assert res_high == "high"
    assert game.success is False
    assert game.attempts_used == 2

def test_scoreboard():
    game = GuessGame(
        player_name = "Oliver",
        difficulty = "Svår",
        max_number = 100,
        max_attempts = 3,
        secret_number = 42,
    )

    game.make_guess(50)
    game.make_guess(40)

    result = game.to_result()
    assert isinstance(result, GameResult)
    assert result.player_name == "Oliver"
    assert result.max_number == 100
    assert result.secret_number == 42
    assert result.attempts_used == 2
    assert result.success is False