LigaOst Tournament Manager by Oliver Beyer. 

This is the first iteration of the liga tool and it tries to create balanced teams for each round, manages match pairings, and updates player ratings based on results.

------------------------------------------------------------
BASIC WORKFLOW
------------------------------------------------------------

Each round follows this exact sequence:
0. Add Players to the player list. 
   -> See how to Add players below. important!

1. Click "New Round"
   -> Teams are generated and written to current_round.csv

2. Open current_round.csv
   ->Enter the match scores (e.g. 0:0 -> 3:2) to the file. don't touch anything else in the file. Just the score

3. Click "Finish Round (Update Ratings)"
   -> Player Ratings are updated automatically. See below for information

4. (Optional) Add new players to player_list.csv

5. Repeat

IMPORTANT:
Do NOT modify player_list.csv between steps 1 and 3.


------------------------------------------------------------
PLAYER LIST FORMAT (STRICT)
------------------------------------------------------------

The player list file must follow this exact format:

Name;Rating

Example:
MaxMuster-Vienna;300
Olli-Dresden;300
Levi-Gdansk;600

Rules:
- Player names must be unique, just add the city with an hyphon if you're unsure
- Exactly one ";" per line
- No spaces before or after ";"
- Each name must be UNIQUE
- ideally no empty lines at the end of the file
- Do NOT edit during an active round


------------------------------------------------------------
INITIAL RATINGS
------------------------------------------------------------

If players don't have a rating yet from previous days then
just have the players rate themselves on a scale of 1–10 and multiply by 100.

if people don't know how to rate them selfs, simply go by number of years the have played. 
played for five years? it's a five. It's just the initial rating, it doesn't matter too much. 

Convert to rating:
rating = self_rating × 100

Examples:
1 → 100
5 → 500
10 → 1000

Allowed range:
1 to 1000


------------------------------------------------------------
TEAM GENERATION
------------------------------------------------------------

- Teams are automatically balanced based on rating (to some extend)
- Each team has 3 players
- If needed, substitute players ("subs") are automatically added by the program! Don't add any subs to player list!

SUB RULES:
- Subs are selected randomly from the full player pool
- All players have equal chance
- A player can only be used once as a sub per round
- Subs are marked with "(sub)" in the output


------------------------------------------------------------
PAIRINGS
------------------------------------------------------------

- Teams are paired randomly
- The system avoids:
  → players facing themselves (including subs)

ODD NUMBER OF TEAMS:
- One team will play TWO matches. Lucky them ;)
- This is intentional and part of the system


------------------------------------------------------------
SCORING
------------------------------------------------------------

Scores are entered manually in current_round.csv:

Format:
3:2
5:5
0:1

Rules:
- Only wins, losses, and draws matter
- Goal difference is ignored. 

Reason:
I think a trailing team may take more risks, which can distort goal difference.
The system focuses on match outcome, not margin.


------------------------------------------------------------
RATING SYSTEM (ELO)
------------------------------------------------------------

- Ratings are updated after each round
- Based on standard ELO system
- Team rating = average of player ratings

Effects:
- Beating stronger teams → higher gain
- Losing to weaker teams → higher loss
- Close matches (equal teams) → moderate changes

Typical change:
~30 points for evenly matched teams for each player. 

for more information on this check the section "TECHNICAL DETAILS: RATING CALCULATION" below or the wikipedia page for elo


------------------------------------------------------------
FILES
------------------------------------------------------------

Main files:
- ligaost.exe
- player_list.csv
- current_round.csv (auto-generated)
- config.txt (don't touch unless you know what you're doing please!)

History:
- round_history/
  → contains archived rounds and player states


------------------------------------------------------------
IMPORTANT RULES
------------------------------------------------------------

- Do NOT edit player_list.csv during a round
- Always finish a round before starting a new one
- Ensure scores are valid before updating ratings
- Do not delete or rename files while the program is running
- close the files after editing them so they are not locked for the program 
    (when you use programs that lock the file for writing such as excel)


------------------------------------------------------------
COMMON MISTAKES
------------------------------------------------------------

Program crashes or errors usually come from:

- Empty line in player_list.csv (should not matter, but just so you know to look out for it)
- Missing rating
- Wrong format (missing ";")
- Duplicate player names
- Invalid score format (must be X:Y)
- files still open in another program that locks them for writing


------------------------------------------------------------
TECHNICAL DETAILS: RATING CALCULATION
------------------------------------------------------------

The rating system is based on the standard ELO formula, commonly used in chess and other competitive games.

Each match compares two teams:

- Team rating = average rating of all players in the team
- The system calculates how "expected" a win is based on rating difference

EXPECTED SCORE FORMULA:

Expected score of Team A vs Team B:

E_A = 1 / (1 + 10^((R_B - R_A) / 400))

Where:
- R_A = average rating of Team A
- R_B = average rating of Team B

Interpretation:
- If both teams have equal rating → expected score = 0.5
- If Team A is stronger → expected score > 0.5
- If Team A is weaker → expected score < 0.5


ACTUAL RESULT VALUES:

Win  → 1  
Draw → 0.5  
Loss → 0  


RATING UPDATE FORMULA:

New Rating = Old Rating + K × (Actual - Expected)

Where:
- K = scaling factor (configured in config.txt, only change that value if you know what you're doing)
- Higher K → larger rating changes


WHAT THIS MEANS IN PRACTICE:

- If you win a match you were expected to win → small rating gain
- If you win against a stronger team → large rating gain
- If you lose against a weaker team → large rating loss
- If teams are evenly matched → moderate rating changes (~30 points per player with a k=64)


IMPORTANT NOTES:

- Rating changes are applied individually to each player
- All players in a team receive the same adjustment
- Goal difference does NOT affect rating, only win/draw/loss matters
- Ratings are always rounded to whole numbers


WHY THIS SYSTEM?

The ELO system ensures:
- Fair adjustments based on opponent strength
- Stability over multiple rounds
- Resistance to random fluctuations

Over time, player ratings should converge to reflect actual skill levels.

------------------------------------------------------------
NOTES
------------------------------------------------------------

Have fun!

