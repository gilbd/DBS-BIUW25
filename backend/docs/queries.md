# SQL Queries Documentation

This document lists all SQL queries used in the application controllers, organized by endpoint.

## Recipe Controller

### Get Recipe
```sql
SELECT 
    r.*,
    CASE WHEN e.user_id IS NOT NULL THEN TRUE ELSE FALSE END as is_eaten,
    JSON_ARRAYAGG(
        JSON_OBJECT(
            'name', n.name,
            'amount', c.amount,
            'unit', n.unit
        )
    ) as nutrition_info
FROM recipe r
LEFT JOIN eats e ON r.recipe_id = e.recipe_id AND e.user_id = :user_id
LEFT JOIN contains c ON r.recipe_id = c.recipe_id
LEFT JOIN nutrition n ON c.nutrition_name = n.name
WHERE r.recipe_id = :id
GROUP BY r.recipe_id, e.user_id
```
Purpose: Fetches a recipe with its nutrition information and eaten status for a specific user

### Get Recent Recipes
```sql
SELECT r.recipe_id, latest_e.latest_created_at
FROM recipe r
JOIN (
    SELECT e.recipe_id, MAX(e.created_at) AS latest_created_at
    FROM eats e
    WHERE e.user_id = :user_id
    GROUP BY e.recipe_id
) latest_e ON r.recipe_id = latest_e.recipe_id
ORDER BY latest_e.latest_created_at DESC
LIMIT 4;
```
Purpose: Gets the most recently eaten recipes for a user

### Get Recommendations
```sql
SELECT r.recipe_id
FROM recipe r
WHERE NOT EXISTS (
    SELECT 1 FROM eats e2
    WHERE e2.recipe_id = r.recipe_id
    AND e2.user_id = :user_id
)
ORDER BY RAND()
LIMIT 5;
```
Purpose: Gets random recipe recommendations that the user hasn't eaten

### Create Recipe
```sql
INSERT INTO recipe (recipe_name, total_time, image, directions, ingredients)
VALUES (:recipe_name, :total_time, :image, :directions, :ingredients)
RETURNING *;
```
Purpose: Creates a new recipe

## Contains Controller

### Add Nutrition to Recipe
```sql
SELECT * FROM recipe WHERE recipe_id = :recipe_id;
SELECT * FROM nutrition WHERE nutrition_name = :nutrition_name;
```
Purpose: Validates recipe and nutrition existence before creating relationship

## Diet Controller

### Get All Diets
```sql
SELECT * FROM diet;
```
Purpose: Retrieves all available diets

## Fits Controller

### Add Recipe to Diet
```sql
INSERT INTO fits (recipe_id, diet_id)
VALUES (:recipe_id, :diet_id);
```
Purpose: Associates a recipe with a diet

## Nutrition Controller

### Get All Nutrition Items
```sql
SELECT * FROM nutrition;
```
Purpose: Retrieves all nutrition items

### Get Nutrition by Name
```sql
SELECT * FROM nutrition WHERE name = :nutrition_name;
```
Purpose: Gets specific nutrition item details

## User Diet Controller

### Add User Diet
```sql
INSERT INTO user_diet (user_id, diet_id)
VALUES (:user_id, :diet_id);
```
Purpose: Associates a user with a diet preference

## Search Queries

### Recipe Search
```sql
SELECT DISTINCT r.*, 
    CASE WHEN e.user_id IS NOT NULL THEN TRUE ELSE FALSE END as is_eaten
FROM recipe r
LEFT JOIN eats e ON r.recipe_id = e.recipe_id AND e.user_id = :user_id
WHERE 
    [Dynamic conditions based on search parameters]
ORDER BY RAND() 
LIMIT 4;
```
Purpose: Searches recipes with various filters (name, ingredients, cooking time)

### Admin Stats

#### Weekly Stats
```sql
SELECT 
    DATE(e.created_at) as day,
    COUNT(*) as eats
FROM eats e
WHERE e.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY DATE(e.created_at)
ORDER BY day;
```
Purpose: Gets daily eating statistics for the past week

