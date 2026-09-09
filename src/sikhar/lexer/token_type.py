"""
Sikhar Token Types
Enumeration of all token types in Sikhar.
"""

from enum import Enum, auto


class TokenType(Enum):
    # Literals
    NUMBER = auto()      # 10, 42
    DECIMAL = auto()     # 3.14, 99.50
    TEXT = auto()        # "Hello, world!"
    BOOLEAN = auto()     # sacho, jutho
    NULL = auto()        # khali

    # Identifiers
    IDENTIFIER = auto()  # x, naam, age

    # Keywords - Variables & Values
    RAKHA = auto()       # rakha
    BADLA = auto()       # badla
    STHAYI = auto()      # sthayi
    KHALI = auto()       # khali
    SACHO = auto()       # sacho
    JUTHO = auto()       # jutho

    # Keywords - Input / Output
    DEKHA = auto()       # dekha
    SODHA = auto()       # sodha

    # Keywords - Conditions
    YADI = auto()        # yadi
    ATHAWA = auto()      # athawa
    NATRA = auto()       # natra

    # Keywords - Loops
    JABA = auto()        # jaba
    KO_LAGI = auto()     # ko_lagi
    MA = auto()          # ma (for loop iterator: ko_lagi x ma items)
    ROK = auto()         # rok (break)
    JAARI = auto()       # jaari (continue)

    # Keywords - Functions
    KAAM = auto()        # kaam
    FARKA = auto()       # farka

    # Keywords - Error Handling
    KOSHISH = auto()     # koshish (try)
    SAMATA = auto()      # samata (catch)
    FAL = auto()         # fal (throw)

    # Reserved Keywords for Future (Modules, OOP, Async, File, Control)
    AAYAAT = auto()      # aayaat (import)
    PATHAAU = auto()     # pathaau (export)
    VARG = auto()        # varg (class)
    NIRMAAN = auto()     # nirmaan (constructor)
    GUN = auto()         # gun (property)
    YO = auto()          # yo (this)
    SARBAJANIK = auto()  # sarbajanik (public)
    GOPYA = auto()       # gopya (private)
    PARKHA = auto()      # parkha (await)
    SANGAI = auto()      # sangai (async)
    KHOLA = auto()       # khola (open)
    BANDA = auto()       # banda (close)
    PADH = auto()        # padh (read)
    LEKH = auto()        # lekh (write)
    JOD = auto()         # jod (add)
    HATAU = auto()       # hatau / hatāu (remove)
    KHOJ = auto()        # khoj (find)
    PRAKAAR = auto()     # prakaar (type)
    JAACH = auto()       # jaach (check)
    SURUWAT = auto()     # suruwat (start)
    SAMAPTA = auto()     # samapta (end)

    # Operators - Arithmetic
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    PERCENT = auto()     # %

    # Operators - Comparison
    EQUAL_EQUAL = auto() # ==
    BANG_EQUAL = auto()  # !=
    LESS = auto()        # <
    LESS_EQUAL = auto()  # <=
    GREATER = auto()     # >
    GREATER_EQUAL = auto()# >=

    # Operators - Logical
    AND = auto()         # and
    OR = auto()          # or
    NOT = auto()         # not

    # Operators - Assignment
    EQUAL = auto()       # =

    # Delimiters and Punctuation
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,
    COLON = auto()       # :
    SEMICOLON = auto()   # ;
    DOT = auto()         # .

    # Control / Structural
    NEWLINE = auto()     # '\n'
    EOF = auto()         # End of file


KEYWORDS = {
    # Implemented v0.1 keywords
    "rakha": TokenType.RAKHA,
    "badla": TokenType.BADLA,
    "sthayi": TokenType.STHAYI,
    "khali": TokenType.KHALI,
    "sacho": TokenType.SACHO,
    "jutho": TokenType.JUTHO,
    "dekha": TokenType.DEKHA,
    "sodha": TokenType.SODHA,
    "yadi": TokenType.YADI,
    "athawa": TokenType.ATHAWA,
    "natra": TokenType.NATRA,
    "jaba": TokenType.JABA,
    "ko_lagi": TokenType.KO_LAGI,
    "ma": TokenType.MA,
    "rok": TokenType.ROK,
    "jaari": TokenType.JAARI,
    "kaam": TokenType.KAAM,
    "farka": TokenType.FARKA,
    "koshish": TokenType.KOSHISH,
    "samata": TokenType.SAMATA,
    "fal": TokenType.FAL,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,

    # Reserved keywords
    "aayaat": TokenType.AAYAAT,
    "pathaau": TokenType.PATHAAU,
    "varg": TokenType.VARG,
    "nirmaan": TokenType.NIRMAAN,
    "gun": TokenType.GUN,
    "yo": TokenType.YO,
    "sarbajanik": TokenType.SARBAJANIK,
    "gopya": TokenType.GOPYA,
    "parkha": TokenType.PARKHA,
    "sangai": TokenType.SANGAI,
    "hatau": TokenType.HATAU,
    "hatāu": TokenType.HATAU,
    "khoj": TokenType.KHOJ,
    "prakaar": TokenType.PRAKAAR,
    "jaach": TokenType.JAACH,
    "suruwat": TokenType.SURUWAT,
    "samapta": TokenType.SAMAPTA,
}

RESERVED_FUTURE_KEYWORDS = {
    TokenType.VARG: "Classes (varg) are reserved for future OOP support.",
    TokenType.NIRMAAN: "Constructors (nirmaan) are reserved for future OOP support.",
    TokenType.GUN: "Properties (gun) are reserved for future OOP support.",
    TokenType.YO: "Self/This (yo) is reserved for future OOP support.",
    TokenType.SARBAJANIK: "Access modifier (sarbajanik) is reserved for future versions.",
    TokenType.GOPYA: "Access modifier (gopya) is reserved for future versions.",
    TokenType.PARKHA: "Async/await (parkha) is reserved for future versions.",
    TokenType.SANGAI: "Async/await (sangai) is reserved for future versions.",
    TokenType.HATAU: "Collection remove (hatau) is reserved for future syntax.",
    TokenType.KHOJ: "Collection search (khoj) is reserved for future syntax.",
    TokenType.PRAKAAR: "Explicit type checking (prakaar) is reserved for future versions.",
    TokenType.SURUWAT: "Entry point (suruwat) is reserved for future versions.",
    TokenType.SAMAPTA: "Program termination (samapta) is reserved for future versions.",
}
