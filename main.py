import turtle
import random

# --- 1. GAME SETUP ---
screen = turtle.Screen()
screen.title("Grid Clicker! 2-Minute Challenge")
screen.bgcolor("#f7fafc")
screen.setup(width=500, height=600)
screen.tracer(0) # Turns off animations for instant drawing

# Game state variables
score = 0
time_left = 120  # 2 minutes in seconds
game_active = True

GRID_SIZE = 100
COLS = 3
ROWS = 3

# Calculate start offsets to center a 300x300 grid
start_x = -150
start_y = -150

# --- 2. DRAW THE GRID BACKGROUND ---
grid_drawer = turtle.Turtle()
grid_drawer.hideturtle()
grid_drawer.speed(0)
grid_drawer.pensize(3)

# Draw horizontal lines
for i in range(ROWS + 1):
    grid_drawer.penup()
    grid_drawer.goto(start_x, start_y + i * GRID_SIZE)
    grid_drawer.color("#cbd5e0")
    grid_drawer.pendown()
    grid_drawer.goto(start_x + COLS * GRID_SIZE, start_y + i * GRID_SIZE)

# Draw vertical lines
for i in range(COLS + 1):
    grid_drawer.penup()
    grid_drawer.goto(start_x + i * GRID_SIZE, start_y)
    grid_drawer.color("#cbd5e0")
    grid_drawer.pendown()
    grid_drawer.goto(start_x + i * GRID_SIZE, start_y + ROWS * GRID_SIZE)

# --- 3. THE HUD (SCORE & TIMER) ---
hud = turtle.Turtle()
hud.hideturtle()
hud.penup()
hud.color("#2d3748")

def update_hud():
    hud.clear()
    hud.goto(-200, 200)
    hud.write(f"SCORE: {score}", align="left", font=("Arial", 18, "bold"))
    
    # Color warning for low time
    if time_left <= 10:
        hud.color("#e53e3e") # Red
    else:
        hud.color("#2d3748")
        
    hud.goto(200, 200)
    hud.write(f"TIME: {time_left}s", align="right", font=("Arial", 18, "bold"))
    screen.update()

# --- 4. THE LIT-UP TARGET ---
# We use a square-shaped turtle stretched to fit the grid cell
target = turtle.Turtle()
target.shape("square")
# Default turtle size is 20x20 pixels. 4.75 * 20 = 95 pixels (leaves a nice tiny gap in a 100px grid cell)
target.shapesize(4.75, 4.75) 
target.color("#ecc94b")  # Bright golden yellow
target.penup()
target.speed(0)

# Grid coordinate tracking
current_col = 1
current_row = 1

def move_target():
    global current_col, current_row
    # Choose a new random spot, making sure it isn't the exact same one as before
    new_col, new_row = current_col, current_row
    while new_col == current_col and new_row == current_row:
        new_col = random.randint(0, COLS - 1)
        new_row = random.randint(0, ROWS - 1)
        
    current_col, current_row = new_col, new_row
    
    # Calculate screen coordinates for the center of the chosen grid cell
    x = start_x + (current_col * GRID_SIZE) + (GRID_SIZE / 2)
    y = start_y + (current_row * GRID_SIZE) + (GRID_SIZE / 2)
    target.goto(x, y)
    screen.update()

# Spawn the first target
move_target()
update_hud()

# --- 5. GAME FUNCTIONS & CLICKS ---
def on_target_click(x, y):
    global score
    if not game_active:
        return
    
    score += 1
    update_hud()
    move_target()

# Bind the click action directly to the yellow target turtle
target.onclick(on_target_click)

def game_over():
    global game_active
    game_active = False
    target.hideturtle()
    
    # Draw Game Over message
    end_text = turtle.Turtle()
    end_text.hideturtle()
    end_text.penup()
    end_text.color("#e53e3e")
    end_text.goto(0, 30)
    end_text.write("TIME'S UP!", align="center", font=("Arial", 28, "bold"))
    end_text.color("#2d3748")
    end_text.goto(0, -20)
    end_text.write(f"Final Score: {score}", align="center", font=("Arial", 22, "bold"))
    screen.update()

# Countdown timer function running in the background
def tick():
    global time_left
    if time_left > 0:
        time_left -= 1
        update_hud()
        screen.ontimer(tick, 1000) # Run tick again in 1 second (1000 ms)
    else:
        game_over()

# Start the timer countdown loop
screen.ontimer(tick, 1000)

screen.update()
screen.mainloop()
