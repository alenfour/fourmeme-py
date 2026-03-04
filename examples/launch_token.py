"""
Example: launch a token on four.meme via Agentic Mode using fourmeme-py.

Successful launch example:
    Token:   (see README for name/symbol)
    CA:      0x083ae7a7f0d099811636f9f73d4285e3d3e14444
    Network: BSC Mainnet
    Mode:    four.meme Agentic Mode
    Wallet:  0x4d246f362fd94ba04d2909b7fff3621244d8ab7b  (ERC-8004 agent wallet)
"""
import asyncio
import os

from fourmeme.auth import FourMemeAuth
from fourmeme.client import FourMemeClient
from fourmeme.onchain import BSCChain


async def main() -> None:
    private_key = os.environ["WALLET_PRIVATE_KEY"]

    auth   = FourMemeAuth(private_key)
    client = FourMemeClient(auth)
    chain  = BSCChain(private_key)

    print(f"Wallet: {auth.address}")
    print(f"Balance: {chain.get_balance():.4f} BNB")

    # 1. Upload token image
    img_url = await client.upload_image("logo.png")

    # 2. Request creation args from four.meme backend
    result = await client.create_token(
        name="My Token",
        symbol="MTK",
        description="The most based token on BSC",
        img_url=img_url,
        raised_amount=0.1,
    )

    # 3. Submit on-chain
    tx_hash = chain.submit_create_token(
        create_arg=result["createArg"],
        signature=result["signature"],
        raise_amount_bnb=0.1,
    )
    print(f"TX: {tx_hash}")

    receipt = chain.wait_for_receipt(tx_hash)
    print(f"Token deployed: {receipt}")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