#### Top Recipes
```sql
SELECT 
    r.recipe_id,
    r.recipe_name as name,
    COUNT(*) as eats
FROM recipe r
JOIN eats e ON r.recipe_id = e.recipe_id
WHERE e.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY r.recipe_id, r.recipe_name
ORDER BY eats DESC
LIMIT 5;
```
Purpose: Gets the most eaten recipes in the past week

#### Diet Violations
```sql
SELECT 
    u.user_id as userId,
    u.username as user,
    r.recipe_name as recipe,
    d.name as diet
FROM eats e
JOIN user u ON e.user_id = u.user_id
JOIN recipe r ON e.recipe_id = r.recipe_id
JOIN user_diet ud ON u.user_id = ud.user_id
JOIN diet d ON ud.diet_id = d.diet_id
WHERE NOT EXISTS (
    SELECT 1 FROM fits f 
    WHERE f.recipe_id = r.recipe_id 
    AND f.diet_id = ud.diet_id
)
AND e.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
ORDER BY e.created_at DESC
LIMIT 10;
```
Purpose: Identifies recent cases where users ate recipes that don't fit their dietary restrictions

#### Calorie Violations
```sql
WITH user_calories AS (
    SELECT 
        u.user_id,
        u.username,
        u.age,
        u.sex,
        CASE 
            WHEN u.age < 30 THEN '18-29'
            WHEN u.age < 50 THEN '30-49'
            ELSE '50+'
        END as age_group,
        AVG(
            COALESCE((
                SELECT SUM(c.amount)
                FROM contains c
                WHERE c.recipe_id = e.recipe_id
                AND c.nutrition_name = 'Calories'
            ), 0)
        ) as avg_daily_calories
    FROM user u
    JOIN eats e ON u.user_id = e.user_id
    WHERE e.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
    GROUP BY u.user_id, u.username, u.age, u.sex
)
SELECT 
    uc.user_id as userId,
    uc.username as user,
    uc.age_group as ageGroup,
    uc.sex,
    uc.avg_daily_calories as avgCalories,
    CASE 
        WHEN uc.sex = 'M' THEN 2500
        ELSE 2000
    END as recommended,
    ROUND(
        (uc.avg_daily_calories / 
        CASE 
            WHEN uc.sex = 'M' THEN 2500
            ELSE 2000
        END - 1) * 100
    ) as excessPercentage
FROM user_calories uc
WHERE uc.avg_daily_calories > 
    CASE 
        WHEN uc.sex = 'M' THEN 2500
        ELSE 2000
    END
ORDER BY uc.avg_daily_calories DESC;
```
Purpose: Identifies users who consistently exceed their recommended daily calorie intake

#### Top Rated Recipes
```sql
SELECT 
    r.recipe_id as recipeId,
    r.recipe_name as recipeName,
    AVG(rt.rating) as avgRating,
    COUNT(*) as ratingCount
FROM recipe r
JOIN rating rt ON r.recipe_id = rt.recipe_id
WHERE 
    CASE 
        WHEN :period = 'week' THEN rt.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        ELSE TRUE
    END
GROUP BY r.recipe_id, r.recipe_name
HAVING COUNT(*) >= 3
ORDER BY avgRating DESC, ratingCount DESC
LIMIT 10;
```
Purpose: Gets the highest-rated recipes, filtered by time period and minimum number of ratings

## Performance Considerations

1. Indexes
   - Primary keys on all tables
   - Index on eats(user_id, recipe_id)
   - Index on contains(recipe_id, nutrition_name)
   - Index on recipe(recipe_name)

2. Query Optimizations
   - Use of EXISTS for better performance
   - JSON_ARRAYAGG for efficient nutrition data aggregation
   - LIMIT clauses to restrict result sets
   - LEFT JOINs for optional relationships

3. Data Integrity
   - Foreign key constraints
   - NOT NULL constraints where appropriate
   - Unique constraints on relevant fields

## Common Patterns

1. User-Specific Queries
   - Most queries include user_id filtering
   - Use of CASE statements for boolean flags
   - LEFT JOINs for optional user relationships

2. Aggregation Patterns
   - GROUP BY for aggregating related data
   - JSON_ARRAYAGG for nested data structures
   - MAX() for latest records

3. Randomization
   - ORDER BY RAND() for recommendations
   - LIMIT for controlling result set size 