cpm = False
jumping = False
crouched = True
# contain heights within range
min_z = 100
max_z = 215.8
# z coordinates of ob ground and water
ground_z = -735.875
water_surface_z = -648
# if using sample poses
x, y, pitch, yaw = 1776.875, -2472.875, 79, 90

# Fixed vars
crouch_offset = 14 if crouched else 0
water_friction = 0.5 if cpm else 1.0
gravity = 800
frame_time = 0.008


def apply_water_friction(pos, vel):
    if pos <= water_surface_z - 1:  # origin - 23u
        water_level = 1
    if pos <= water_surface_z - 25 + crouch_offset/2:  # origin + 1u
        water_level = 2
    if pos <= water_surface_z - 50 + crouch_offset:  # origin + 26u
        water_level = 3

    try:
        drop = vel * water_friction * water_level * frame_time
    except NameError:
        raise "Water friction requested, but no valid water level could be found."

    new_vel = vel - drop
    if -new_vel < 0:
        new_vel = 0
    return new_vel, water_level


def calculate_final_z(pos, vel, water_surface_z):
    water_level = 0
    while True:
        if pos <= water_surface_z - 1:
            vel, water_level = apply_water_friction(pos, vel)

        if water_level > 1:
            next_vel = vel
            next_pos = pos + frame_time * next_vel
        else:
            next_vel = vel - gravity * frame_time
            next_pos = pos + frame_time * 0.5 * (next_vel + vel)

        if next_pos < ground_z:
            return pos, vel
        else:
            vel, pos = round(next_vel), next_pos
            continue


if __name__ == "__main__":
    curr_pos = min_z

    while curr_pos < max_z:
        vel = -270 if jumping else 0
        z_final, vel_final = calculate_final_z(curr_pos, vel, water_surface_z)
        if ground_z < z_final < ground_z + .25:
            print(f"{'CPM' if cpm else 'VQ3'} {'J' if jumping else 'G'} ob at: {curr_pos}")
            print(f"sample pos: /placeplayer {x} {y} {curr_pos} {pitch} {yaw} 0.000000 0.000000 0.000000 {vel} ")
        curr_pos += 0.25
