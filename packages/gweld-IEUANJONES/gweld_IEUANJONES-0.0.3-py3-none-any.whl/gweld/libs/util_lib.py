import math

def calculate_y_scale(data, tick_count=5):
    # Algorithm from: https://stackoverflow.com/a/326746
    lower_bound = 0 # No support for negative numbers.... yet
    upper_bound = data.max
    data_range = upper_bound - lower_bound
    coarse_tick_size = data_range / (tick_count-1)
    magnitude = math.ceil(math.log(coarse_tick_size, 10)) # Yay floating point arithmetic!

    for tick_size in [0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1]:
        if coarse_tick_size/10**magnitude <= tick_size:
            tick_size *= 10**magnitude
            break

    if not tick_size % 1:
        tick_size = int(tick_size)

    scale = [0]
    while tick_count-1 > 0:
        scale.append(round(scale[-1]+tick_size, 3))

        if scale[-1] > upper_bound:
            break
        tick_count -= 1

    return scale

def calculate_margins(vis):
    # Left, Top, Right, Bottom
    return (
        vis.style.width * vis.style.margin[0],
        vis.style.width * vis.style.margin[2],
        vis.style.height * vis.style.margin[1],
        vis.style.height * vis.style.margin[3]
    )

def calculate_chart_size(vis, margins):
    width = vis.style.width - margins[0] - margins[2]
    height = vis.style.height - margins[1] - margins[3]

    return (width, height)
