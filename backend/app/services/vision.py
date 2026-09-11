import math

def calculate_center(x, y, w, h):
    """Calculate the center point of a bounding box."""
    return (x + w / 2, y + h / 2)

def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def analyze_tactical_geometry(yolo_results, image_width=1920):
    """
    Analyzes standard YOLO bounding box outputs and applies tactical rules.
    
    yolo_results is expected to be a list of dictionaries:
    [
        {"class": "goalkeeper", "box": (x, y, w, h)},
        {"class": "player", "box": (x, y, w, h)},
        {"class": "ball", "box": (x, y, w, h)},
        ...
    ]
    (x, y) represents the top-left corner of the bounding box.
    """
    tactical_contexts = []
    
    players = []
    goalkeeper = None
    ball = None
    
    # Parse results
    for item in yolo_results:
        cls = item.get("class", "").lower()
        box = item.get("box")
        if not box:
            continue
            
        center = calculate_center(*box)
        
        if cls == "player":
            players.append({"box": box, "center": center})
        elif cls == "goalkeeper":
            goalkeeper = {"box": box, "center": center}
        elif cls == "ball":
            ball = {"box": box, "center": center}

    # Set some arbitrary pixel thresholds for proximity (can be tuned later)
    CROWDING_RADIUS = 150  # Pixels radius around the goalkeeper
    SHORT_CORNER_RADIUS = 200 # Pixels radius around the ball

    # 1. Goalkeeper Crowding
    if goalkeeper:
        gk_center = goalkeeper["center"]
        crowding_players = sum(
            1 for p in players if calculate_distance(p["center"], gk_center) <= CROWDING_RADIUS
        )
        if crowding_players >= 2:
            tactical_contexts.append("Tactical Context: The goalkeeper is being heavily crowded inside the 6-yard box.")

    # 2. Short Corner Overload & 3. Near/Far Post Density
    if ball:
        ball_center = ball["center"]
        
        # Rule 2: Short Corner Overload
        close_to_ball = sum(
            1 for p in players if calculate_distance(p["center"], ball_center) <= SHORT_CORNER_RADIUS
        )
        if close_to_ball >= 2:
            tactical_contexts.append("Tactical Context: A short corner routine is set up with an overload near the ball.")
            
        # Rule 3: Near-Post vs. Far-Post Density
        # Determine if ball is on left or right half
        ball_on_left = ball_center[0] < (image_width / 2)
        
        near_post_count = 0
        far_post_count = 0
        
        for p in players:
            p_x = p["center"][0]
            p_on_left = p_x < (image_width / 2)
            
            # If the player is on the same half as the ball, they are at the near post
            if p_on_left == ball_on_left:
                near_post_count += 1
            else:
                far_post_count += 1
                
        tactical_contexts.append(f"Tactical Context: There are {near_post_count} players at the near post and {far_post_count} players at the far post.")

    return " ".join(tactical_contexts)

# Example Usage
if __name__ == "__main__":
    mock_results = [
        {"class": "ball", "box": (100, 100, 20, 20)}, # Ball on the left
        {"class": "player", "box": (120, 110, 50, 150)}, # Player near ball
        {"class": "player", "box": (80, 90, 50, 150)}, # Player near ball (short corner)
        {"class": "goalkeeper", "box": (900, 500, 60, 160)}, # GK in the middle
        {"class": "player", "box": (880, 480, 50, 150)}, # Player crowding GK
        {"class": "player", "box": (920, 490, 50, 150)}, # Player crowding GK
        {"class": "player", "box": (1500, 400, 50, 150)} # Player far post
    ]
    
    print("Mock Image 1 (Left Side Corner, Overload & GK Crowded):")
    print(analyze_tactical_geometry(mock_results))
