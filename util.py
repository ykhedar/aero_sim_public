from matplotlib.patches import Rectangle


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


# hier a function will be implemented to predict if the crane move away in defined time
def is_wait(drone_, crane_, time, wait_time):
    crane_patch = Rectangle((crane_.get_location(time + wait_time), 0), crane_.width, crane_.length, angle=0, lw=1,
                            ec='b', fc='#6699ff')
    if wait_time <= 0:
        return False
    return not detect_overlap(drone_.get_vis_patch(), crane_patch)


# this function will return if the cranes still stop at slots
def is_in_slots(cranes, slots_list):
    for crane_ in cranes:
        for slot in slots_list:
            if detect_moving(crane_, slot):
                return True
    return False


# this function will detect if the crane move away the position of marked slots
def detect_moving(crane, slot):
    crane_xl, crane_xr = get_box_extent(crane)
    slot_xl = slot
    # 5 means the width of drone
    slot_xr = slot + 5
    if is_a_between(slot_xl, crane_xl, crane_xr) or is_a_between(slot_xr, crane_xl, crane_xr):
        return False
    return True


def is_drone_meet_slot(drone_, slot):
    slot_xl, slot_xr = slot, slot + drone_.get_width()
    drone_xl, drone_xr = get_box_extent(drone_)
    a = is_a_between(slot_xl, drone_xl, drone_xr) or is_a_between(slot_xr, drone_xl, drone_xr)
    b = is_a_between(drone_xl, slot_xl, slot_xr) or is_a_between(drone_xr, slot_xl, slot_xr)
    return a or b
