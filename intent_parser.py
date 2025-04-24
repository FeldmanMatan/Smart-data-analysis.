intent_dict = {
    "graph": "plot",
    "plot": "plot",
    "show": "plot",
    "display": "plot",
    "visualize": "plot",
    "average": "average",
    "mean": "average",
    "avg": "average",
    "count": "count",
    "how many": "count",
    "total": "count",
    "occurred": "when",
    "when": "when",
    "date": "when",
    "time": "when",
    "find": "count"  # Added "find"
}

def parse_query(query, columns):
    """
    Analyzes text queries and identifies intent and relevant columns.

    Args:
        query (str): The query text
        columns (list): List of all columns in the DataFrame

    Returns:
        tuple: (intent, columns_list) - the identified intent and columns
    """
    query = query.lower()
    intent = None

    # Identify intent
    for keyword, action in intent_dict.items():
        if keyword in query:
            intent = action
            break

    # Search for columns in query
    column_matches = []
    for col in columns:
        if col.lower() in query.lower():
            column_matches.append(col)

    # Smarter identification for specific query types
    if intent == "plot" and "with" in query:
        try:
            cols_part = query.split("with")[1].strip()
            if "and" in cols_part:
                col1, col2 = [c.strip() for c in cols_part.split("and")]
                # Find partial matches
                col1_match = find_closest_column(col1, columns)
                col2_match = find_closest_column(col2, columns)
                if col1_match and col2_match:
                    column_matches = [col1_match, col2_match]
        except Exception:
            pass
    # Handle average case
    elif intent == "average" and "of" in query:
        try:
            col = query.split("of")[1].strip()
            col_match = find_closest_column(col, columns)
            if col_match:
                column_matches = [col_match]
        except Exception:
            pass

    # Handle count case
    elif intent == "count":
        # Extract conditions from the query
        conditions = {}
        parts = query.split("where")
        if len(parts) > 1:
            condition_str = parts[1].strip()
            for part in condition_str.split("and"):
                try:
                    col, value = part.strip().split("=")
                    col = col.strip()
                    value = value.strip()
                    col_match = find_closest_column(col, columns)
                    if col_match:
                        conditions[col_match] = value
                except ValueError:
                    pass  # Skip badly formatted conditions
        column_matches = conditions  # Return conditions instead of columns

    # Handle when case
    elif intent == "when" and len(query.split("when")) > 1:
        try:
            col = query.split("when")[1].strip()
            col_match = find_closest_column(col, columns)
            if col_match:
                column_matches = [col_match]
        except Exception:
            pass

    return intent, column_matches

def find_closest_column(search_term, columns):
    """
    Finds the column that best matches the search term.

    Args:
        search_term (str): The search term to match
        columns (list): List of column names to search in

    Returns:
        str or None: The matching column name or None if no match found
    """
    search_term = search_term.lower()

    # Look for exact match
    for col in columns:
        if col.lower() == search_term:
            return col

    # Look for partial match
    for col in columns:
        if search_term in col.lower():
            return col

    return None