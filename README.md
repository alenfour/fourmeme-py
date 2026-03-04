# fourmeme-py

A minimal Python client for the [four.meme](https://four.meme) token launch API on BSC.

Covers the full creation flow: wallet auth → image upload → token creation args → on-chain submission via `TokenManager2`.

---

## Installation

```bash
git clone https://github.com/alenfour/fourmeme-py
cd fourmeme-py
pip install -r requirements.txt
cp .env.example .env
# set WALLET_PRIVATE_KEY in .env
```

---

## Modules

| Module | Description |
|--------|-------------|
| `src/fourmeme/auth.py` | Nonce fetch + wallet signature login |
| `src/fourmeme/client.py` | REST client — upload, create_token, ticker |
| `src/fourmeme/onchain.py` | BSC Web3 — calls `TokenManager2.createToken()` |

---

## Auth Flow

```
1. GET  /meme-api/v1/public/user/login/nonce?address=<wallet>
        → { nonce }

2. Sign message:  "You are sign in Meme {nonce}"
   using wallet private key  →  signature (hex)

3. POST /meme-api/v1/public/user/login
        { address, signature, nonce }
        → { accessToken, expiresIn }
```

---

## Token Creation Flow

```
1. POST /meme-api/v1/private/tool/upload   (multipart image)
        → { url: "https://..." }

2. POST /meme-api/v1/private/token/create
        {
          name, symbol, description,
          imgUrl, raisedTokenSymbol, raisedAmount,
          twitter, telegram, website
        }
        → { createArg: "0x...", signature: "0x..." }

3. BSC: TokenManager2.createToken(createArg, signature)
        value = raisedAmount in wei
        → token deployed on-chain
```

---

## On-chain Contract

| | |
|---|---|
| Contract | `TokenManager2` |
| Address | `0x5c952063c7fc8610FFDB798152D69F0B9550762b` |
| Network | BSC Mainnet (chainId 56) |
| Method | `createToken(bytes createArg, bytes signature) payable` |

---

## Example Launch

Token deployed via this client:

```
CA:      0x083ae7a7f0d099811636f9f73d4285e3d3e14444
Network: BSC Mainnet
Wallet:  0x4d246f362fd94ba04d2909b7fff3621244d8ab7b
```

Run the example:

```bash
python examples/launch_token.py
```

---

## Warning

- Never commit your `.env` or private key
- Always verify token creation args before submitting on-chain
- Gas + optional BNB seed raise required per launch

---

Built by [@alenfour](https://github.com/alenfour)
