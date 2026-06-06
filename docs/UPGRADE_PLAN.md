# E-Commerce Upgrade Plan

A phased plan to fix known bugs, finish the checkout/address refactor, and harden the app for production. Review each phase before implementing; phases are ordered by impact and dependency.

**Last reviewed:** 2026-06-06  
**Stack:** Django 3.2.7 · PostgreSQL · Razorpay · `products` + `useraccount` apps

---

## How to use this document

1. Work through phases in order unless noted otherwise.
2. Check off tasks as you complete them.
3. Run the **Verification** steps at the end of each phase before moving on.
4. Keep changes small — one PR or commit per phase is ideal.

---

## Phase 0 — Environment & database baseline

**Goal:** Ensure the app runs against a consistent schema before bug fixes.  
**Priority:** Required first  
**Effort:** ~30 minutes

### Tasks

- [ ] Apply pending migrations, especially `useraccount/migrations/0007_auto_20221024_1713.py` (adds `Address.landmark`):
  ```bash
  python manage.py migrate
  ```
- [ ] Confirm PostgreSQL database `e_commerce` exists and credentials in `e_commerce/settings.py` match your local setup.
- [ ] Create a `.env` file (do not commit) for secrets — used in Phase 4:
  ```
  SECRET_KEY=
  DB_NAME=e_commerce
  DB_USER=postgres
  DB_PASSWORD=
  DB_HOST=localhost
  DB_PORT=5432
  RAZOR_KEY_ID=
  RAZOR_KEY_SECRET=
  ```
- [ ] Document local run steps in a short note (optional): `pip install -r requirements.txt`, `python manage.py runserver`.

### Verification

- [ ] `python manage.py check` passes with no errors.
- [ ] Home page (`/`) loads and shows products.
- [ ] Admin (`/admin/`) loads.

---

## Phase 1 — Critical bugs (data corruption & crashes)

**Goal:** Fix issues that corrupt product prices, break orders, or crash pages.  
**Priority:** P0 — do immediately after Phase 0  
**Effort:** ~2–4 hours  
**Depends on:** Phase 0

These bugs affect real data or block core flows. Fix them before any UI polish.

### 1.1 Cart mutates `ProductVariation.price` in the database

**Problem:** Multiple views multiply `product_variation.price` by quantity and never restore the original unit price. Every cart view, checkout, and payment permanently inflates prices in the DB.

**Affected files:**

| File | Lines (approx.) |
|------|-----------------|
| `useraccount/views.py` | `view_cart`, `cart_plus_minus`, `cart_remove`, `payment`, `paymenthandler`, `get_billing_details` |

**Fix approach:**

- [ ] Introduce a small helper (or inline calculation) that computes line totals without touching the model:
  ```python
  line_total = item.product_variation.price * item.quantity
  ```
- [ ] Remove all `item.product_variation.price *= item.quantity` assignments.
- [ ] Never call `.save()` on `ProductVariation` during cart/display logic.
- [ ] Audit existing DB data: reset any variation prices that were already corrupted (manual SQL or admin fix).

### 1.2 Wrong loop variable in stock deduction after payment

**Problem:** In `paymenthandler`, stock is decremented using `item.quantity` from the cart loop instead of `order_detail.quantity`.

**File:** `useraccount/views.py` (~line 628)

**Fix:**

- [ ] Change `product_variation_obj.quantity -= item.quantity` to `product_variation_obj.quantity -= order_detail.quantity`.

### 1.3 Registration form validation never runs

**Problem:** `form_obj.is_valid` is missing `()` — validation is always truthy (method reference), so invalid registrations may be saved.

**File:** `useraccount/views.py` — `view_reg` (~line 57)

**Fix:**

- [ ] Change `if form_obj.is_valid:` to `if form_obj.is_valid():`.

### 1.4 Broken redirect URL name

**Problem:** Several views call `redirect('view_checkout')`, but the URL name is `'checkout'`. This raises `NoReverseMatch` on validation errors.

**File:** `useraccount/views.py` — `view_checkout`, `update_billing_details` (~lines 505, 509, 759, 762, 769)

**Fix:**

- [ ] Replace all `redirect('view_checkout')` with `redirect('checkout')`.

### 1.5 Order status field name mismatch

**Problem:** Model field is `order_status`, but views and templates use `.status`.

**Affected files:**

