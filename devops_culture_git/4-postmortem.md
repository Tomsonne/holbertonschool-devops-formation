# PixelCart Friday-Night Incident Post-Mortem

## Incident summary

On Friday evening, PixelCart’s checkout service became unavailable after an invalid database URL was introduced during a manual production deployment. The problem was first reported publicly by a customer at 8:30 pm, but the team did not detect it until 9:15 am on Saturday.

The service was restored at 11:40 am after the configuration error was identified and corrected manually. The incident resulted in approximately 15 hours of checkout downtime and lost revenue.

This post-mortem focuses on the system conditions that allowed the incident to occur and delayed recovery. Its purpose is to improve the delivery and incident-response processes, not to assign blame.

## Factual timeline

* **Friday, 5:40 pm — Deployment started:** A requested checkout fix was deployed manually. The process required an SSH connection to the production server, manual file copying, and direct configuration editing.
* **Friday, 5:52 pm — Incident introduced:** The production database URL was changed and contained a typo. No production-like test environment or automated configuration validation was available.
* **Friday, 6:05 pm — Deployment left unmonitored:** No active monitoring, automated alerting, or formal on-call process was in place.
* **Friday, 8:30 pm — First external report:** A customer reported on social media that checkout was failing. The report was not seen by the team that evening.
* **Saturday, 9:15 am — Incident detected by the team:** The customer complaints were discovered. Incident response was delayed because server access, deployment records, and rollback instructions were not readily available.
* **Saturday, 11:40 am — Service restored:** The incorrect database URL was identified and corrected manually. Checkout functionality returned to normal.

## Impact

* Checkout was unavailable for approximately 15 hours.
* Customers were unable to complete purchases.
* PixelCart lost revenue during the outage.
* The incident became visible publicly on social media.
* Recovery required manual investigation and coordination.

## Systemic causes and affected DORA metrics

### 1. Manual and untracked production deployment

Production changes were performed over SSH by copying files and editing configuration directly on the server. There was no automated deployment pipeline, versioned deployment record, or simple rollback mechanism.

**DORA metrics affected:**

* **Lead time for changes:** manual deployment steps make delivery slower and less repeatable.
* **Deployment frequency:** risky and time-consuming manual deployments discourage frequent, small releases.
* **Time to restore service:** the absence of a versioned rollback mechanism delayed recovery.

### 2. Insufficient testing and configuration validation

There was no test environment matching production, and the database URL was not validated automatically before deployment. The checkout flow therefore reached production without a reliable end-to-end verification.

**DORA metric affected:**

* **Change failure rate:** missing automated tests and configuration validation increased the probability that a deployment would cause a production failure.

### 3. Missing monitoring, alerting, and incident-response readiness

PixelCart had no automated checkout monitoring, no alert for failed transactions, and no formal on-call process. The person who discovered the incident did not have immediate server access, deployment history, or a documented recovery procedure.

**DORA metric affected:**

* **Time to restore service (MTTR):** late detection, unclear ownership, missing access, and the absence of a runbook significantly increased the time required to restore checkout.

## Three priority actions

### Priority 1 — Implement monitoring, alerting, and a formal on-call process

PixelCart should add synthetic checkout monitoring, transaction-failure alerts, and notifications sent directly to an assigned on-call contact. On-call responders should have the required access and a documented incident-response runbook.

**Justification:** This is the first priority because the incident remained unnoticed by the team overnight. Fast detection and immediate access would substantially reduce the **time to restore service** and limit customer and revenue impact.

### Priority 2 — Build an automated, versioned deployment pipeline with rollback

Production deployments should run through a CI/CD pipeline instead of manual SSH operations. The pipeline should record every deployed version, validate required configuration, prevent direct production edits, and provide an automated rollback to the last known working release.

**Justification:** A repeatable pipeline reduces manual deployment errors, shortens the **lead time for changes**, supports a higher **deployment frequency**, lowers the **change failure rate**, and improves the **time to restore service** through rapid rollback.

### Priority 3 — Create a production-like test environment with automated checkout tests

PixelCart should create a staging environment that closely matches production. Each checkout change should pass automated configuration validation, database connectivity checks, and end-to-end checkout tests before deployment.

**Justification:** These controls would have detected the invalid database URL before it reached production. They directly reduce the **change failure rate** and make frequent deployments safer.

## Conclusion

The incident was enabled by gaps in deployment automation, testing, observability, access, and recovery procedures. Strengthening these systems will allow PixelCart to detect failures earlier, deploy smaller changes more safely, and restore service more quickly.

The goal is not to prevent individuals from ever making mistakes. The goal is to build a delivery system in which mistakes are detected before production and can be recovered from rapidly.
