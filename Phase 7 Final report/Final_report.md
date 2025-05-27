# Phase 7 (Final report)

## Presentation
The [presentation file](./Presentation.pdf) can be found from this directory.

## Maintenance Plan
To ensure long-term stability and improvement of the system, we propose the following maintenance strategies:

**Testing:** Writing unit tests for the backend and UI tests for the frontend will be prioritized to ensure system behavior remains consistent through future updates.

**Model Updates:** Models should be retrained regularly using new data. For now, hyperparameter tuning will need to be performed manually during each retraining cycle.

**Backend Compatibility:** Periodic checks will be made to ensure compatibility with newer versions of FastAPI and other dependencies.

**Data and Model Backup:** Regular backups of datasets and trained models are critical. Automation through scheduled tasks (e.g., cron jobs) and cloud storage solutions like AWS S3 is recommended.

**Continuous Improvement:** Further improvement plans and detailed development notes can be found in:
- [docs/Phase 6/README.md](../Phase%206/README.md)
- [docs/Phase 6/phase_6_result.ipynb](../Phase%206/phase_6_result.ipynb)

## Self-Assessment of the Project (Team Perspective)
Throughout the project, our team effectively collaborated to understand the business goals, analyze the dataset, and develop high-performing predictive models.
Key achievements include:

1. Successfully achieving very high prediction accuracies with the models:
   - XGBoost: ~95%
   - MLP: ~100%
2. Building a production-ready deployment setup with straightforward and repeatable steps.
3. Implementing user-friendly API endpoints that allow adding new data and triggering retraining directly from the UI, making future maintenance significantly easier.

Overall, the project is well-structured for future scalability, continuous delivery, and real-world application. We are confident that with the outlined maintenance practices, the system will remain robust and evolve effectively over time.
