"""Generate a reproducible synthetic campaign-response dataset."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N = 1200

def main():
    rng = np.random.default_rng(SEED)
    age = rng.integers(18, 71, N)
    income = np.clip(rng.normal(52000, 18000, N), 12000, 150000).round(0)
    tenure = rng.integers(0, 16, N)
    web_visits = rng.poisson(4, N)
    email_opens = rng.poisson(3, N)
    previous_purchases = rng.poisson(2, N)
    channel = rng.choice(["Email", "Social", "Web", "Phone"], N, p=[.42,.25,.23,.10])
    region = rng.choice(["North", "South", "East", "West"], N)
    score = (-2.0 + .025*(age-35) + .000025*(income-50000)
             + .12*web_visits + .18*email_opens + .22*previous_purchases
             + .08*tenure + (channel=="Email")*.35 + rng.normal(0,.8,N))
    probability = 1/(1+np.exp(-score))
    response = rng.binomial(1, probability)
    df = pd.DataFrame({
        "customer_id": np.arange(10001, 10001+N),
        "age": age, "annual_income": income, "tenure_years": tenure,
        "web_visits": web_visits, "email_opens": email_opens,
        "previous_purchases": previous_purchases, "channel": channel,
        "region": region, "responded": response
    })
    out = Path(__file__).resolve().parents[1] / "data" / "raw" / "campaign_response.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows to {out}")
    print(df["responded"].value_counts(normalize=True).rename("proportion"))

if __name__ == "__main__":
    main()
