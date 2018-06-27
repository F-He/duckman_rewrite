import yaml

x = 0
differenz = 100 # I'd suggest English variable names.
level_dict = {}

for i in range(0, 51):
    if i == 0:
        continue
    print(f"{i} == {x} xp")
    level_dict[i] = {"xp": x, "rewards": "20 Coins!", "coins": 20}

    x += differenz
    differenz += 100



with open("cfg/level2.yml", 'w', encoding='utf-8') as stream:
            yaml.dump(level_dict, stream, default_flow_style=False)


while True:
    pass
