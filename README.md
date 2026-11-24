# postcard-maker

A reusable Agent Skill that turns any photo into a stylized 800x600 postcard with a Gaussian-blurred backdrop, centered sharp foreground, black bottom caption bar, and custom title text using Python Pillow.

## Structure

```text
postcard-maker/
├── SKILL.md
├── README.md
└── scripts/
    └── make_postcard.py
```

## Quick Start

```bash
pip install pillow
python3 scripts/make_postcard.py --input photo.png --output postcard.jpg --text "Aespa Winter" --color violet
```
