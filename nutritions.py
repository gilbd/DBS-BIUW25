import ast  # To safely evaluate the string as a dictionary
import csv

# File paths
input_file = "core-data_recipe.csv"
output_file = "nutritions.csv"
contains_file = "contains.csv"

# Set to store unique nutrition items
unique_nutritions = set()
nutrition_daily_values = {}
recipe_contains = []

# Reading from input CSV
with open(input_file, mode="r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        # Get the 'nutritions' column (which is a string representation of a dictionary)
        recipe_id = row.get("recipe_id", "")
        nutritions_column = row.get("nutritions", "")

        # If 'nutritions' column is not empty
        if nutritions_column:
            try:
                # Safely convert the string to a dictionary
                nutritions = ast.literal_eval(nutritions_column)

                # Loop through each nutrition item in the dictionary
                for key, value in nutritions.items():
                    # Extract the nutrition name and unit
                    nutrition_name = value.get("name")
                    unit = value.get("unit")
                    percent_daily_value = value.get("percentDailyValue", 0)
                    amount = value.get("amount")

                    if (
                        percent_daily_value
                        and percent_daily_value.isalnum()
                        and int(percent_daily_value)
                    ):
                        daily_value = amount / (int(percent_daily_value) / 100)
                        nutrition_daily_values[nutrition_name] = daily_value

                    # If both name and unit are available, add to the set
                    if nutrition_name and unit:
                        unique_nutritions.add((nutrition_name, unit))
                        recipe_contains.append((recipe_id, nutrition_name, amount))
            except (ValueError, SyntaxError) as e:
                # Handle errors in the case of invalid 'nutritions' column
                print(f"Error parsing nutritions data: {e} for row: {row}")
                continue

# Writing unique nutrition data to the output CSV
with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)

    # Write the header for the nutrition CSV (columns: 'Nutrition Name' and 'Unit')
    writer.writerow(["name", "unit", "average_daily_value"])

    # Write each unique nutrition item (name and unit) as a new row
    for nutrition_name, unit in unique_nutritions:
        nutrition_daily_value = nutrition_daily_values.get(nutrition_name, 0)
        writer.writerow([nutrition_name, unit, nutrition_daily_value])

with open(contains_file, mode="w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["recipe_id", "nutrition_name", "amount"])
    for recipe_id, nutrition_name, amount in recipe_contains:
        writer.writerow([recipe_id, nutrition_name, amount])

print(f"Nutrition data has been extracted to {output_file}.")
print(f"Contains data has been extracted to {contains_file}.")
