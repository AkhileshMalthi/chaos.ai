#!/usr/bin/env python3
"""
Demo script showing how to use the chaos.ai prototype

Run this script to see a complete game in action:
    python demo.py
"""

from chaos_ai.game_session_manager import GameSessionManager
from chaos_ai.player_manager import PlayerManager
from chaos_ai.story_engine import StoryEngine
from chaos_ai.contribution_handler import ContributionHandler
from chaos_ai.genai_service import GenAIService
from chaos_ai.models import ContributionType


def print_separator():
    """Print a visual separator"""
    print("\n" + "=" * 70 + "\n")


def main():
    print_separator()
    print("🎮 Welcome to chaos.ai - Mock-First TDD Prototype Demo")
    print_separator()
    
    # Initialize all components
    print("🔧 Initializing game components...")
    player_manager = PlayerManager()
    genai_service = GenAIService()
    story_engine = StoryEngine(genai_service)
    contribution_handler = ContributionHandler()
    game_manager = GameSessionManager(
        player_manager=player_manager,
        story_engine=story_engine,
        contribution_handler=contribution_handler
    )
    print("✓ All components initialized")
    
    # Create a game session
    print_separator()
    print("📝 Creating game session...")
    session = game_manager.create_session(
        title="The Great Space Adventure",
        max_players=4,
        min_players=2
    )
    print(f"✓ Game session created: '{session.story.title}'")
    print(f"  Session ID: {session.session_id}")
    print(f"  Min players: {session.min_players}, Max players: {session.max_players}")
    
    # Register players
    print_separator()
    print("👥 Registering players...")
    player1 = player_manager.register_player("Alice")
    player2 = player_manager.register_player("Bob")
    player3 = player_manager.register_player("Charlie")
    
    print(f"✓ Registered: {player1.username} (ID: {player1.player_id[:8]}...)")
    print(f"✓ Registered: {player2.username} (ID: {player2.player_id[:8]}...)")
    print(f"✓ Registered: {player3.username} (ID: {player3.player_id[:8]}...)")
    
    # Players join the session
    print_separator()
    print("🚪 Players joining session...")
    game_manager.join_session(session.session_id, player1)
    print(f"✓ {player1.username} joined")
    game_manager.join_session(session.session_id, player2)
    print(f"✓ {player2.username} joined")
    game_manager.join_session(session.session_id, player3)
    print(f"✓ {player3.username} joined")
    print(f"\nTotal players: {len(session.players)}")
    
    # Start the game
    print_separator()
    print("🎬 Starting game...")
    game_manager.start_session(session.session_id)
    print(f"✓ Game started! Status: {session.status.value}")
    
    # Players take turns
    print_separator()
    print("📖 Story Building Phase")
    print_separator()
    
    turns = [
        (player1, "Once", ContributionType.WORD),
        (player2, "upon a time", ContributionType.PHRASE),
        (player3, "there was a brave astronaut", ContributionType.SENTENCE),
        (player1, "who discovered", ContributionType.PHRASE),
        (player2, "a mysterious planet", ContributionType.PHRASE),
        (player3, "filled with strange creatures", ContributionType.PHRASE),
        (player1, "that could talk", ContributionType.PHRASE),
        (player2, "and sing beautifully", ContributionType.PHRASE),
    ]
    
    for player, content, contribution_type in turns:
        turn_num = session.current_turn
        print(f"\n🎯 Turn {turn_num} - {player.username}'s turn")
        print(f"   Contribution: \"{content}\" ({contribution_type.value})")
        
        contribution = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player.player_id,
            content=content,
            contribution_type=contribution_type
        )
        
        if contribution:
            print(f"   ✓ Contribution accepted")
            
            # Check if a twist was added
            if len(session.story.ai_twists) > 0:
                latest_twist = session.story.ai_twists[-1]
                if latest_twist.applied_after_turn == turn_num:
                    print(f"\n   🎭 AI TWIST ADDED!")
                    print(f"   \"{latest_twist.content}\"")
        else:
            print(f"   ✗ Contribution rejected")
    
    # Get the complete story
    print_separator()
    print("📚 Complete Story")
    print_separator()
    
    story_text = game_manager.get_story_text(session.session_id)
    print(f"\n{story_text}\n")
    
    # End the game
    print_separator()
    print("🏁 Ending game...")
    game_manager.end_session(session.session_id)
    print(f"✓ Game ended. Status: {session.status.value}")
    
    # Final statistics
    print_separator()
    print("📊 Game Statistics")
    print_separator()
    print(f"Total turns: {session.current_turn}")
    print(f"Total contributions: {len(session.story.contributions)}")
    print(f"Total AI twists: {len(session.story.ai_twists)}")
    print(f"Players: {', '.join([p.username for p in session.players])}")
    
    print_separator()
    print("✨ Demo completed successfully!")
    print("\nTo see the tests that validate this behavior:")
    print("  pytest tests/test_integration_flow.py -v")
    print_separator()


if __name__ == "__main__":
    main()
