a = "Starting:"
b = "Starting:"

c = "This run: 3.23K"
d = "This run: 0"

e = "Current:"
f = "Current:"

g = "Per hour:"
h = "Per hour:"

i = "Total Runtime: 0:00:34 "


aa = "44.9K"
bb = "74.3K"
cc = "3.23K"
dd = "56.7K"
ee = "48.1K"
ff = "776M"
gg = "30.56M"
hh = "12.34K"
print("\n{0:^40}\n".format("0:02:55"))
print("{0:{fill}{align}40}".format(" # 1 ", fill="-", align="^"))
print("{0:{fill}{align}40}".format(" # 10 ", fill="-", align="^"))
print("{0:{fill}{align}40}".format(" # 100 ", fill="-", align="^"))
print("{0:{fill}{align}40}".format(" # 1000 ", fill="-", align="^"))
print("{0:{fill}{align}40}".format(" # 10000", fill="-", align="^"))
print("{0:{fill}{align}40}".format(" # 100000 ", fill="-", align="^"))
print("{0:{fill}{align}40}".format(" # 1000000 ", fill="-", align="^"))
print("{:^18}{:^3}{:^18}".format("XP", "|", "PP"))
print("Starting: {:^8}{:^3}Starting: {:^8}".format(aa, "|", bb))
print("This run: {:^8}{:^3}This run: {:^8}".format(cc, "|", dd))
print("Current:  {:^8}{:^3}Current: {:^8}".format(ee, "|", ff))
print("Per hour: {:^8}{:^3}Per hour: {:^8}".format(gg, "|", hh))
print("\n{}".format(i))

def get_inventory_slots(slots):
    """Get coords for inventory slots from 1 to slots"""
    i = 1
    row = 1
    x_pos = 300
    y_pos = 330
    coords = []

    while i <= slots:
        x = x_pos + (i - (12 * (row - 1))) * 50
        y = y_pos + ((row - 1) * 50)
        coords.append((x, y))
        if i % 12 == 0:
            row += 1
        i += 1
    return coords

print(get_slots(12))
