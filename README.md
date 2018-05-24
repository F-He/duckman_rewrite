# Duckman Rewritten

The [Duckman Community Bot](https://github.com/Grewoss/duckman-python_bot) rewritten in Python using the [discord.py command ext](https://discordpy.readthedocs.io/en/rewrite/ext/commands/index.html).

Duckman is a community bot created for the [Grewoss Discord Server](https://discord.gg/XW3a27Z)!  
You are free to fork and do basicly anythings with this Repo but keep the [License](https://github.com/Grewoss/duckman_rewrite/blob/master/LICENSE) in mind.  
I would appreciate if you send me a message on Discord if you use this code so i can check out your Version!

## Getting Started

Placeholder

## Contributing

placeholder

## Requirements

* [Discord.py](https://github.com/Rapptz/discord.py/tree/rewrite)
* [neo2py](https://github.com/technige/py2neo)

## Creating Embeds with .YAML

If you want to create an Embed for the Chat please use the `generateEmbed` function from `src/embeds.py` and follow the Rules in `embeds/default.yml`!  
`default.yml` file:
```yml
header:
  title: Header_name_here
  description: description_here # Needs to be here but can be empty.
  url: url_here # If you don't wan't to add a custom URL add "https://gwo.io".

fields:
  1:
    title: title_here
    description: description_here
  2:
    title: title_here
    description: description_here
  # There can be as many fields as you wan't/need.

# Footer is optional.
footer: footer_here

# Color is optional.
color: 0xb02fbc
# show_thumbnail is also optional and if not given False!
show_thumbnail: False
```


## Authors

* [**Grewoss**](https://github.com/Grewoss)

See also the list of [contributors](https://github.com/Grewoss/duckman_rewrite/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details