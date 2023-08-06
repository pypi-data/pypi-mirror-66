# wikt-cli

## Installation

- From pypi: `pip install wikt-cli`

- From source: clone this repo, `cd` into it, run `python setup.py bdist_wheel`, `pip install dist/wikt_cli-{VERSION}-py3-none-any.whl` with proper permission and/or destination.

## Usage

`wikt <word> [--no-color] [-d]`

## Example output

The output of `wikt meta --no-color` is:

```
Etymology:
    From meta-, back-formed from metaphysics.

    Definitions:
        (adjective) meta (comparative more meta, superlative most meta) (informal)
        Self-referential; structured analogously, but at a higher level.

Etymology:
    From Latin mēta.

    Definitions:
        (noun) meta (plural metas) Boundary marker. Either of the conical columns at
        each end of a Roman circus.

Etymology:
    Clipping of metagame.

    Definitions:
        (noun) meta (plural metas) (video games) Metagame; the most effective tactics
        and strategies used in a competitive video game.

        (adjective) meta (comparative more meta, superlative most meta) (video games)
        Prominent in the metagame; effective and frequently used in competitive
        gameplay.

Etymology:
    Clipping of metaoidioplasty.

    Definitions:
        (noun) meta (plural metas) (informal) Metoidioplasty.
```

## Contributing

1. Using `git.sr.ht`, you don't need an account to contribute! Send "issues" to the mailing list `~fkfd/wikt@lists.sr.ht` (remember to use plaintext, not HTML), and "pull/merge requests" as a patch (see [git-send-email](https://git-send-email.io) and [sourcehut mailing list wiki](https://man.sr.ht/lists.sr.ht/)).

2. Can't use a mailing list? A web mirror is available at [this codeberg repo](https://codeberg.org/fakefred/wikt-cli).