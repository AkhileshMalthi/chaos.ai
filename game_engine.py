from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

class StoryGameEngine:
    def __init__(self, model_name="llama-3.3-70b-versatile", temperature=0.8, api_key=None):
        self.llm = ChatGroq(model=model_name, temperature=temperature, groq_api_key=api_key)
        self.history = []
        self.current_story = ""
        self.turn = 0
        self.players = []

    def add_player(self, name):
        if name not in self.players:
            self.players.append(name)

    def reset(self):
        self.history.clear()
        self.current_story = ""
        self.turn = 0
        self.players.clear()

    def contribute(self, player, contribution):
        self.add_player(player)
        record = f"{player}: {contribution}"
        self.history.append(record)
        self.current_story += f" {contribution}"
        self.turn += 1

class ModifiedStoryGameEngine(StoryGameEngine):
    def genai_twist(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a mischievous AI Game Master for a multiplayer story game. Your job is to inject a wild, dramatic, funny, and unpredictable twist into the story. The twist must be a complete sentence between 20 and 30 words long. Story so far:"),
            ("human", self.current_story.strip())
        ])
        chain = prompt | self.llm
        twist_msg = chain.invoke({})
        twist = twist_msg.content.strip()

        # Limit to 20-30 words, keep sentence meaningful
        words = twist.split()
        if len(words) > 30:
            truncated = " ".join(words[:30])
            if '.' in truncated:
                twist = truncated.rsplit('.', 1)[0] + '.'
            else:
                twist = truncated

        record = f"Chaos Engine: {twist}"
        self.history.append(record)
        self.current_story += f" {twist}"
        return twist

    def get_state(self):
        return {
            "turn": self.turn,
            "players": self.players[:],
            "history": self.history[:],
            "current_story": self.current_story.strip()
        }

if __name__ == "__main__":
    game = ModifiedStoryGameEngine(api_key=os.getenv("GROQ_API_KEY"))

    num_players = int(input("Enter number of players: "))
    for _ in range(num_players):
        player_name = input("Enter player name: ").strip()
        game.add_player(player_name)

    while True:
        for player in game.players:
            contribution = input(f"{player} (or type 'exit' to stop): ")
            if contribution.lower() == 'exit':
                print("Game ended.")
                exit(0)
            game.contribute(player, contribution)

            # Add AI twist every round
            if game.turn % 1 == 0:
                twist = game.genai_twist()
                print("AI Twist:", twist)
