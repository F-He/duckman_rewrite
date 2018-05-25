import yaml

x = 0
differenz = 100
level_dict = {}

for i in range(0, 51):
    if i == 0:
        continue
    print(f"{i} == {x} xp")
    level_dict[i] = {"xp": x, "rewards": None}

    x += differenz
    differenz += 100



with open("cfg/level.yml", 'w', encoding='utf-8') as stream:
            yaml.dump(level_dict, stream, default_flow_style=False)


while True:
    pass