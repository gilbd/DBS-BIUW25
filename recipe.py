import csv
import json

# Updated function to calculate the time
def extract_ready_in_time(directions):
    lines = directions.split("\n")  # Split the directions into lines
    for i, line in enumerate(lines):
        if "Ready In" in line:  # Find the line with "Ready In"
            if i - 1 >= 0:  # Ensure the previous line exists
                time_line = lines[i + 1]  # Get the previous line containing time
                time_parts = time_line.split()  # Split the time information into parts
                total_minutes = 0
                for j, part in enumerate(time_parts):
                    try:
                        if part.endswith("h"):  # If it's an hour
                            total_minutes += int(time_parts[j - 1]) * 60  # Convert hours to minutes
                        elif part.endswith("m"):  # If it's minutes
                            total_minutes += int(time_parts[j - 1])  # Add minutes
                    except (ValueError, IndexError):
                        # Ignore errors or incorrect structure
                        continue
                return total_minutes
    return 0  # Return 0 if no time is found

# File paths
input_file = "core-data_recipe.csv"
output_file = "recipes.csv"

# Reading from input and writing to output file
with open(input_file, mode="r", encoding="utf-8") as infile, open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    # Write header to the output file
    writer.writerow(["recipe_id", "recipe_name", "total_time", "image", "directions", "ingredients"])

    for row in reader:
        recipe_id = int(row["recipe_id"])
        recipe_name = row["recipe_name"]
        image_url = row["image_url"]
        ingredients = row["ingredients"]
        # Handle cooking_directions parameter
        try:
            # Clean up the string to remove 'u' and correct the quotes
            directions_text = row["cooking_directions"]
            directions_text = directions_text.replace("u'", "'").replace('u"', '"').replace("'", '"')

            # Extract directions from the cleaned string
            if 'directions' in directions_text:
                # We assume directions are wrapped in quotes, so we remove them first
                start_index = directions_text.find('directions') + 12  # Skip past the 'directions' key
                end_index = directions_text.find('}', start_index)  # Find the end of the directions
                directions_text = directions_text[start_index:end_index].strip('"')

                # Add a quote at the end of the directions string only
                directions_text = f'{directions_text}"'

            # Handle possible embedded newlines correctly
            directions_text = directions_text.replace('\\n', '\n')

        except Exception as e:
            print(f"Warning: Failed to parse directions in row {recipe_id}. Error: {e}")
            directions_text = row["cooking_directions"]

        # Calculate the total time
        total_time = extract_ready_in_time(directions_text)

        # Write processed data to the output file
        writer.writerow([recipe_id, recipe_name, total_time, image_url, directions_text, ingredients])

print(f"CSV file '{output_file}' created successfully!")