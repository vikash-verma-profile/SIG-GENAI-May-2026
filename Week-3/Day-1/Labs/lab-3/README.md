# Lab 3 - Chain of Thought SQL Optimiser

## Objective
Implement step-by-step SQL reasoning and compare it with direct SQL generation.

## Learning Outcomes

- Use CoT prompting ideas.
- Improve SQL quality.
- Reduce hallucinations with explicit reasoning.
- Benchmark query performance.

## Detailed Steps

1. Run the optimizer.

   ```bash
   python sql_optimizer.py
   ```

2. Ask this question.

   ```text
   Show total revenue by region
   ```

3. Compare the standard SQL with the reasoned SQL.

4. Review the complexity score and benchmark duration.

## Exercises

- Add query complexity scoring.
- Benchmark query performance across multiple runs.
- Add a query quality checklist.
