<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/flask-web%20framework-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/mongodb-database-47A248?style=for-the-badge&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/socket.io-realtime-010101?style=for-the-badge&logo=socket.io" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" />
</p>

<h1 align="center">🏪 Market Game</h1>

<p align="center">
  <strong>A multiplayer economic simulation where players run businesses, trade commodities across geographic markets, and dispatch convoys through a real-time networked world.</strong>
</p>

<p align="center">
  <em>Built at UC Santa Cruz · Summer 2019</em>
</p>

---

## The Idea

What happens when you give a group of people virtual businesses, three colored pigments, and a map of Bay Area cities — then let them loose?

**Market Game** is a multiplayer trading simulation built on Flask and MongoDB. Players assume the role of competing businesses spread across geographically distinct markets. They set their own buy and sell prices, dispatch convoys across physical distances (with real travel time), earn currency through mining and trivia, and spend their hard-earned pigments painting pixels on a shared collaborative canvas.

It's part economics experiment, part strategy game, part r/Place.

---

## How It Works

### The World

The simulation takes place across three markets, each positioned in 2D space:

```
                    San Francisco (-2, 7)
                    ├── Asic    ($200)
                    ├── Reebok  ($200)
                    └── Vans    ($200)


    Santa Cruz (5, 0)                     Redwood City (10, -8)
    ├── Nike   ($100)                     ├── Sketchers ($200)
    └── Adidas  ($77)                     └── Puma      ($200)
```

Each market has **local exports** — colored pigments (Red, Green, Blue) — and each business maintains independent **bid/ask prices** for every commodity. Trade only happens when two businesses are in the same market and their prices overlap.

### The Trading Engine

Transactions use a **midpoint price discovery** mechanism:

```
Settlement Price = (Buyer's Bid - Seller's Ask) / 2 + Seller's Ask
```

A trade executes when a buyer's bid meets or exceeds a seller's ask. The engine automatically negotiates the best price for both parties. If a seller doesn't have enough stock, the system gracefully scales down to available quantity.

```
#---- Nike ----#---- Red ----#---- Adidas ----#
Purchase succeeded between Nike to Adidas at $12.50 with 5 Red pigments.
```

### Convoys

The real magic. Players can't just teleport goods — they have to **physically move them**.

A convoy is a mobile trading unit dispatched from a business. It:
- Costs money to create (which determines its speed)
- Travels through 2D space using **Euclidean distance**
- Has a speed drawn from a **normal distribution** (min 0.5x, max 2.0x) — spending more money shifts the curve toward faster speeds
- Executes trades automatically upon arrival at the destination market
- Returns home with profits

```python
# Puma sends a convoy from Redwood City to Santa Cruz
convoy = puma.createConvoy(cost=70, money=30, quantity=5)
convoy.gotoMarket(santa_cruz, [(vans, 2), (nike, 3)])
# Convoy travels... arrives... trades... returns home
```

Travel is **asynchronous** — convoys move in real time using Python's `threading.Timer`. Try to trade with a convoy mid-transit and you'll get rejected: *"Wrong market; no sale."*

### The Oracle

Need quick cash? Visit the Oracle.

A YAML-powered quiz engine serves random trivia questions with variable rewards (1-5 creativity points). Get it right, earn currency. Topics range across:

- 🧮 Math puzzles (*"Divide 30 by ½ and add 10"*)
- 🌍 Geography (*"What ocean borders California?"*)
- 🧩 Word association (*"Cake, swiss, cottage → ???"*)
- 🎬 Disney trivia (*"In Aladdin, Rajah is the pet Tiger of whom?"*)
- 🤯 Logic riddles (*"A word I know, six letters it contains. Subtract just one, and twelve remains."*)

48 hand-crafted questions with flexible answer matching — case-insensitive strings, numeric tolerance, and multi-format responses.

### The Canvas

Every pixel costs pigment.

