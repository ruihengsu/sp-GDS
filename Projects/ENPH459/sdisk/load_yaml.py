import yaml

try: 
    with open("params.yaml", "r") as f:
        p = yaml.safe_load(f)
    
    l_inner = p["l_inner"]
    l_outer = p["l_outer"]
    w_meander = p["w_meander"]
    thick = p["thick"]
    pitch = p["pitch"]
    n = p["n"]
    outer_r = p["outer_r"]
    thetas = p["thetas"]

except Exception as e: 
    print("Error opening yaml file. using defaults")
    l_inner = 40
    l_outer = 10
    w_meander = 10
    thick = 5
    pitch = thick + 5
    n = 8
    outer_r = 200
    thetas = [0, 90, 270]