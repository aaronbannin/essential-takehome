# Question Labeling

## Reasoning
!! TODO !! Explain why we are breaking down into categories. It helps identify the agent's performance on specific tasks and can be used to improve performance of the underlying model. Why is the agent succeeding or failing?
!! Do we need a "quantity of steps" or "lenghth of chain of thought" rubric? It seems to be implicit in the current categories

A question's difficulty is heavily influenced by the underlying data model. One of the primary goals of ETL pipelines is to structure the data to simplify queries. This is traditionally defined as denormalizing a transactional data model (OLTP) into one that is designed for analytic workloads (OLAP; Star Schema is a common design pattern). A question that is highly aligned with the data model is easy to answer; a question that is at odds with the data model is hard to answer.

## Rubric
- **Quantity of datasets**: Merging datasets are the most common source of bugs within data modeling. A `join` operation can return the same quantity of rows as the underlying set, remove rows from the underlying set, or it might increase the rows. The latter, when done unintentionally, is known as a [fan out](https://www.googlecloudcommunity.com/gc/Technical-Tips-Tricks/The-problem-of-SQL-fanouts/ta-p/587483).
    - **Easy**: Question can be answered with a single table/dataframe. No joins required.
    - **Medium**: Multiple datasets combined with simple join logic.
    - **Hard**: Complex join logic; e.g. aggregation required prior to join to avoid fan out.
- **Use of Fractions**: Aggregations are foundational to data analysis, and fractions must be aggregated with the correct order. Consider conversion rate; User A has 2 visits and 1 conversion User B has 3 visits and 1 conversion. If we calculate the ratio and then add, we end up with `(0.5 + 0.33)/2 = 0.375`, which is incorrect. The total visists is 5, and the total conversions is 2. Our formula should be `(1 + 1) / (2 + 3) = 0.4`.
    - **Easy**: No fractions are required.
    - **Medium**: Simple aggregation of two measures that are combined in the final step.
    - **Hard**: Combining derirved measures (aggregate in step 2, then again in step 3, then perform division). Distinct counts are also challenging; they are inherenly an `O(n)` operation (you must traverse the entire vector) and can not be rolled up.
- **Windowing and Ordinality of data**: Windowing is applying a function to a row that depends on other rows. Most aggregations are naive to order; `sum(1, 3)` returns the same result as `sum(3, 1)`. The simplest example is row numbers; for a given set of dimensions, this record is the nth value. The value of the previous row is required to determine the current row. In `session_clickstream_data.csv`, the `ordinal` column is a row number calculation. Rolling mean is another good example; we determine the row's mean based on a neighboring subset of data.
    - **Easy**: No windowing required.
    - **Medium**: Simple windowing logic; e.g. row number, rolling sum.
    - **Hard**: Applying window logic on derived data sets, funneling logic (do A, then B, then C).
- **Transformations Required**: It is very common to need to mutate values to make them easier to use. This might be changing the data type (casting year, month, and day columns as a date) or defining a [dimensional hierarchy](https://docs.oracle.com/en/cloud/saas/freeform/freef/about_dimension_hierarchies.html#f_navigate_workspace_143) to facilitate rollups.
    - **Easy**: No transformations are required.
    - **Medium**: Simple projections performed in the first step.
    - **Hard**: Transformations required on derived data.
- **Scope and Clarity of Request**: Does the prompt clearly define a successful response? Does the agent need to make assumptions or infer the prompt's intent? "What is the MoM change in revenue for November 2023?" is clearly scoped. "How is revenue?" is very vaugue and requires the model to infer the intent to answer well.
    - **Easy**: Prompt identifies answer as being a scaler or one-dimensional vector.
    - **Medium**: Answer requires multiple dimensions, modeled as a dataframe.
    - **Hard**: Prompt does not identify the scope of a successful answer; agent must first define possible metrics to be calculated.


# Local Setup
- Install [Poetry](https://python-poetry.org/docs/).
- Create `.env` file and add `OPEN_AI_API_KEY`.
- Install dependancies: `poetry install`.
- Launch environment: `poetry shell`, or `source .venv/bin/activate` if you know the location of your `venv`.
- `python cli.py --help` to list availible commands
- `python cli.py eval` to run evaluation suite.
