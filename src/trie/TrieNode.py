class TrieNode:
    # 0 because that is the size of my dictionary: 'abcdefghijklmnopqrstuvwxyz12345670(|@$[!'
    _MAX_SIZE = 40

    def __init__(self):
        self.children = [None] * self._MAX_SIZE
        self.is_end_of_word = False