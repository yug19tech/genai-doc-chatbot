![Answer with sources](screenshot.png)
![Out-of-scope question refused](screenshot-refusal.png)
## Evaluation

**Tuning set (24 questions, 4 out-of-scope):**

| Chunk size | Overlap | Top-k | Accuracy |
|---|---|---|---|
| 500 | 50 | 4 | 95.8% |
| 500 | 50 | 6 | 95.8% |
| 300 | 50 | 4 | 100% |
| 800 | 100 | 4 | 100% |

The single failure at chunk size 500 was a question about a table
(fragment lifecycle) whose chunk was split badly. Increasing top-k did not
fix it; changing chunk size did. Chunk 300 / overlap 50 was chosen as the final
setting as a tiebreak, since several settings scored 100%.
The first strict keyword check also wrongly failed one correct answer
because of a special hyphen character; I fixed the checker by normalising text.

**Held-out set (12 new questions, 2 out-of-scope), run once with no tuning:**
83.3% (10/12). Failures: [BAM question: cause], [Retrofit question: cause].
All out-of-scope questions were correctly refused.

**Limitations:** small test sets written by me from the same documents, a
keyword-based check that can miss paraphrased answers, and only three short
PDFs. Next steps: an LLM-based judge, a larger test set, and re-ranking.