# Duckman Rewritten

The [Duckman Community Bot](https://github.com/Grewoss/duckman-python_bot) rewritten in Python using the [discord.py command ext](https://discordpy.readthedocs.io/en/rewrite/ext/commands/index.html).

## Getting Started

Placeholder

## Creating Embeds with .YAML

If you want to create an Embed for the Chat please use the `generateEmbed` function from `src/embeds.py` and follow the Rules in `embeds/default.yml`!  
`default.yml` file:
```yml
header:
  title: Header_name_here
  description: description_here # Muss da sein kann aber leer bleiben
  url: url_here # Wenn keine URL gebraucht wird "https://gwo.io" benutzen

fields:
  1:
    title: title_here
    description: description_here
  2:
    title: title_here
    description: description_here
  # Hier koennen beliebig viele fields hin.

# Footer ist optional.
footer: footer_here

# Color ist optional.
color: 0xb02fbc
# show_thumbnail ist auch optional und ist wenn nicht angegeben False!
show_thumbnail: False
```

## Requirements

* [Discord.py](https://github.com/Rapptz/discord.py/tree/rewrite)
* [PyMongo](https://api.mongodb.com/python/current/installation.html)

## Contributing

placeholder

## Authors

* [**Grewoss**](https://github.com/Grewoss)

See also the list of [contributors](https://github.com/Grewoss/duckman_rewrite/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details