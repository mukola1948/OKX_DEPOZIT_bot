# Observation Log — Pre-release Monitoring

Project: crypto_deposit_alert_bot
Phase: Pre-release (Stabilization)
Start date: 2026-01-19
Expected duration: 7 days
Note: Observation period is time-based, not event-based.
Alert may not trigger during observation — this є acceptable.

---

## Monitoring Scope

Exchanges:
- OKX
- Binance
- MEXC

Telegram:
- Daily report 07:30
- Alert on ≥5% change (time and value logged)

---

## Daily Observations Examples

### 📅 2026-01-19
**Runtime**
- Bot status: Running
- Uptime since last restart: 24h

**Scheduled Events**
- [x] Daily report 07:30 delivered
- [x] Telegram formatting OK (monospace + markdown)
- [x] Time correct (local)

**Alerts**
- Alert triggered: No
- Reason: Deposit change < 5%

**API Stability**
- OKX: OK
- Binance: OK
- MEXC: OK

**Errors**
- None

**Notes**
- Everything stable, no issues observed

---

### 📅 2026-01-20
**Runtime**
- Bot status: Running
- Uptime since last restart: 24h

**Scheduled Events**
- [x] Daily report 07:30 delivered
- [x] Telegram formatting OK
- [x] Time correct (local)

**Alerts**
- Alert triggered: Yes
- Exchange: OKX
- Change: +50.0%
- Time: 00:15
- Message readable: Yes

**API Stability**
- OKX: OK
- Binance: OK
- MEXC: OK

**Errors**
- None

**Notes**
- Dпоточне=3000, Dминуле=2000, N=50 days

---

### 📅 2026-01-21
**Runtime**
- Bot status: Running
- Uptime since last restart: 24h

**Scheduled Events**
- [x] Daily report 07:30 delivered
- [x] Telegram formatting OK
- [x] Time correct (local)

**Alerts**
- Alert triggered: No

**API Stability**
- OKX: OK
- Binance:
