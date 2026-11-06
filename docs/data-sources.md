# Data sources (layered)

| Layer | Source | Gives | Status / license notes |
|---|---|---|---|
| Works + authors | Shamela (authorized) | titles, authors, categories, text | check what the authorization covers |
| Works + authors | OpenITI / KITAB (GitHub, Zenodo) | metadata TSV/JSON: titles, authors, death dates | open corpus; premodern texts only, no covers |
| Free modern books | Hindawi corpus (CC BY 4.0 version) | metadata + text | free ebooks, not for resale as products |
| Editions + covers | Your supplier / publisher | ISBN, price, cover photos | the only source matching what you can really sell |
| Editions + covers (fallback) | Google Books API, Open Library (by ISBN) | metadata, thumbnails | read each service's terms before storing images; Arabic coverage uneven |
| Missing covers | Generated typographic cover | consistent style, works in 3D | built by the project itself |

Rules: every imported row keeps source name + source URL + fetch date. AI-research findings go to `data/review/` first.
