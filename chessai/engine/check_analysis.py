class CheckAnalysis:
    def __init__(
        self,
        there_is_check,
        cord_of_piece_to_capture,
        interposing_dest_coordinates,
        king_legal_moves,
    ):
        self.there_is_check = there_is_check
        self.cord_of_piece_to_capture = cord_of_piece_to_capture
        self.interposing_dest_coordinates = interposing_dest_coordinates
        self.king_legal_moves = king_legal_moves
