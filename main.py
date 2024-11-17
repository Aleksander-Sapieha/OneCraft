#import libraries
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random


noise = PerlinNoise(octaves=3, seed=random.randint(1, 9999))

#create an instance of the ursina app
app = Ursina()

#define game variables
selected_item = "grass"
dev_mode = False
cb = 0

#create player
player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100),
    position=(0, 5, 0)
)

# Define textures and models for blocks and items
textures = {
  "grass": load_texture("assets/textures/groundEarth.png"),
  "dirt": load_texture("assets/textures/groundMud.png"),
  "stone": load_texture("assets/textures/wallStone.png"),
  "bedrock": load_texture("assets/textures/stone07.png"),
  "barrier": load_texture("assets/textures/barrier01.png")
}

models = {
  "block": "assets/models/block_model",
  "poppy": "assets/models/poppy_model"
}

def distance_xz(pos1, pos2):
    return ((pos1.x - pos2.x) ** 2 + (pos1.z - pos2.z) ** 2) ** 0.5

class Block(Entity):
  def __init__(self, position, item_type, model_type="block"):
    # Apply a slight offset for specific items
    y_offset = -0.50 if item_type == "poppy" else 0
    
    super().__init__(
        position=(position[0], position[1] + y_offset, position[2]),
        model=models.get(model_type, models["block"]),
        scale=1,
        origin_y=-0.5,
        texture=textures.get(item_type),
        collider="box"
    )
    self.item_type = item_type

mini_item = Entity(
  parent=camera,
  model=models.get("block"),
  scale=0.2,
  texture=textures.get(selected_item),
  position=(0.35, -0.25, 0.5),
  rotation=(-15, -30, -5)
)

#create the ground
min_height = -10
for x in range(-10, 10):
  for z in range(-10, 10):
    height = noise([x * 0.02, z * 0.02])
    height = math.floor(height * 7.5)
    for y in range(height, min_height - 1, -1):
      if y == min_height:
        block = Block((x, y + min_height, z), "bedrock")
      elif y == height:
        block = Block((x, y + min_height, z), "grass")
      elif height - y > 2:
        block = Block((x, y + min_height, z), "stone")
      else:
        block = Block((x, y + min_height, z), "dirt")

def input(key):
  global selected_item
  #place item
  if key == "right mouse down":
    hit_info = raycast(camera.world_position, camera.forward, distance=10)
    if hit_info.hit:
      if selected_item == "poppy":
        if not mouse.hovered_entity.item_type == "bedrock"  and not mouse.hovered_entity.item_type == "barrier":
          block = Block(hit_info.entity.position + hit_info.normal, selected_item, model_type="poppy")
      else:
        block = Block(hit_info.entity.position + hit_info.normal, selected_item)
  #grab item
  if key == "middle mouse down":
    if dev_mode:
      selected_item = mouse.hovered_entity.item_type
    else:
      if not mouse.hovered_entity.item_type == "bedrock" and not mouse.hovered_entity.item_type == "barrier":
        selected_item = mouse.hovered_entity.item_type
  #delete block
  if key == "left mouse down" and mouse.hovered_entity:
    if cb == "1":
       destroy(mouse.hovered_entity)
    else:
      if not mouse.hovered_entity.item_type == "bedrock" and not mouse.hovered_entity.item_type == "barrier":
         destroy(mouse.hovered_entity)
        
  #change item type
  if key == "1":
    selected_item = "grass"
  if key == "2":
    selected_item = "dirt"
  if key == "3":
    selected_item = "stone"
  if key == "4":
    if dev_mode:
      selected_item = "barrier"
  if key == "5":
     if dev_mode:
        selected_item = "bedrock"
  if key == "6":
     selected_item = "poppy"

def update():
  # Change the mini item model and texture based on the selected item
  if selected_item == "poppy":
    mini_item.model = models.get("poppy")
  else:
    mini_item.model = models.get("block")
  mini_item.texture = textures.get(selected_item)

#run the app
app.run()
