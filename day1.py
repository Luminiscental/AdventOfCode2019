"""
AdventOfCode2019 - Day 1
"""


def fuel_from_mass1(mass):
    """
    Calculate the required fuel for a module based on its mass.
    """
    return mass // 3 - 2


def fuel_from_mass2(mass):
    """
    Calculate the required fuel for a module
    """
    result = 0
    fuel = fuel_from_mass1(mass)

    while fuel > 0:
        result = result + fuel
        fuel = fuel_from_mass1(fuel)

    return result


def run():
    """
    Solve and display the answer.
    """
    masses = [int(line) for line in PUZZLE_INPUT.splitlines()]
    fuel1 = sum(fuel_from_mass1(mass) for mass in masses)
    fuel2 = sum(fuel_from_mass2(mass) for mass in masses)
    print(f"part1: {fuel1}")
    print(f"part2: {fuel2}")


if __name__ == "__main__":
    run()

PUZZLE_INPUT = """128398
118177
139790
84818
75859
139920
90212
74975
120844
85533
77851
127044
128094
77724
81951
115804
60506
65055
52549
108749
92367
53974
52896
66403
93539
118392
78768
128172
85643
109508
104742
71305
84558
68640
58328
58404
70131
73745
149553
57511
119045
90210
129537
114869
113353
114181
130737
134877
90983
84361
62750
114532
139233
139804
130391
144731
84309
137050
79866
121266
93502
132060
109190
61326
58826
129305
141059
143017
56552
102142
110604
136052
93872
71951
72954
70701
137381
76580
62535
62666
126366
66361
109076
126230
73367
94459
126314
133327
143771
50752
75607
117606
142366
59068
75574
149836
57058
77622
83276
82734"""
