from openalea.plantgl.all import NurbsCurve, Vector3, Point2Array, Point3Array, Polyline2D, BezierCurve2D
from openalea.lpy import Lsystem, newmodule
from random import uniform, seed
from numpy import linspace, pi, sin, cos


def amplitude(x): return 2

def cut_from(pruning_id, s, path = None):
    """Check cut_string_from_manipulation for manual implementation"""
    s.insertAt(pruning_id, newmodule('F'))
    s.insertAt(pruning_id+1, newmodule('%'))
    return s

def cut_using_string_manipulation(pruning_id, s, path = None):
  """Cuts starting from index pruning_id until branch 
        end signified by ']' or the entire subtrees if pruning_id starts from leader"""
  bracket_balance = 0
  cut_num = pruning_id
  #s[cut_num].append("no cut")
  cut_num += 1
  pruning_id +=1
  total_length = len(s)
  while(pruning_id < total_length):
      if s[cut_num].name == '[':
          bracket_balance+=1
      if s[cut_num].name == ']':
          if bracket_balance == 0:
              break
          else:
              bracket_balance-=1
      del s[cut_num]
      pruning_id+=1             # Insert new node cut at the end of cut
  if path != None:
      new_lsystem = Lsystem(path) #Figure out to include time in this
      new_lsystem.axiom = s
      return new_lsystem
  #s.insertAt(cut_num, newmodule("I(1, 0.05)"))
  return s

def pruning_strategy(it, lstring):
  if((it+1)%8 != 0):  
    return lstring
  cut = False
  curr = 0
  while curr < len(lstring):
    if lstring[curr] == '/':
      if not (angle_between(lstring[curr].args[0], 0, 50) or angle_between(lstring[curr].args[0], 130, 180)):
        if(len(lstring[curr].args) > 1):
          if lstring[curr].args[1] == "no cut":
            curr+=1
            continue
        
        print("Cutting", curr, lstring[curr], (lstring[curr].args[0]+180))
        #lstring[curr].append("no cut")
        lstring = cut_from(curr+1, lstring)
    elif lstring[curr] == '&':
      if not (angle_between(lstring[curr].args[0], 0, 50) or angle_between(lstring[curr].args[0], 130, 180)):
        if(len(lstring[curr].args) > 1):
          if lstring[curr].args[1] == "no cut":
            curr+=1
            continue
        print("Cutting", curr, lstring[curr], (lstring[curr].args[0]+180))
        #lstring[curr].append("no cut")
        lstring = cut_from(curr+1, lstring)
    curr+=1
  
  return lstring

def angle_between(angle, min, max):
  angle = (angle+90)
  if angle > min and angle < max:
    return True
  return False
  
def myrandom(radius): 
    return uniform(-radius,radius)

def gen_noise_branch(radius,nbp=20):
    return  NurbsCurve([(0,0,0,1),(0,0,1/float(nbp-1),1)]+[(myrandom(radius*amplitude(pt/float(nbp-1))),
                                     myrandom(radius*amplitude(pt/float(nbp-1))),
                                     pt/float(nbp-1),1) for pt in range(2,nbp)],
                        degree=min(nbp-1,3),stride=nbp*100)

def create_noisy_circle_curve(radius, noise_factor, num_points=100, seed=None):
  if seed is not None:
      seed(seed)
  t = linspace(0, 2 * pi, num_points, endpoint=False)
  points = []
  s_texture = []
  for angle in t:
      # Base circle points
      x = radius * cos(angle)
      y = radius * sin(angle)

      # Need to create texture coordinates
      # texture coordinate is theta/360* 
      s = t / (2 * pi) 
      
      # Add noise
      noise_x = uniform(-noise_factor, noise_factor)
      noise_y = uniform(-noise_factor, noise_factor)
      
      noisy_x = x + noise_x
      noisy_y = y + noise_y
      
      points.append((noisy_x, noisy_y))
      s_texture.append(s)
  
  # Ensure the curve is closed by adding the first point at the end
  points.append(points[0])
  s_texture.append(s_texture[0])
  
  # Create the PlantGL Point2Array and Polyline2D
  curve_points = Point2Array(points)
  curve = Polyline2D(curve_points)
  return curve

def create_bezier_curve(num_control_points=4, x_range=(0, 10), y_range=(-2, 2), seed_val=None):
    if seed_val is not None:
        seed(seed_val)  # Set the random seed for reproducibility
    # Generate progressive control points within the specified ranges
    control_points = []
    prev_x = uniform(x_range[0], x_range[1] / 4)
    for i in range(num_control_points):
        x = prev_x + uniform(0, (x_range[1] - prev_x) / (num_control_points - i))
        y = uniform(*y_range)
        control_points.append(Vector3(x, y, 0))  # Set z to 0 for 2D curve
        prev_x = x
    # Create a Point3Array from the control points
    control_points_array = Point3Array(control_points)
    # Create and return the BezierCurve2D object
    bezier_curve = BezierCurve2D(control_points_array)
    return bezier_curve