| File | Change |
|------|--------|
| `useraccount/views.py` | `cancel_order`: `order_obj.status = 5` → `order_obj.order_status = 5`; `order` POST: `order_item.order.status` → `order_item.order.order_status` |
| `useraccount/templates/order.html` | `order.status` → `order.order_status` |
| `useraccount/templates/order_details.html` | `order_item.order.status` → `order_item.order.order_status` |

### 1.6 `get_billing_details` uses undefined `request`

**Problem:** Helper references `request` and `messages` but only receives `customer_obj`. Stock-check branch calls `redirect('cart')` inside a function that should return `(context, msg)`.

**File:** `useraccount/views.py` — `get_billing_details` (~lines 886–971)

**Fix:**

- [ ] Add `request` as a parameter: `get_billing_details(request, customer_obj)`.
- [ ] Update all callers: `view_checkout`, `update_billing_details`.
- [ ] Replace `return redirect('cart')` inside the helper with `return None, 'Some products in your cart are out of stock...'`.
- [ ] Remove the price-mutation block at the end of this function (covered in 1.1); compute Razorpay `amount` from unit prices only.

### 1.7 `OrderDetails` template uses wrong field

**Problem:** `order_details.html` references `order_item.price`; model field is `amount`.

**File:** `useraccount/templates/order_details.html` (~line 19)

**Fix:**

- [ ] Change `order_item.price` to `order_item.amount`.

### Verification (Phase 1)

- [ ] Add item to cart → refresh page → variation price in admin/DB is unchanged.
- [ ] Register with invalid data → form errors shown, user not created.
- [ ] Submit invalid checkout address → redirects/re-renders without `NoReverseMatch`.
- [ ] Complete a test Razorpay payment → stock decrements by correct quantity.
- [ ] Cancel order → `order_status` becomes `5`; order list shows correct status labels.
- [ ] Order detail page shows line item amounts correctly.

---

## Phase 2 — Checkout & address refactor completion

**Goal:** Finish the migration from user-profile address fields to the `Address` model; make checkout forms work correctly.  
**Priority:** P1  
**Effort:** ~3–5 hours  
**Depends on:** Phase 1

### 2.1 Checkout form does not POST to the right endpoints

**Problem:** `checkout.html` uses `<form action="#">` and wraps submit buttons in `<a href="...">`, so "Update details" and "PLACE ORDER" do not submit the billing form reliably.

**File:** `useraccount/templates/checkout.html`

**Fix:**

- [ ] Set form `action` to `{% url 'checkout' %}` (or `{% url 'update_billing_details' %}` if you consolidate handlers).
- [ ] Replace anchor-wrapped buttons with plain `<button type="submit">` and use `name`/`value` or separate forms for "Update details" vs payment.
- [ ] Keep Razorpay `pay-btn` as `type="button"` so it only opens the modal (not a form submit).
- [ ] Fix breadcrumb links: `./index.html` → `{% url 'home' %}`, `./shop.html` → `{% url 'products' %}`.

### 2.2 Legacy `edit_profile_from_checkout` references removed user fields

**Problem:** View sets `cust_obj.address` and `cust_obj.zipcode` on `LoginTable`, but those fields no longer exist. Route is still registered.

**Files:**

- `useraccount/views.py` — `edit_profile_from_checkout` (~lines 337–350)
- `useraccount/urls.py` — `edit_profile_from_checkout` route

**Fix (choose one):**

- [ ] **Option A (recommended):** Delete the view and URL; use `/address/` and checkout billing form only.
- [ ] **Option B:** Rewrite to upsert `Address` model (same logic as `update_address`).

### 2.3 Deduplicate address save logic

**Problem:** Address create/update is copy-pasted in `update_address`, `view_checkout`, and `update_billing_details`.

**Fix:**

- [ ] Extract one function, e.g. `save_customer_address(customer_id, line1, line2, landmark, city, state, zipcode) -> Address`.
- [ ] Optionally extract `save_customer_name(customer_obj, first_name, last_name)`.
- [ ] Call from all three views.

### 2.4 Consolidate checkout POST handlers

**Problem:** `view_checkout` and `update_billing_details` duplicate POST logic.

**Fix:**

- [ ] Keep billing POST in `view_checkout` only; remove `update_billing_details` view and URL, **or**
- [ ] Keep `update_billing_details` as the single POST target and make `view_checkout` GET-only.

