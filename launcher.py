import pygame
from os import listdir
from os.path import isfile

import controller.main as cont

# Defining my colours
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (150, 0, 0)
GREEN = (0, 150, 0)
DARKGREEN = (30, 180, 30)
BLUE = (0, 0, 150)
CYAN = (50, 220, 220)
YELLOW = (220, 220, 50)

MAP_FOLDER = "./resources/maps/"
MEDIA_FOLDER = "./resources/media/"
STRATEGIES_FOLDER = "./resources/strategies/"

# Load all available maps
# Currently does not support usb
currentMap = 0
map_paths = []
map_info_paths = []
for folder in listdir(MAP_FOLDER):
	if ((not isfile(folder)) and (folder[:8] == "autocars")):
		for file in listdir(MAP_FOLDER + folder):
			if ((file[-4:] == ".png") and (file[:3] == "map")):
				map_paths.append(MAP_FOLDER + folder + "/" + file)
			if ((file[-4:] == ".txt") and (file[:3] == "map")):
				map_info_paths.append(MAP_FOLDER + folder + "/" + file)

strategy_paths = []
for file in listdir(STRATEGIES_FOLDER):
	if ((file[-3:] == ".py") and (file[:5] == "strat")):
		strategy_paths.append(STRATEGIES_FOLDER + file)

# Initialise output constructs
currentCar = 0
vision_modes = ["Regular", "Perfect"]
car_types = ["Car", "Truck", "Motorcycle", "Bicycle"]
en_text = ["Enabled", "Disabled"]
# car_data -> [desc,MAC,enabled,stratFile,visMode]
car_data = [["Red Car", "00:06:66:61:A3:48", 0, 0, 0, 0],
			["Green Car", "00:06:66:61:A9:3D", 0, 0, 0, 0],
			["Orange Car", "00:06:66:61:9B:2D", 0, 0, 0, 0],
			["Pink Car", "00:06:66:47:0A:0A", 0, 0, 0, 0],
			["Blue Car", "00:06:66:61:A6:CD", 0, 0, 0, 0],
			["Yellow Car", "00:06:66:61:9E:F7", 0, 0, 0, 0],
			["Black Car", "00:06:66:61:9E:A5", 0, 0, 0, 0]]
car_paths = [MEDIA_FOLDER + "redcar.jpg",
			 MEDIA_FOLDER + "greencar.jpg",
			 MEDIA_FOLDER + "orangecar.jpg",
			 MEDIA_FOLDER + "pinkcar.jpg",
			 MEDIA_FOLDER + "bluecar.jpg",
			 MEDIA_FOLDER + "yellowcar.jpg",
			 MEDIA_FOLDER + "blackcar.jpg"]
# map_data -> [carType,wetRoad,wind,fog,night,perfGPS]
map_data = [0, 0, 0, 0, 0]


# Label class
class Label:
	def __init__(self, x, y, text):
		self.text = text
		self.font_size = 28
		self.font = pygame.font.SysFont("comicsansms", self.font_size)
		self.font.set_bold(1)
		self.color = WHITE
		self.x = x
		self.y = y
		labels.append(self)

	def render(self):
		screen.blit(self.font.render(self.text, True, self.color), [self.x, self.y])


# Button class
class Button:
	def __init__(self, x, y, w, h):
		self.id = "Blank"
		self.text = ""
		self.font_size = 28
		self.font = pygame.font.SysFont("comicsansms", self.font_size)
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.next = [-1, -1, -1, -1]
		self.img = -1
		self.colors = [BLUE, YELLOW, BLACK, CYAN]
		self.border_w = 5
		self.hover = 0
		self.selected = 0
		buttons.append(self)

	# Draw background then border
	def render(self):
		if (self.img == -1):
			# Fill color
			temp_bg_color = self.colors[0]
			if (self.selected == 1):
				temp_bg_color = self.colors[1]
			pygame.draw.rect(screen, temp_bg_color, (self.x, self.y, self.w, self.h), 0)
		else:
			# Draw image
			button_img = pygame.image.load(self.img)
			button_img = pygame.transform.scale(button_img, (self.w, self.h))
			screen.blit(button_img, (self.x, self.y))

		# Draw text
		if (self.text != ""):
			screen.blit(self.font.render(self.text, True, WHITE),
						[self.x + 8, self.y + self.h / 2 - self.font_size / 2 - 4])

		temp_bd_color = self.colors[2]
		if (self.hover == 1):
			temp_bd_color = self.colors[3]
		pygame.draw.rect(screen, temp_bd_color, (self.x, self.y, self.w, self.h), self.border_w)

	# Based on current direction options and input, change hover states
	def go_next(self, direction):
		if (self.next[direction] != -1):
			self.hover = 0
			buttons[self.next[direction]].hover = 1

	def onClick(self, button):
		print("You clicked button " + button + " and I'm not doing anything!")


