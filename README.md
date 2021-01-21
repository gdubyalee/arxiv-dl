# arXiv-dl 

Command-line [arXiv.org](https://arxiv.org/) Papers Downloader

- [Source Code](https://github.com/MarkHershey/arxiv-dl)
- [Python Package Index (PyPI)](https://pypi.org/project/arxiv-dl/)

## Installation 

- Require `Python 3.x`

```bash
pip install --upgrade arxiv-dl
```

## Configuration 

Set Custom Download Destination *(Optional)*

- Let's say you want your papers get downloaded into `~/Documents/Papers`.
- First, make sure the directory `~/Documents/Papers` exists.
- Then, set the environment variable `ARXIV_DOWNLOAD_FOLDER`:
    ```bash
    export ARXIV_DOWNLOAD_FOLDER=~/Documents/Papers
    ```
- If the environment variable is not set, paper will be downloaded into Default Download Destination (`~/Downloads/ArXiv_Papers`)

## Usage

Type in command line:

```bash
add-paper "URL"
```

or

```bash
dl-paper "URL"
```

Usage Example:

```bash
add-paper https://arxiv.org/abs/1512.03385
```

## Features

### Commands

**`add-paper` will do**

- Download paper named `[id]_[title].pdf` into destination folder.
- Maintain a papers list named `000_Paper_List.json` in the destination folder.
- Create a new MarkDown document named `[id]_Notes.md` in the destination folder. (for adding your personal paper reading notes)

**`dl-paper` will do**

- Download paper `[id]_[title].pdf` into destination folder.

### Supported URLs

- URLs from `arXiv.org` Only
    - Paper's abstract page `https://arxiv.org/abs/xxxx.xxxxx` 
    - or Paper's PDF URL `https://arxiv.org/pdf/xxxx.xxxxx.pdf`

## License

[MIT License](LICENSE) - Copyright (c) 2021 Mark Huang