### 2.5 Delivery fee constant

**Problem:** `₹40` delivery fee is hardcoded in multiple places.

**Fix:**

- [ ] Add `DELIVERY_FEE = 40` in `e_commerce/settings.py` and reference it everywhere (cart, checkout, payment).

### Verification (Phase 2)

- [ ] `/address/` — create and update address persists correctly.
- [ ] `/checkout/` — "Update details" saves address + name; page reloads with success message.
- [ ] Razorpay button opens modal; successful payment still hits `paymenthandler`.
- [ ] No references to `LoginTable.address` or `LoginTable.zipcode` remain in active code.

---

## Phase 3 — Product catalog alignment

**Goal:** Align product detail page, brand filter, and URLs with the current `ProductVariation` model.  
**Priority:** P1  
**Effort:** ~2–3 hours  
**Depends on:** Phase 1 (price logic)

### 3.1 Product details page is broken

**Problem:** Template expects `pr_details.pr_image` and `details.description`; `Products` has no image field and `ProductDetails` model was removed.

**Files:**

- `products/views.py` — `product_details`
- `products/templates/product_details.html`

**Fix:**

- [ ] Load `ProductVariation` objects for the product: `ProductVariation.objects.filter(product_id=id)`.
- [ ] Pass variations to template; show image, color, price, description from variation.
- [ ] Wire "Add to cart" to existing AJAX (`add_to_cart` with variation id).
- [ ] Consider URL change to `/product_details/<product_id>/` with variation selector, or `/product/<variation_id>/`.

### 3.2 Brand filter AJAX returns stale schema

**Problem:** `product_view_bybrand` serializes `Products` only; frontend (`products.js`) expects `pr_price`, `pr_image` on product rows.

**Files:**

- `products/views.py` — `product_view_bybrand`
- `products/static/js/products.js` (or inline JS in `home.html`)

**Fix:**

- [ ] Return `ProductVariation` data (or a custom JSON payload) with `image`, `price`, `product_name`, `variation_id`.
- [ ] Update JS to render variation cards and correct add-to-cart ids.

### 3.3 Duplicate `add_to_cart` URL name

**Problem:** Both `products/urls.py` and `useraccount/urls.py` register `name='add_to_cart'`. Last included wins (`/products/add_to_cart/`).

**Fix:**

- [ ] Remove duplicate from `products/urls.py` (line 9) — keep only `useraccount` route.
- [ ] Grep templates/JS for `{% url 'add_to_cart' %}` and hardcoded `/add_to_cart/` paths; ensure they resolve correctly.

### 3.4 `product_details` add-to-cart on listing pages

**Problem:** Home/products pages use variation ids for cart; product details page buttons are not wired.

**Fix:**

- [ ] Reuse same pattern as `home.html` / `products.js` after 3.1 is done.

### Verification (Phase 3)

- [ ] `/product_details/<id>/` renders image, description, price without template errors.
- [ ] Brand filter on home page updates product grid with correct prices/images.
- [ ] Add to cart works from product detail page.
- [ ] `python manage.py show_urls` or manual check: single `add_to_cart` named route.

---

## Phase 4 — Security hardening

**Goal:** Move secrets out of source, reduce attack surface, fix auth gaps.  
**Priority:** P1 (before any public deployment)  
**Effort:** ~2–4 hours  
**Depends on:** Phases 1–2 stable

### 4.1 Externalize secrets

**Files:** `e_commerce/settings.py`

**Fix:**

- [ ] Load `SECRET_KEY`, DB credentials, `RAZOR_KEY_ID`, `RAZOR_KEY_SECRET` from environment (e.g. `python-decouple` or `django-environ`).
- [ ] Add `.env` to `.gitignore` if not already present.
- [ ] Rotate Razorpay test keys if they were ever committed to a public repo.

### 4.2 Production settings guardrails

**Fix:**

- [ ] `DEBUG = os.getenv('DEBUG', 'False') == 'True'` (default False for deploy).
- [ ] Set `ALLOWED_HOSTS` from env.
- [ ] Add `SECURE_*` cookie settings when HTTPS is enabled.

### 4.3 `paymenthandler` CSRF

**Problem:** `@csrf_exempt` on payment callback.

**Fix:**