def checkOverflow(num, min, max):
	result = num
	if (result < min):
		result = max
	if (result > max):
		result = min
	return result


def loadMap(map_index):
	buttons[0].img = map_paths[map_index]
	labels[0].text = map_paths[map_index]
	labels[1].text = map_info_paths[map_index]


def loadCar(car_index):
	buttons[1].img = car_paths[car_index]
	buttons[2].selected = 1 - car_data[car_index][2]
	buttons[2].text = en_text[buttons[2].selected]
	buttons[3].text = strategy_paths[car_data[car_index][3]]
	buttons[4].text = vision_modes[car_data[car_index][4]]
	buttons[5].text = car_types[car_data[car_index][5]]
	labels[2].text = car_data[car_index][0] + "  |  " + car_data[car_index][1]
	buttons[7].selected = 1 - map_data[0]
	buttons[8].selected = 1 - map_data[1]
	buttons[9].selected = 1 - map_data[2]
	buttons[10].selected = 1 - map_data[3]
	buttons[11].selected = 1 - map_data[4]


# Button onClick methods
def onClick_map_image_button(button):
	global currentMap
	currentMap += (-2 * button + 1)
	currentMap = checkOverflow(currentMap, 0, len(map_paths) - 1)
	loadMap(currentMap)


def onClick_car_image_button(button):
	global currentCar
	currentCar += (-2 * button + 1)
	currentCar = checkOverflow(currentCar, 0, len(car_data) - 1)
	loadCar(currentCar)


def onClick_car_enabled_button(button):
	car_data[currentCar][2] = 1 - car_data[currentCar][2]
	loadCar(currentCar)


def onClick_wet_road_button(button):
	map_data[0] = 1 - map_data[0]
	loadCar(currentCar)


def onClick_wind_button(button):
	map_data[1] = 1 - map_data[1]
	loadCar(currentCar)


def onClick_fog_button(button):
	map_data[2] = 1 - map_data[2]
	loadCar(currentCar)


def onClick_night_button(button):
	map_data[3] = 1 - map_data[3]
	loadCar(currentCar)


def onClick_perfGPS_button(button):
	map_data[4] = 1 - map_data[4]
	loadCar(currentCar)


def onClick_strategy_text_button(button):
	car_data[currentCar][3] += (-2 * button + 1)
	car_data[currentCar][3] = checkOverflow(car_data[currentCar][3], 0, len(strategy_paths) - 1)
	loadCar(currentCar)


def onClick_vision_text_button(button):
	car_data[currentCar][4] += (-2 * button + 1)
	car_data[currentCar][4] = checkOverflow(car_data[currentCar][4], 0, len(vision_modes) - 1)
	loadCar(currentCar)


def onClick_cartype_text_button(button):
	car_data[currentCar][5] += (-2 * button + 1)
	car_data[currentCar][5] = checkOverflow(car_data[currentCar][5], 0, len(car_types) - 1)
	loadCar(currentCar)


def onClick_launch_button(button):
	global done
	if (button == 0):
		done = 1
		car_params = car_data
		map_params = map_data
		en_convert = [False, True]
		index = 0
		while (index < 4):
			car_params[index][2] = en_convert[car_data[index][2]]
			car_params[index][3] = strategy_paths[car_data[index][3]]
			car_params[index][4] = vision_modes[car_data[index][4]]
			car_params[index][5] = car_types[car_data[index][5]]
			index += 1
		pygame.quit()
		cont.main(map_paths[currentMap], map_info_paths[currentMap], car_params, map_params)


