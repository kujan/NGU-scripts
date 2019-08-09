from collections import namedtuple
Wish = namedtuple("Wish", "id name levels divider")
WISH_ORDER = [
              Wish(1, "I wish that wishes kicked ass", 1, 1e15),
              Wish(2, "I wish that wishes weren't so slow :c", 10, 1e15),
              Wish(3, "I wish MacGuffin drops mattered", 5, 2e15),
              Wish(7, "I wish I was stronger in Adventure mode I", 10, 3e15),
              Wish(16, "I wish I had more Resource 3 Power I", 10, 5e15),
              Wish(17, "I wish I had more Resource 3 Cap I ", 10, 5e15),
              Wish(10, "I wish I had more Energy Power I", 10, 5e15),
              Wish(11, "I wish I had more Energy Cap I", 10, 5e15),
              Wish(13, "I wish I had more Magic Power I", 10, 5e15),
              Wish(14, "I wish I had more Magic Cap I", 10, 5e15),
              Wish(18, "I wish I had more Resource 3 Bars I", 10, 5e15),
              Wish(5, "I wish money pit didn't suck", 10, 6e15),
              Wish(6, " I wish I could beat up more bosses I", 10, 3e15),
             ]

# skips: 6, 8