A **25×25 collaborative pixel canvas** rendered via Flask templates with **real-time updates over WebSocket**. Players select a pixel, mix RGB values from their pigment inventory, and paint. Socket.IO broadcasts every change to all connected clients instantly.

The economy feeds the art: you need to trade for pigments before you can paint. Red pigments from Santa Cruz, Green from San Francisco, Blue from Redwood City. Want purple? Better have trade routes to two markets.

---

## Architecture

```
market-game/
│
├── src/                        # Game Engine (~730 LOC)
│   ├── Market.py               # Geographic trading hubs with distance calculation
│   ├── Business.py             # Player-controlled entities with convoy dispatch
│   ├── Trader.py               # Transaction engine with price negotiation
│   ├── Commodity.py            # Tradeable goods (Red, Green, Blue pigments)
│   ├── Convoy.py               # Mobile traders with async travel simulation
│   ├── Saveable.py             # MongoDB ORM base class with upsert semantics
│   ├── db.py                   # Database config, P2P broadcast, user profiles
│   ├── net.py                  # Flask web server + Socket.IO + REST API
│   ├── build.py                # World initialization (markets, businesses, commodities)
│   ├── db_build.py             # Canvas grid initialization
│   ├── driver.py               # Demo scenario with convoy dispatches
│   │
│   ├── templates/
│   │   ├── canvas.html         # Collaborative pixel canvas with color mixing
│   │   └── market.html         # Market overview with business listings
│   │
│   └── static/
│       ├── canvas.js           # Pixel selection + real-time Socket.IO updates
│       ├── canvas.css           # Grid layout with hover glow effects
│       └── base.css            # Montserrat typography + flexbox layout
│
├── bin/                        # CLI Tools
│   ├── market <name>           # Inspect a market's businesses and exports
│   ├── business <name>         # View business inventory, prices, and balance
│   ├── transact <biz> <c> <n>  # Execute a trade with another business
│   ├── update buy|sell <p> <$> # Set your bid/ask prices
│   ├── mine <amount>           # Time-based wealth generation (RNG duration)
│   ├── oracle.py               # Trivia quiz for earning currency
│   └── oracle.yaml             # 48 questions with variable rewards
│
├── setup.py                    # Package config (v0.0.4, MIT License)
└── requirements.txt            # Python dependencies
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3, Flask, Flask-RESTful |
| **Database** | MongoDB (via PyMongo) |
| **Real-time** | Flask-SocketIO + Socket.IO client |
| **Transport** | HTTP POST broadcast + WebSocket |
| **Frontend** | Jinja2 templates, jQuery 3.4, vanilla CSS |
| **Networking** | IP-based player detection, multicast broadcast |
| **Randomness** | NumPy normal distribution (convoy speed) |

### Object Model

```
Saveable (MongoDB persistence)
├── Market
│   └── has many → Business
├── Commodity
│   └── produces → Stock (quantity + bid/ask prices)
└── Trader (transaction engine)
    ├── Business (extends Trader + Saveable)
    │   └── dispatches → Convoy
    └── Convoy (extends Trader)
        └── travels between Markets with async arrival
```

Every game entity inherits from `Saveable`, which provides MongoDB upsert persistence. A `Trader` handles all buy/sell logic. A `Business` is a `Trader` that lives in a `Market` and can dispatch `Convoy` units. A `Convoy` is a `Trader` that moves between markets in real time.

---

## Gameplay Loop

```
1. Register as a business          →  bin/setAccount Nike 112358
2. Check your market               →  bin/market "Santa Cruz"
3. Set competitive prices          →  bin/update buy Red 15
4. Trade with neighbors            →  bin/transact Adidas Red 5
5. Dispatch convoy to far market   →  (via driver.py or web UI)
6. Wait for convoy to arrive...    →  (real-time async travel)
7. Earn currency via Oracle        →  bin/oracle
8. Mine for resources              →  bin/mine 10 --repeat
9. Spend pigments on the canvas    →  http://localhost:2002/canvas
10. Repeat, optimize, dominate     →  📈
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/Tsangares/market.git
cd market

