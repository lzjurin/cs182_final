## CS182 Final Project
#### Xavier: Chess AI
###### Larry Zhang, Shayn Lozano, Ben Zheng

A chess AI that focuses on building a highly sophisticated evaluation function to identify best moves as opposed to using dictionaries of standard movesets or high-depth search expectimax.
Allows custom weight parametrization across 9 subevaluators:

1. Material
2. Threat level
3. Space
4. Mobility
5. Pawn structure
6. Piece-specific development
7. Piece-specific value (e.g. rook files)
8. King safety
9. Checkmate status
