# Security & Prompt Injection Defense

## 1. Untrusted Customer Feedback Sanitization
Customer feedback submitted via tickets, surveys, reviews, or CSV uploads is strictly treated as untrusted data.
- System prompt instructions and customer feedback are segregated using strict delimiters.
- Feedback strings are passed through `FeedbackService.sanitize_untrusted_input()` which filters prompt injection tokens (`ignore previous instructions`, `system prompt`, `delete bank`).
- Feedback content is retained solely as an inert `experience` payload.

---

## 2. Hard Tenant Isolation
- Each tenant maps to a discrete Hindsight Bank ID (`workspace_{tenant_id}`).
- Memory units, entity graphs, and reflections cannot cross bank boundaries.
- Cross-tenant queries are blocked at the storage engine level.

---

## 3. PII & Secret Redaction
- Credit card numbers, private API tokens, and passwords should be scrubbed before calling `retain()`.
- Hindsight Memory Defense is enabled to safeguard against storing credentials.