- [ ] Remove `@csrf_exempt` if Razorpay callback can include CSRF token via `callback_url` + session.
- [ ] If exempt is required, document why and add signature verification as the sole trust boundary (already partially done).

### 4.4 OTP password reset

**Problem:** OTP hardcoded to `1234` in `generate_otp()`; no email sent.

**File:** `useraccount/views.py` (~line 772)

**Fix:**

- [ ] Generate random 4–6 digit OTP.
- [ ] Send via Django `send_mail` (configure `EMAIL_*` in settings) or a provider (SendGrid, etc.).
- [ ] Remove `print()` of OTP in production code.

### 4.5 Password fields visible in forms

**File:** `useraccount/forms.py`

**Fix:**

- [ ] Use `forms.PasswordInput` for password fields in `RegisterForm` and login/reset forms.

### Verification (Phase 4)

- [ ] App starts with secrets only from `.env`.
- [ ] Forgot password sends email (or logs to console backend in dev).
- [ ] No secrets in `git diff` for settings.
- [ ] Payment flow still completes after CSRF changes.

---

## Phase 5 — Authentication & access control

**Goal:** Protect user-specific views consistently.  
**Priority:** P2  
**Effort:** ~1–2 hours  
**Depends on:** Phase 4

### 5.1 Add `@login_required`

**Views to protect:**

| View | File |
|------|------|
| `view_cart` | `useraccount/views.py` |
| `add_to_cart` | `useraccount/views.py` |
| `cart_plus_minus`, `cart_remove` | `useraccount/views.py` |
| `view_checkout`, `update_billing_details`, `update_address` | `useraccount/views.py` |
| `payment`, `paymenthandler`, `order`, `cancel_order` | `useraccount/views.py` |
| `view_profile`, `edit_profile` | `useraccount/views.py` |

**Fix:**

- [ ] Add `from django.contrib.auth.decorators import login_required`.
- [ ] Decorate views; set `LOGIN_URL = '/login/'` in settings.
- [ ] Remove redundant manual `if request.user.is_authenticated` blocks where decorator suffices.

### 5.2 Blocked user handling

**Fix:**

- [ ] Optionally add middleware or a decorator to log out blocked users on each request (currently only checked at login).

### Verification (Phase 5)

- [ ] Logged-out user visiting `/cart/` redirects to login.
- [ ] Logged-out AJAX to `add_to_cart` returns 302/403 appropriately.

---

## Phase 6 — Model & data integrity cleanup

**Goal:** Fix schema inconsistencies and Django best practices.  
**Priority:** P2  
**Effort:** ~2–3 hours  
**Depends on:** Phase 1

### 6.1 `Order.payment_status` type mismatch

**Problem:** `CharField` with integer choices `(1,'Success'), ...`.

**File:** `useraccount/models.py`

**Fix:**

- [ ] Change to `IntegerField(choices=PAYMENT_STATUS, default=2)` and create migration.
- [ ] Set `payment_status=1` explicitly in `paymenthandler` on success.

### 6.2 Naive datetime defaults

**Problem:** `datetime.now()` used instead of `timezone.now`.

**Files:** `useraccount/models.py`, `useraccount/views.py`

**Fix:**

- [ ] Replace defaults with `timezone.now` (no parentheses in model: `default=timezone.now`).
- [ ] Migration if altering field defaults.

### 6.3 Unused / erroneous imports

**File:** `useraccount/models.py`

**Fix:**

- [ ] Remove `from pyexpat import model` and `from unittest.util import _MAX_LENGTH`.

### 6.4 `Order.__str__` when user is null

**Fix:**

- [ ] Guard: `return self.user.username if self.user else f'Order {self.id}'`.

### Verification (Phase 6)

- [ ] `python manage.py makemigrations` / `migrate` clean.
- [ ] New orders have correct `payment_status` and timezone-aware timestamps.

---

## Phase 7 — Admin, logging & observability

**Goal:** Make orders and users manageable; replace `print()` debugging.  
**Priority:** P3  
**Effort:** ~1–2 hours

### Tasks

- [ ] Register in `useraccount/admin.py`: `LoginTable`, `Order`, `OrderDetails`, `Address`, `CustomerOtp`.
- [ ] Add `OrderAdmin` with `OrderDetails` inline (uncomment/adapt existing stub).
- [ ] Fix typo: `admin.site.register(Cart),` → `admin.site.register(Cart)`.
- [ ] Replace `print()` in views with `logging.getLogger(__name__)` at appropriate levels.
- [ ] Configure `LOGGING` in settings for dev.

