import json 
import random 
from dataclasses import dataclass, asdict #
from pathlib import Path
from typing import List
from typing import Optional 

DB_PATH = Path("db.json")

@dataclass
class GameResult:
    player_name:str
    difficulty: str
    max_number: int
    secret_number: int
    attempts_used: int
    max_attempts: int
    success: bool

    def to_dict(self) -> dict:
        return asdict(self)
    
class GuessGame: #Klass
    def __init__(
            self,
            player_name: str,
            difficulty: str,
            max_number: int,
            max_attempts: int,
            secret_number: Optional[int] = None,
    ) -> None:
        self.player_name = player_name
        self.difficulty = difficulty
        self.max_number = max_number
        self.max_attempts = max_attempts
        self.secret_number = secret_number or random.randint(1, max_number)
        self.attempts_used = 0
        self.success = False


#Gissning, returnerar olika beroende på hur nära man är
    def make_guess(self, guess: int) -> str:
        if self.is_over():
            return "game_over"
        
        self.attempts_used += 1

        if guess < self.secret_number:
            return "low"
        elif guess > self.secret_number:
            return "high"
        else:
            self.success = True
            return "correct"
        
    def is_over(self) -> bool:
        return self.success or self.attempts_used >= self.max_attempts
    
    def to_result(self) -> GameResult:
        return GameResult(
            player_name=self.player_name,
            difficulty = self.difficulty,
            max_number = self.max_number,
            secret_number = self.secret_number,
            attempts_used = self.attempts_used,
            max_attempts = self.max_attempts,
            success = self.success,
        )
    
# Tar upp scoreboard/ tidigare resultat som har lagrats
def load_results() -> List[dict]:
    if not DB_PATH.exists():
        return[]
    
    try:
        with DB_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        #Om filen är korrupt eller något går fel
        return []
    
#Spara ett nytt resultat
def save_result(result: GameResult) -> None:
    results = load_results()
    results.append(result.to_dict())

    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

#scoreboard / textlista över sparade spel
def results_summary(results: List[dict]) -> str:
    if not results:
        return "Inga tidigare spel sparade än."
    
    lines = ["Tidigare spel (Max 5 senaste):"]
    for i, r in enumerate(results[-5:], start = 1):
        status = "Vann" if r.get("success") else "Förlorade"
        lines.append(
            f"{i}. {r.get('player_name', 'Okänd')} | "
            f"Svårighet: {r.get('difficulty', '?')} | "
            f"Tal 1-{r.get('max_number', '?')} | "
            f"{status} på {r.get('attempts_used', '?')}/{r.get('max_attempts', '?')} försök"
        )
    return "\n".join(lines)