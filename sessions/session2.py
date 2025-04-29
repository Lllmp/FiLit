import streamlit as st
from utils import (
    award_coins, 
    award_achievement, 
    update_progress, 
    mark_activity_complete, 
    is_activity_completed,
    create_quiz_question,  # Add this import to all session files
    safe_rerun  # Use this instead of st.experimental_rerun
)
from styles import apply_session_goals_styling


def run():
    """
    Session 2: Money for Needs and Wants
    
    Objectives:
    - Describe the difference between needs and wants
    - Explain that families must earn money for the things they need and want
    """
    st.header("🛒 Session 2: Money for Needs and Wants")
    
    # Session overview

    # List of goals for this session
    goals = [
        "Learn the difference between needs and wants",
        "Understand that families must earn money for things they need and want",
        "Practice making choices about spending money"
    ]

    # Apply styled session goals
    apply_session_goals_styling(goals)
    
    # Vocabulary section
    st.subheader("📝 Important Words to Know")
    
    vocab_col1, vocab_col2 = st.columns(2)
    
    with vocab_col1:
        st.markdown("""
        <div class="vocabulary-card">
            <h4>Needs</h4>
            <p>Things people must have to live, like:</p>
            <ul>
                <li>Food</li>
                <li>Water</li>
                <li>Shelter (a home)</li>
                <li>Clothing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with vocab_col2:
        st.markdown("""
        <div class="vocabulary-card">
            <h4>Wants</h4>
            <p>Things that are nice to have, but not necessary to live, like:</p>
            <ul>
                <li>Toys</li>
                <li>Video Games</li>
                <li>Ice Cream</li>
                <li>Movie Tickets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive needs vs wants game
    st.subheader("🎮 Needs vs. Wants Sorting Game")
    
    st.markdown("""
    <div class="fun-box">
        <h3>Let's Play the Needs and Wants Game!</h3>
        <p>Sort each item as either a NEED or a WANT.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Items to sort
    if 'items_sorted' not in st.session_state:
        st.session_state.items_sorted = {
            "Apple": "",
            "Bicycle": "",
            "House": "",
            "Video Game": "",
            "Winter Coat": "",
            "Water": "",
            "Toy Car": "",
            "School Books": "",
            "Chocolate": "",
            "Medicine": ""
        }
        st.session_state.items_correct = {
            "Apple": "Need",
            "Bicycle": "Want",
            "House": "Need",
            "Video Game": "Want",
            "Winter Coat": "Need",
            "Water": "Need",
            "Toy Car": "Want",
            "School Books": "Need",
            "Chocolate": "Want",
            "Medicine": "Need"
        }
    
    # Item icons
    item_icons = {
        "Apple": "🍎",
        "Bicycle": "🚲",
        "House": "🏠",
        "Video Game": "🎮",
        "Winter Coat": "🧥",
        "Water": "💧",
        "Toy Car": "🚗",
        "School Books": "📚",
        "Chocolate": "🍫",
        "Medicine": "💊"
    }
    
    # Create two columns for the game
    game_col1, game_col2 = st.columns(2)
    
    with game_col1:
        st.markdown(f"""
        <div style="background-color: #4361EE; padding: 10px; border-radius: 10px; color: white; text-align: center; margin-bottom: 10px;">
            <h3 style="margin: 0;">NEEDS</h3>
            <p style="margin: 0; font-size: 14px;">Things we must have</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display items sorted as needs
        for item, category in st.session_state.items_sorted.items():
            if category == "Need":
                st.markdown(f"""
                <div class="game-card need">
                    <div style="font-size: 24px;">{item_icons[item]}</div>
                    <p style="margin: 5px 0 0 0;"><b>{item}</b></p>
                </div>
                """, unsafe_allow_html=True)
    
    with game_col2:
        st.markdown(f"""
        <div style="background-color: #FF5C8D; padding: 10px; border-radius: 10px; color: white; text-align: center; margin-bottom: 10px;">
            <h3 style="margin: 0;">WANTS</h3>
            <p style="margin: 0; font-size: 14px;">Things that are nice to have</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display items sorted as wants
        for item, category in st.session_state.items_sorted.items():
            if category == "Want":
                st.markdown(f"""
                <div class="game-card want">
                    <div style="font-size: 24px;">{item_icons[item]}</div>
                    <p style="margin: 5px 0 0 0;"><b>{item}</b></p>
                </div>
                """, unsafe_allow_html=True)
    
    # Items to sort section
    st.markdown("### Items to Sort")
    
    # Calculate sorted and unsorted items
    sorted_items = [item for item, category in st.session_state.items_sorted.items() if category]
    unsorted_items = [item for item, category in st.session_state.items_sorted.items() if not category]
    
    # Display progress
    st.progress(len(sorted_items) / len(st.session_state.items_sorted))
    st.write(f"You've sorted {len(sorted_items)} out of {len(st.session_state.items_sorted)} items")
    
    # Item grid (3 columns)
    if unsorted_items:
        item_cols = st.columns(3)
        for i, item in enumerate(unsorted_items):
            with item_cols[i % 3]:
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 32px;">{item_icons[item]}</div>
                    <p style="margin: 5px 0;"><b>{item}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Need", key=f"need_{item}"):
                        st.session_state.items_sorted[item] = "Need"
                        st.rerun()
                with col2:
                    if st.button(f"Want", key=f"want_{item}"):
                        st.session_state.items_sorted[item] = "Want"
                        st.rerun()
    
    # Check answers button (only if all items are sorted)
    if not unsorted_items:
        if st.button("Check My Answers"):
            # Count correct answers
            correct = 0
            for item, sorted_category in st.session_state.items_sorted.items():
                if sorted_category == st.session_state.items_correct[item]:
                    correct += 1
            
            # Display results
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 15px; text-align: center; margin-top: 20px;">
                <h3>Your Score: {correct}/{len(st.session_state.items_sorted)}</h3>
                <p>You got {correct} out of {len(st.session_state.items_sorted)} items correct!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Award coins based on performance
            if mark_activity_complete("needs_wants_game"):
                coins_earned = correct * 2
                award_coins(coins_earned, f"Getting {correct} answers correct in the Needs vs. Wants game")
                
                # Update progress
                update_progress("session2", 40)
                
                # Award achievement if they did well
                if correct >= 8:
                    award_achievement("🛒", "Smart Shopper", "You know the difference between needs and wants!")
            
            # Reset game button
            if st.button("Play Again"):
                for item in st.session_state.items_sorted:
                    st.session_state.items_sorted[item] = ""
                st.rerun()
    
    # Shopping decisions activity
    st.subheader("💵 Making Smart Money Choices")
    
    st.markdown("""
    <div class="fun-box">
        <h3>Shopping with $20</h3>
        <p>You have $20 to spend. What would you buy?</p>
        <p>Remember to think about needs before wants!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Shopping items
    shopping_items = [
        {"name": "Sandwich", "price": 5, "category": "Need", "icon": "🥪"},
        {"name": "Toy Car", "price": 8, "category": "Want", "icon": "🚗"},
        {"name": "Water Bottle", "price": 3, "category": "Need", "icon": "🍶"},
        {"name": "Stickers", "price": 2, "category": "Want", "icon": "🏷️"},
        {"name": "Mittens", "price": 7, "category": "Need", "icon": "🧤"},
        {"name": "Candy Bar", "price": 1, "category": "Want", "icon": "🍫"},
        {"name": "Book", "price": 9, "category": "Need", "icon": "📘"},
        {"name": "Bouncy Ball", "price": 3, "category": "Want", "icon": "⚽"}
    ]
    
    # Initialize shopping cart if not exists
    if 'shopping_cart' not in st.session_state:
        st.session_state.shopping_cart = []
    
    # Function to calculate remaining budget
    def calculate_remaining():
        spent = sum(item["price"] for item in st.session_state.shopping_cart)
        return 20 - spent
    
    # Display remaining budget
    remaining_budget = calculate_remaining()
    
    st.markdown(f"""
    <div style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h4 style="margin: 0;">Your Budget:</h4>
            <p style="margin: 0; font-size: 14px;">Money you have to spend</p>
        </div>
        <div style="font-size: 24px; font-weight: bold; color: #4361EE;">
            ${remaining_budget}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Shopping items display
    st.markdown("### Store Items")
    
    # Create a grid of items for shopping
    item_cols = st.columns(4)
    for i, item in enumerate(shopping_items):
        with item_cols[i % 4]:
            # Check if item is in cart
            in_cart = any(cart_item["name"] == item["name"] for cart_item in st.session_state.shopping_cart)
            
            # Display badge for need/want
            badge_color = "badge-blue" if item["category"] == "Need" else "badge-pink"
            
            st.markdown(f"""
            <div style="background-color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                <span class="badge {badge_color}">{item["category"]}</span>
                <div style="font-size: 32px; margin: 10px 0;">{item["icon"]}</div>
                <h4 style="margin: 5px 0;">{item["name"]}</h4>
                <p style="font-weight: bold; color: #4361EE;">${item["price"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add/Remove button
            if in_cart:
                if st.button("Remove", key=f"remove_{item['name']}"):
                    # Find and remove the item
                    for j, cart_item in enumerate(st.session_state.shopping_cart):
                        if cart_item["name"] == item["name"]:
                            st.session_state.shopping_cart.pop(j)
                            break
                    st.rerun()
            else:
                # Disable button if not enough money
                disabled = item["price"] > remaining_budget
                if st.button("Add to Cart", key=f"add_{item['name']}", disabled=disabled):
                    st.session_state.shopping_cart.append(item)
                    st.rerun()
    
    # Shopping cart
    st.markdown("### Your Shopping Cart")
    
    if st.session_state.shopping_cart:
        # Display cart items in a table format
        st.markdown("""
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #f1f3f9;">
                <th style="padding: 10px; text-align: left;">Item</th>
                <th style="padding: 10px; text-align: left;">Type</th>
                <th style="padding: 10px; text-align: right;">Price</th>
            </tr>
        """, unsafe_allow_html=True)
        
        for item in st.session_state.shopping_cart:
            badge_color = "badge-blue" if item["category"] == "Need" else "badge-pink"
            
            st.markdown(f"""
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 10px;">{item["icon"]} {item["name"]}</td>
                <td style="padding: 10px;"><span class="badge {badge_color}">{item["category"]}</span></td>
                <td style="padding: 10px; text-align: right;">${item["price"]}</td>
            </tr>
            """, unsafe_allow_html=True)
        
        # Calculate totals
        total_spent = sum(item["price"] for item in st.session_state.shopping_cart)
        needs_spent = sum(item["price"] for item in st.session_state.shopping_cart if item["category"] == "Need")
        wants_spent = sum(item["price"] for item in st.session_state.shopping_cart if item["category"] == "Want")
        
        st.markdown(f"""
            <tr style="border-top: 2px solid #ddd; font-weight: bold;">
                <td style="padding: 10px;" colspan="2">Total:</td>
                <td style="padding: 10px; text-align: right;">${total_spent}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
        
        # Spending breakdown
        st.markdown(f"""
        <div style="display: flex; margin-top: 15px;">
            <div style="flex: 1; padding: 10px; background-color: #e6f3ff; border-radius: 10px 0 0 10px; text-align: center;">
                <p style="margin: 0; font-weight: bold;">Spent on Needs</p>
                <p style="font-size: 20px; margin: 5px 0; color: #4361EE;">${needs_spent}</p>
            </div>
            <div style="flex: 1; padding: 10px; background-color: #ffe6ee; border-radius: 0 10px 10px 0; text-align: center;">
                <p style="margin: 0; font-weight: bold;">Spent on Wants</p>
                <p style="font-size: 20px; margin: 5px 0; color: #FF5C8D;">${wants_spent}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Checkout button
        if st.button("Checkout"):
            # Calculate the balance of needs vs wants
            needs_count = sum(1 for item in st.session_state.shopping_cart if item["category"] == "Need")
            wants_count = sum(1 for item in st.session_state.shopping_cart if item["category"] == "Want")
            
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 15px; margin-top: 20px;">
                <h3>Shopping Results</h3>
                <p>You bought {needs_count} needs and {wants_count} wants.</p>
            """, unsafe_allow_html=True)
            
            # Give feedback based on their choices
            if needs_count > wants_count:
                st.markdown("""
                <p style="color: green;">Great job! You prioritized needs over wants. That's smart money management!</p>
                """, unsafe_allow_html=True)
                if mark_activity_complete("shopping_activity"):
                    award_coins(10, "Making smart shopping choices")
                    update_progress("session2", 30)
            elif needs_count == wants_count:
                st.markdown("""
                <p style="color: blue;">You balanced needs and wants. Remember that needs should usually come first!</p>
                """, unsafe_allow_html=True)
                if mark_activity_complete("shopping_activity"):
                    award_coins(5, "Completing the shopping activity")
                    update_progress("session2", 20)
            else:
                st.markdown("""
                <p style="color: orange;">You spent more on wants than needs. Remember to take care of needs first!</p>
                """, unsafe_allow_html=True)
                if mark_activity_complete("shopping_activity"):
                    award_coins(3, "Completing the shopping activity")
                    update_progress("session2", 10)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Reset button
            if st.button("Shop Again"):
                st.session_state.shopping_cart = []
                st.rerun()
    else:
        st.info("Your shopping cart is empty. Add some items!")
    
    # Comprehension check
    with st.expander("✅ Check Your Learning"):
        st.markdown("### Review what you've learned about needs and wants")
        
        q1 = st.radio(
            "Why do families need to earn money?",
            ["To buy toys only", "To buy things they need and want", "To make other families sad", "Money isn't important"],
            index=None
        )
        
        if q1 == "To buy things they need and want":
            st.success("Correct! Families earn money so they can buy the things they need to live and some things they want.")
            if mark_activity_complete("session2_q1"):
                award_coins(5, "Understanding why families need money")
                update_progress("session2", 20)
        elif q1 != "":
            st.error("That's not quite right. Think about what families use money for.")
        
        q2 = st.radio(
            "Which of these is a need?",
            ["Video game", "Toy robot", "Water", "Candy"],
            index=None
        )
        
        if q2 == "Water":
            st.success("Correct! Water is something people need to live.")
            if mark_activity_complete("session2_q2"):
                award_coins(5, "Identifying needs correctly")
                update_progress("session2", 10)
                
                # Award achievement if both questions correct
                if is_activity_completed("session2_q1") and is_activity_completed("needs_wants_game"):
                    award_achievement("💵", "Money Maven", "You understand needs, wants, and why families need money!")