### Verification

- [ ] Admin can view/edit orders and addresses.
- [ ] No sensitive data logged in production mode.

---

## Phase 8 — Code quality, tests & deployment prep

**Goal:** Long-term maintainability and safe releases.  
**Priority:** P3  
**Effort:** ~4–8 hours

### 8.1 Split `useraccount/views.py`

**Problem:** ~970 lines mixing auth, cart, checkout, payment, OTP helpers.

**Suggested modules:**

```
useraccount/
  views/
    __init__.py      # re-export for urls
    auth.py
    cart.py
    checkout.py
    orders.py
    payments.py
  services/
    address.py
    otp.py
    razorpay.py
```

### 8.2 Remove dead code & unused dependencies

- [ ] Delete or archive: `checkout_old.html`, `login_old.html`, `cart.html` (if unused).
- [ ] Remove unused packages from `requirements.txt`: Falcon, SQLAlchemy, `mysql-connector-python`, etc. (verify nothing imports them).
- [ ] Pin versions; add `requirements-dev.txt` for test tools.

### 8.3 Add tests for critical paths

**Minimum test coverage:**

- [ ] Cart line total calculation does not mutate variation price.
- [ ] `validate_address` accepts/rejects expected inputs.
- [ ] Registration rejects invalid forms.
- [ ] `cancel_order` sets `order_status=5`.
- [ ] `get_billing_details` returns correct subtotal + delivery fee.

**File:** `useraccount/tests.py`, `products/tests.py`

### 8.4 Deployment checklist

- [ ] `collectstatic` configured.
- [ ] `gunicorn`/`waitress` + reverse proxy documented.
- [ ] Media files storage plan (local vs S3).
- [ ] `ALLOWED_HOSTS`, HTTPS, `DEBUG=False`.
- [ ] Razorpay live keys in production env only.

### Verification (Phase 8)

- [ ] `python manage.py test` passes.
- [ ] Fresh clone + `.env` + migrate + runserver works from README-style steps.

---

## Phase summary

| Phase | Focus | Priority | Effort |
|-------|--------|----------|--------|
| 0 | DB & env baseline | Required | ~30 min |
| 1 | Critical bugs (prices, orders, redirects) | P0 | 2–4 h |
| 2 | Checkout & address completion | P1 | 3–5 h |
| 3 | Product catalog alignment | P1 | 2–3 h |
| 4 | Security hardening | P1 | 2–4 h |
| 5 | Auth & access control | P2 | 1–2 h |
| 6 | Model & data integrity | P2 | 2–3 h |
| 7 | Admin & logging | P3 | 1–2 h |
| 8 | Refactor, tests, deploy | P3 | 4–8 h |

**Suggested order:** 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

Phases 5 and 6 can run in parallel after Phase 4. Phase 8 is ongoing but should start only after Phase 1 is verified.

---

## Quick reference — files most often touched

| Area | Primary files |
|------|----------------|
| Cart & checkout logic | `useraccount/views.py` |
| Templates | `useraccount/templates/checkout.html`, `shopping-cart.html`, `order.html` |
| Product display | `products/views.py`, `products/templates/product_details.html`, `products/static/js/products.js` |
| Models | `useraccount/models.py`, `products/models.py` |
| URLs | `useraccount/urls.py`, `products/urls.py`, `e_commerce/urls.py` |
| Config | `e_commerce/settings.py`, `requirements.txt` |
| Admin | `useraccount/admin.py`, `products/admin.py` |

---

## Notes for reviewers

- **Phase 1 is non-negotiable before production** — price mutation alone can make the catalog unusable after a few cart sessions.
- The checkout refactor (Phase 2) is already half-done; finishing it reduces confusion between `checkout.html`, `address.html`, and legacy handlers.
- Razorpay test keys in `settings.py` should be rotated if this repo is or will be public.
- After Phase 1, consider a one-time SQL audit:
  ```sql
  SELECT id, price, product_id FROM products_productvariation ORDER BY modified DESC;
  ```
  Reset prices manually if they look like totals (e.g. 59900 instead of 599).

---

*Update this document as phases complete or priorities change.*