def init_buttons():
	# Map image button
	t = Button(20, 20, 450, 300)
	t.id = "map_image_button"
	t.img = MAP_FOLDER + "autocars_map_basic/map_basic.png"
	t.next = [-1, 7, 1, -1]
	t.onClick = onClick_map_image_button
	t.hover = 1

	# Car image button
	t = Button(20, 450, 450, 300)
	t.id = "car_image_button"
	t.img = car_paths[0]
	t.next = [0, 11, 2, -1]
	t.onClick = onClick_car_image_button

	# Car enabled button
	t = Button(350, 770, 120, 50)
	t.id = "car_enabled_button"
	t.next = [1, 11, 3, -1]
	t.onClick = onClick_car_enabled_button
	t.colors = [GREEN, RED, BLACK, CYAN]
	t.text = "Disabled"

	# Strategy text button
	t = Button(200, 860, 800, 60)
	t.id = "strategy_text_button"
	t.next = [2, 6, 4, -1]
	t.onClick = onClick_strategy_text_button
	t.text = "Default"
	t.font = pygame.font.SysFont("comicsansms", 40)

	# Agent type text button
	t = Button(200, 960, 800, 60)
	t.id = "agent_type_button"
	t.next = [3, 6, 5, -1]
	t.onClick = onClick_vision_text_button
	t.text = "Default"
	t.font = pygame.font.SysFont("comicsansms", 40)

	# Car type text button
	t = Button(200, 1060, 800, 60)
	t.id = "car_type_button"
	t.next = [4, 6, -1, -1]
	t.onClick = onClick_cartype_text_button
	t.text = "Default"
	t.font = pygame.font.SysFont("comicsansms", 40)

	# Launch button
	t = Button(1150, 500, 300, 200)
	t.id = "launch_button"
	t.next = [-1, -1, 3, 11]
	t.onClick = onClick_launch_button
	t.colors = [DARKGREEN, RED, BLACK, CYAN]
	t.text = "Launch"
	t.font = pygame.font.SysFont("comicsansms", 80)

	# Wet Road button
	t = Button(650, 100, 300, 80)
	t.id = "wet_road_button"
	t.next = [-1, 6, 8, 0]
	t.onClick = onClick_wet_road_button
	t.colors = [GREEN, RED, BLACK, CYAN]
	t.text = "Wet Road"

	# Wind button
	t = Button(650, 200, 300, 80)
	t.id = "wind_button"
	t.next = [7, 6, 9, 0]
	t.onClick = onClick_wind_button
	t.colors = [GREEN, RED, BLACK, CYAN]
	t.text = "Wind"

	# Fog button
	t = Button(650, 300, 300, 80)
	t.id = "fog_button"
	t.next = [8, 6, 10, 1]
	t.onClick = onClick_fog_button
	t.colors = [GREEN, RED, BLACK, CYAN]
	t.text = "Fog"

	# Night button
	t = Button(650, 400, 300, 80)
	t.id = "night_button"
	t.next = [9, 6, 11, 1]
	t.onClick = onClick_night_button
	t.colors = [GREEN, RED, BLACK, CYAN]
	t.text = "Night Time"

	# Perfect GPS button
	t = Button(650, 500, 300, 80)
	t.id = "perfGPS_button"
	t.next = [10, 6, 3, 1]
	t.onClick = onClick_perfGPS_button
	t.colors = [GREEN, RED, BLACK, CYAN]
	t.text = "GPS Noise"


def init_labels():
	# Map file label
	t = Label(20, 350, "Default")
	# Map data file label
	t = Label(20, 380, "Default")
	# Car ID label
	t = Label(20, 780, "Default")
	# Strategy file label
	t = Label(20, 872, "Strategy:")
	t.font = pygame.font.SysFont("comicsansms", 40)
	# Vision mode label
	t = Label(20, 972, "Vision Mode:")
	t.font = pygame.font.SysFont("comicsansms", 40)
	# Car type label
	t = Label(20, 1072, "Vehicle:")
	t.font = pygame.font.SysFont("comicsansms", 40)


# Initialise pygame module
pygame.init()
# Initialise screen with chosen size
size = [1600, 1200]
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
# Give my game window a title
pygame.display.set_caption("Title Screen")

# Initialise pygame clock
clock = pygame.time.Clock()
# Initialise pygame joystick functions
pygame.joystick.init()
# Initialise buttons
buttons = []
labels = []
init_buttons()
init_labels()
loadCar(currentCar)
loadMap(currentMap)
# Remember last state of the joystick hat
last_hat = [0, 0]
# Used to break out of the loop when required
done = 0
while (done == 0):
	button_tapped = -1
	# Check if a joystick is connected
	if (pygame.joystick.get_count() < 1):
		print("No gamepad detected. Exiting...")
		break
	# Given a joystick is connected, initialise it
	# If more than one is connected, we only use the first one
	joystick = pygame.joystick.Joystick(0)
	joystick.init()
	# Handle user input events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = 1
		if event.type == pygame.JOYBUTTONDOWN:
			# Note which button was tapped
			# 0=A, 1=B, X,Y,LB,RB,St,Se
			index = 0
			while (index < 6):
				if (joystick.get_button(index)):
					button_tapped = index

					break
				index += 1

	# Deal with button tap
	if (button_tapped != -1):
		# We hit a button!
		for b in buttons:
			if (b.hover == 1):
				if (button_tapped <= 3):
					temp = [2, 1, 3, 0]
					b.go_next(temp[button_tapped])
					button_tapped = -1
					break
				if (button_tapped == 4):
					b.onClick(1)
					break
				if (button_tapped == 5):
					b.onClick(0)
					break

	# Wash with clean background
	screen.fill(pygame.Color("black"))
	# Draw UI Divisions
	pygame.draw.rect(screen, GRAY, (1050, 0, 10, 1200), 0)
	pygame.draw.rect(screen, GRAY, (0, 430, 500, 10), 0)
	pygame.draw.rect(screen, GRAY, (500, 430, 10, 400), 0)
	pygame.draw.rect(screen, GRAY, (500, 830, 550, 10), 0)

	# Draw all buttons
	for b in buttons:
		b.render()

	# Draw all labels
	for l in labels:
		l.render()

	# Update screen with new contents
	pygame.display.flip()

	# Limit game fps
	clock.tick(40)

pygame.quit()
quit()
