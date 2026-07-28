class QueryRouter:

    GENERAL = [

        "hi",
        "hello",
        "hey",
        "how are you",
        "who are you",
        "good morning",
        "good evening",
        "thanks",
        "thank you",
        "bye"
    ]

    def is_general(self, question):

        q = question.lower().strip()

        return any(
            x in q
            for x in self.GENERAL
        )