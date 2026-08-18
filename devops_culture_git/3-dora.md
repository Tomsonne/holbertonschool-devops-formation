# DORA Metrics and DevOps Culture

## Q1

* **Deployment frequency:** how frequently an organization successfully deploys code to production.
* **Lead time for changes:** the time required for a change to go from code committed to code successfully running in production.
* **Change failure rate:** the percentage of changes or deployments that cause a failure in production and require remediation.
* **Time to restore service (MTTR):** the time required to restore service after a production incident, outage, or service impairment.

## Q2

The poor metric is **deployment frequency** because deploying only once a quarter means that the team delivers changes to production very infrequently.

## Q3

The **lead time for changes** improves because the time required for a change to go from code committed to successfully running in production becomes shorter.

## Q4

This is the **change failure rate**. One failed deployment out of four represents a change failure rate of 25%.

A high change failure rate is bad because it means that a large percentage of deployments cause incidents or require remediation.

## Q5

CALMS stands for:

* **Culture**
* **Automation**
* **Lean**
* **Measurement**
* **Sharing**

## Q6

**False.** Elite teams deploy more frequently and work with smaller batches.

Small and frequent changes are easier to test, review, deploy, monitor, and roll back. This allows teams to increase throughput without sacrificing stability.

## Q7

The correct answer is **(b) monitoring and alerting plus automated rollback**.

Monitoring and alerting help the team detect an incident quickly. Automated rollback reduces the time required to restore service by returning the application to a known working version.

## Q8

The **throughput** metrics are:

* Deployment frequency
* Lead time for changes

The **stability** metrics are:

* Change failure rate
* Time to restore service (MTTR)

Throughput measures how frequently and quickly a team delivers changes. Stability measures how often deployments cause failures and how quickly the team restores service after an incident.

## Q9

We run blameless post-mortems to understand the technical, organizational, and process conditions that contributed to an incident without blaming an individual.

A blameless approach encourages honesty, collaboration, learning, and sharing. It helps the team identify corrective actions and improve the system so that similar incidents are less likely to happen again.
