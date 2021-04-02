# arXiv-dl

Command-line [arXiv.org](https://arxiv.org/) Papers Downloader

-   Powered by [arXiv API](https://arxiv.org/help/api/user-manual) and [Papers with code](https://paperswithcode.com/)
-   [Source Code](https://github.com/MarkHershey/arxiv-dl)
-   [Python Package Index (PyPI)](https://pypi.org/project/arxiv-dl/)

## Features

This is a command-line tool, you just need to use `Python3`'s `pip` to install the package, then, you will be able to use the following commands in your shell/terminal.

### Commands

**`add-paper` will do**

-   Download paper named `[id]_[title].pdf` into destination folder.
-   Maintain a papers list named `000_Paper_List.json` in the destination folder.
-   Extract paper metadata, like `title`, `authors`, `abstract`, `bibtex`, `code`, and write them into a new MarkDown document named `[id]__Notes.md` in the destination folder.

**`dl-paper` will do**

-   Download paper `[id]_[title].pdf` into destination folder.

### Supported URLs

-   URLs from `arXiv.org` Only
    -   Paper's abstract page `https://arxiv.org/abs/xxxx.xxxxx`
    -   or Paper's PDF page `https://arxiv.org/pdf/xxxx.xxxxx.pdf`

## Usage

To install

```bash
$ pip install --upgrade arxiv-dl
```

To download paper

```bash
$ add-paper "URL"
```

or

```bash
$ dl-paper "URL"
```

Usage Example:

```bash
$ add-paper https://arxiv.org/abs/1512.03385
```

## Configuration (Optional)

Set Custom Download Destination Folder _(Optional)_

-   Let's say you want your papers get downloaded into `~/Documents/Papers`.
-   Make sure the folder `~/Documents/Papers` exists.
-   Set the environment variable `ARXIV_DOWNLOAD_FOLDER` to your desired location.
    ```bash
    $ export ARXIV_DOWNLOAD_FOLDER=~/Documents/Papers
    ```
-   If the environment variable is not set, paper will be downloaded into the default Download Destination `~/Downloads/ArXiv_Papers`.

## License

[MIT License](LICENSE) - Copyright (c) 2021 Mark Huang
