# Question Labeling

## Reasoning
The goal of the labeling is to not only provide obervability into the level of complexity that the agent can handle, but also

There are two major goals for question labeling:
1. Provide observability into the level of complexity the agent can handle
2. Give insight into how to improve the agent.

In other words, we don't want to just know if the agent is good at it's job. We also want to know where the agent is failing and how to make it better.

To achieve this, we need to take a step back and understand the tasks presented. What are the common tasks within data analysis? How do they influence the difficulty of the task? Can we clealy communicate why one task is easy and the other hard?

I created a rubric for labeling that highlights 5 common tasks within analysis. For a given quesiton, each task is scored with 1 (easy), 2 (easy), or 3 (hard). A question is rated easy, medium, or hard based on aggregating the rating of each task.
- **5**: Easy (minimum score, all 1's)
- **6-10**: Medium
- **11++**: Hard

Identifying and scoring sub-tasks helps bring objectivity to the labeling process. We want an approach that can scale to more questions and be performed by more people. While the labeling task does require expertise in data analysis, the scoring system should minimize disagreement between labelers.

This rubric also allows for deeper insights into the agent's performance. As a benchmark, we can identify if the agent's behavior has changed. Run `n` may have the same overall score as `n - 1`, but that top level score may be hiding large changes in performance that neutralize each other. A balanced rubric helps prevent overfitting.

The additional dimensionality also allows for targeted improvements. It's much easier to develop a strategy for improving the agent's ability to perform transformations then stumble around looking for an overall 10% performance boost.

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
- Create `.env` file and add `OPEN_AI_API_KEY` and `ANTHROPIC_API_KEY`.
- Install dependancies: `poetry install`.
- Launch environment: `poetry shell`, or `source .venv/bin/activate` if you know the location of your `venv`.
- `python cli.py --help` to list availible commands
- `python cli.py eval-all` to run full evaluation suite. Choose LLM using `-m` flag; see `--help` for options.
- `python cli.py eval -q question.json -a answer.txt` to run single question. Pass in files using `-q` and `-a` arguments.
