# Business Requirements and KPI Validation

## Objective
Fine-tune the model so it can resolve credit card support queries accurately and quickly, with minimal human handover.

## Primary Business KPIs

### 1) Query Resolution Rate (QRR)
- **Business target:** Resolve at least **80%** of credit card queries without human help.
- **Definition:** A query is "resolved" if the answer is correct, complete, and actionable with no handover required.
- **Formula:**
	- `QRR = (Resolved Queries / Total Queries) * 100`

### 2) First Contact Resolution (FCR)
- **Business target:** Achieve at least **85%** first-response resolution.
- **Definition:** The **first model response** fully solves the query without follow-up clarification.
- **Formula:**
	- `FCR = (Queries Resolved in First Response / Total Queries) * 100`

## Validation Plan During Fine-Tuning
1. Create a fixed evaluation set of representative credit card queries.
2. Run model inference on the same evaluation set after each fine-tuning cycle.
3. Label each response with:
	 - `Resolved` or `Not Resolved`
	 - `Resolved in First Response` or `Needs Follow-up/Handover`
4. Compute QRR and FCR and compare with targets.

## Decision Criteria
- Fine-tuning iteration is acceptable only if:
	- `QRR >= 80%`
	- `FCR >= 85%`

## Role of Technical Metrics
Validation loss, BERTScore, and similar technical metrics are **supporting diagnostics**.
They are used to guide model improvements, but business success is determined by QRR and FCR.
