# Duckman Rewritten

The [Duckman Community Bot](https://github.com/Grewoss/duckman-python_bot) rewritten in Python using the [discord.py command ext](https://discordpy.readthedocs.io/en/rewrite/ext/commands/index.html).

Duckman is a community bot created for the [Grewoss Discord Server](https://discord.gg/XW3a27Z)!  
You are free to fork and do basically anythings with this Repository, but keep the [License](https://github.com/Grewoss/duckman_rewrite/blob/master/LICENSE) in mind.  
I would appreciate if you send me a message on Discord if you use this code so i can check out your Version!

## Getting Started

Placeholder

## Contributing

Placeholder

## Requirements

* [Discord.py](https://github.com/Rapptz/discord.py/tree/rewrite)
* [neo2py](https://github.com/technige/py2neo)

## Adding a Command to the Help File(Command)

Placeholder

## Creating Embeds with .json

If you want to create an Embed for the Chat please use the `generateEmbed` function from `src/embeds.py` and follow the Rules in `embeds/default.json`!  
`default.json` file:
```json
{
    "header": {
        "title": "Header name here",
        "description": "Description here",
        "url": null
    },

    "fields": {
        "1": {
            "title": "Title here",
            "description": "Description here"
        },
        "2": {
            "title": "Title here",
            "description": "Description here"
        }
    },

    "footer": "The Footer is optional",
    "color": "0xb02fbc",
    "show_thumbnail": true
}
```


## Authors

* [**Grewoss**](https://github.com/Grewoss)

See also the list of [contributors](https://github.com/Grewoss/duckman_rewrite/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
