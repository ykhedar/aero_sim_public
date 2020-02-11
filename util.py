def get_box_extent(box):
    x_bl, y_bl = box.xy
    x_br, y_br = (x_bl + box.get_width()), y_bl
    return [x_bl, x_br]


def detect_overlap(drone_, crane_):
    drone_xl, drone_xr = get_box_extent(drone_)
    crane_xl, crane_xr = get_box_extent(crane_)

    a = is_a_between(drone_xl, crane_xl, crane_xr) or is_a_between(drone_xr, crane_xl, crane_xr)
    b = is_a_between(crane_xl, drone_xl, drone_xr) or is_a_between(crane_xr, drone_xl, drone_xr)
    return a or b


def is_a_between(a, b, c):
    return b < a < c