# Install
pip install -r requirements.txt

# Initialize the world (requires MongoDB connection)
cd market-game/src
python build.py        # Creates markets, businesses, commodities
python db_build.py     # Initializes the 25x25 pixel canvas

# Launch the server
python net.py          # Flask on 0.0.0.0:2002

# Open in browser
# http://localhost:2002/canvas    → Collaborative pixel canvas
# http://localhost:2002/market?name=Santa%20Cruz  → Market view
```

### CLI Tools

```bash
cd market-game/bin

python business Nike              # View Nike's inventory and prices
python market "San Francisco"     # View all businesses in a market
python oracle.py                  # Answer trivia for currency
python mine 10 --repeat           # Mine resources over time
python transact Adidas Red 5      # Buy 5 Red pigments from Adidas
python update buy Red 20          # Set your buy price for Red to $20
```

---

## The Business Display

The CLI renders beautiful ASCII business cards:

```
|=====    Nike     =====|
|  Money      $300.00   |
|-------  Stock  -------|
|                       |
|****     Red     ****|
| Quantity:    10       |
| Buy Price:  $1.00     |
| Sell Price: $1000.00  |
|                       |
|****    Green    ****|
| Quantity:    0        |
| Buy Price:  $1.00     |
| Sell Price: $1000.00  |
|                       |
|****    Blue     ****|
| Quantity:    5        |
| Buy Price:  $1.00     |
| Sell Price: $1000.00  |
|                       |
|=======================|
```

---

## Design Decisions

**Why physical distance matters:** Convoys create natural trade barriers. Goods aren't free to move — you pay for speed, and transit takes real wall-clock time. This creates arbitrage opportunities: a pigment worth $1 in Santa Cruz might sell for $15 in Redwood City, but only if you can get it there.

**Why midpoint pricing:** Neither buyer nor seller gets screwed. The settlement price splits the difference between the bid and ask, creating a fair market mechanism that rewards good price-setting.

**Why the canvas costs pigment:** It closes the economic loop. Currency isn't abstract — it literally becomes art. Players have to weigh trading profit against creative expression. Do you sell your Blue pigments for profit, or paint with them?

**Why a quiz system:** The Oracle is a velocity regulator. It injects currency into the economy at a controlled rate, gated by knowledge rather than time or luck. The variable rewards (1-5 points) create interesting risk/reward choices for players.

---

## Development History

Built in a **9-day sprint** (June 29 – July 7, 2019) at UC Santa Cruz.

| Day | Milestone |
|-----|-----------|
| **Day 1** | Repository scaffolding, business model, MongoDB integration |
| **Day 2** | Convoy system with async travel, distance calculations |
| **Day 3** | Network layer, P2P broadcasting, transaction CLI |
| **Day 4** | Collaborative pixel canvas with Socket.IO |
| **Day 5-7** | Oracle quiz system, canvas color mixing, polish |
| **Day 8-9** | Oracle question expansion (48 questions), bug fixes |

**43 total commits** · Primary author: William Wyatt · Contributor: Val (oracle questions)

---

## Future Possibilities

This codebase is a foundation waiting to be expanded:

- **Dynamic pricing** — Supply/demand curves that shift prices automatically
- **Price volatility** — Random walk models on commodity values
- **Map visualization** — Animated convoy routes on a rendered map
- **AI traders** — Reinforcement learning agents finding arbitrage
- **Commodity expansion** — Beyond RGB: wool, grain, ore, tools
- **Risk mechanics** — Convoy piracy, market crashes, bankruptcy
- **Leaderboards** — Wealth rankings, trade volume, canvas contributions
- **Mobile client** — Same Flask API, responsive frontend
- **Persistent lobbies** — Game rooms with custom parameters

---

## License

MIT License · William Wyatt · UC Santa Cruz

---

<p align="center">
  <em>"The economy feeds the art."</em>
</p>
