# import os
# import sys
# import time
# import pandas as pd

# sys.path.insert(0, "src")
# from answer import answer_question

# df = pd.read_csv("eval/questions.csv")
# correct = 0
# rows = []

# for _, row in df.iterrows():
#     answer, _ = answer_question(row["question"])
#     ok = str(row["expected"]).lower() in answer.lower()
#     correct += ok
#     rows.append({"question": row["question"], "expected": row["expected"], "correct": ok})
#     print(("PASS" if ok else "FAIL"), "-", row["question"])
#     time.sleep(2)  # avoid free-tier rate limits

# accuracy = correct / len(df) * 100
# print(f"\nAccuracy: {accuracy:.1f}% ({correct}/{len(df)})")
# pd.DataFrame(rows).to_csv("eval/results.csv", index=False)

import sys
import time
import pandas as pd

sys.path.insert(0, "src")
from answer import answer_question

def norm(s):
    """Normalise special characters so matching is fair."""
    return (str(s).lower()
            .replace("\u2011", "-")   # non-breaking hyphen
            .replace("\u2010", "-")
            .replace("\u2013", "-")   # en dash
            .replace("\u2019", "'"))  # curly apostrophe

label = sys.argv[1] if len(sys.argv) > 1 else "baseline"
qfile = sys.argv[2] if len(sys.argv) > 2 else "eval/questions.csv"
df = pd.read_csv(qfile)
correct = 0
rows = []

for _, row in df.iterrows():
    answer, chunks = answer_question(row["question"])
    ok = norm(row["expected"]) in norm(answer)
    correct += ok
    sources = "; ".join(f"{c['source']} p{c['page']}" for c in chunks)
    rows.append({
        "question": row["question"],
        "expected": row["expected"],
        "correct": ok,
        "answer": answer,
        "sources": sources,
    })
    print(("PASS" if ok else "FAIL"), "-", row["question"])
    time.sleep(2)  # avoid free-tier rate limits

accuracy = correct / len(df) * 100
print(f"\nAccuracy: {accuracy:.1f}% ({correct}/{len(df)})")
pd.DataFrame(rows).to_csv(f"eval/results_{label}.csv", index=False)