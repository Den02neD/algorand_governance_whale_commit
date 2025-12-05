import requests, time

def algo_commit():
    print("Algorand — Governance Whale Commit (> 50M ALGO locked in one tx)")
    seen = set()
    while True:
        r = requests.get("https://algoexplorer.io/api/v2/transactions?limit=40")
        for tx in r.json().get("transactions", []):
            h = tx["id"]
            if h in seen: continue
            seen.add(h)

            # Governance commit transaction (keyreg with voteKey, etc.)
            if tx.get("tx-type") != "keyreg": continue
            if not tx.get("non-participation", True): continue  # participating
                continue

            amount = tx.get("sender-balance-after", 0) - tx.get("sender-rewards", 0)
            if amount >= 50_000_000_000_000:  # > 50M ALGO (6 decimals)
                addr = tx["sender"][:12]
                period = tx.get("keyreg-tx", {}).get("vote-last-valid", 0)
                print(f"GOVERNANCE WHALE COMMITTED\n"
                      f"{amount/1e6:,.0f} ALGO locked for governance\n"
                      f"Wallet: {addr}...\n"
                      f"Period ends: ~Q{((period//1000000)+1)}\n"
                      f"Tx: https://algoexplorer.io/tx/{h}\n"
                      f"→ Pure conviction play — no yield farming, just belief\n"
                      f"→ Algorand just got a new silent ruler\n"
                      f"{'-'*85}")
        time.sleep(2.1)

if __name__ == "__main__":
    algo_commit()
