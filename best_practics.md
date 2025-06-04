## Best Practice

For APIs, it's common to use the trailing slash for "collection" endpoints (e.g., `/items/`) and omit it for "detail" endpoints (e.g., `/items/42`).
But consistency is most important—choose one style and stick with it throughout your API.

---

**Summary Table:**


| Decorator | `/items` | `/items/` | Redirects? |
| :-- | :-- | :-- | :-- |
| `@app.get("/items")` | ✅ | ❌ | No |
| `@app.get("/items/")` | 🔁 | ✅ | Yes, `/items` → `/items/` |
