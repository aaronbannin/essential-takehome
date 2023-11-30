# manually defined with agent assistance.
# required schema: question, key. answers need to be in a seperate file
base = [
    {
        "question": "In which month was the most products sold?",
        "key": "1_most_sold_month",
        "difficulty": {
            "datasets": 1,
            "fractions": 1,
            "windowing": 1,
            "transformations": 1,
            "scope": 1
        },
        "cot": "I need to use session_clickstream_data.csv to see when products were sold. Group by month and count when Purchased is true.",
        "reasoning": "One dataset needed, no fractions, no windowing, simple group by. Request is very clearly scoped."
    },
    {
        "question": "What were the 5 most common product colors sold in Europe in May, June, and July",
        "key": "2_top_5_colors",
        "difficulty": {
            "datasets": 2,
            "fractions": 1,
            "windowing": 1,
            "transformations": 2,
            "scope": 1
        },
        "cot": "I need to use session_clickstream_data.csv to see when and where products were sold, sku_data.csv for Availible Colors, and country_id_mapping.csv. I need to identify all European countries in country_id_mapping. Then filter the clickstream for the months of May, June, and July and European countries. Aggregate by color and take the top 5 results.",
        "reasoning": "Merging 3 files together. Creating a dimensional hierarchy for countries. Then filter and aggregate. Request is clear."
    },
    {
        "question": "What is the most common color amongst the different clothing types?",
        "key": "3_most_common_color",
        "difficulty": {
            "datasets": 1,
            "fractions": 1,
            "windowing": 1,
            "transformations": 1,
            "scope": 1
        },
        "cot": "I need sku_data.csv for Availible Colors and Type. Group by Type and Availible Colors, counting the rows. Order by count descending and take the first row.",
        "reasoning": "Only 1 file is needed, no fractions, no windowing. A simple transformation to group by color and type. Request is clear. Two stage aggregation."
    },
    {
        "question": "Identify top customers with high purchases and determine what is their common frequency to buy?",
        "key": "4_top_customer_and_frequency",
        "difficulty": {
            "datasets": 2,
            "fractions": 2,
            "windowing": 1,
            "transformations": 2,
            "scope": 2
        },
        "cot": "I need customer_data.csv to find the top customers and session_clickstream_data.csv to determine their purchasing frequncy. Assume that we want the top 5 customers, extract from customer_data the 5 records with largest values for All Purchases. Join this set into session_clickstream_data. Assume that the desired frequency is purchases per month. Aggregate merged set by Customer ID, taking distinct value for All Purchases, counting the number of records with Purchased, and count the quantity of months. Divide the aggregated purchases by quantity of months for each customer.",
        "reasoning": "The instructions are vaugue, agent needs to assume the top N value what frequency should be used. Customers need to be filtered before merging with clickstream. Aggregation needs to avoid fanout. Need to build a ratio."
    },
    {
        "question": "How many products does a customer browse before making a purchase on weekends and holidays vs weekdays?",
        "key": "5_browse_before_purchase",
        "difficulty": {
            "datasets": 3,
            "fractions": 2,
            "windowing": 1,
            "transformations": 3,
            "scope": 2
        },
        "cot": "I need session_clickstream_data.csv for timeseries of user behavior. Add day_of_week and is_holiday dimension. Assume we are using US holidays. Use these columns to filter for weekends and holidays. Create grouping on clickstream data partitioned by date and Customer ID. Aggregate to generate total records and numbner of purchases for Customer ID and date. Compare quantity against holiday and weekend dimensions.",
        "reasoning": "Use clickstream, no fractions. Holidays requires an external dataset. Need windowing to apply logic on ordered data. Medium transformations required. Prompt does not clearly define holidays."
    },
    {
        "question": "What are the most common sizes available for the top-selling products?",
        "key": "6_most_common_sizes",
        "difficulty": {
            "datasets": 3,
            "fractions": 1,
            "windowing": 1,
            "transformations": 3,
            "scope": 1
        },
        "cot": "I need sku_data.csv for size information, and session_clickstream_data.csv to find the top selling products. Filter session_clickstream_data for Purchased, then aggregate by SKU ID and count number of records. Take the top 5 results. In sku_data, Availible Sizes is a string and needs to be cast as a list. Recognize that one SKU ID can have many sizes. Flatten into a table where we have a record for each SKU ID and size combination. Merge with purchase data, group by size and count number of records, order by count descending.",
        "reasoning": "Two datasets are needed, but must be aggregated before merging. No fractions or windowing. Need to transform sizes into useable structure."
    },
    {
        "question": "Are there any trends in product features (texture, color, type) and the session activity (time spent, avg purchases, etc.)?",
        "key": "7_session_and_product_trends",
        "difficulty": {
            "datasets": 3,
            "fractions": 3,
            "windowing": 1,
            "transformations": 3,
            "scope": 3
        },
        "cot": "I need sku_data.csv for product features and session_clickstream_data.csv for session activity. Identify a set of metrics to generate from session activity. Group session activity by date and sku. For each metric, join the grouped session activity into skus to generate a timeseries. Review each metric for changes.",
        "reasoning": "Request is very vauge and requires defining and exploring fractions to answer."
    },
    {
        "question": "What is the average spend in the summer vs spring?",
        "key": "8_season_average_spend",
        "difficulty": {
            "datasets": 1,
            "fractions": 2,
            "windowing": 1,
            "transformations": 2,
            "scope": 1
        },
        "cot": "I need session_clickstream_data.csv for time series. Transform month into season, filter for Purchased. Aggregate to sum price and count purchases. Divide in final step.",
        "reasoning": "One dataset, one fraction at final step. No windowing, small transformation. Request is clearly scoped."
    }
]