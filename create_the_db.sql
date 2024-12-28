CREATE SCHEMA `dbs` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;

CREATE TABLE dbs.recipe (
    recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_name VARCHAR(255) NOT NULL,
    total_time INT NOT NULL,
    image VARCHAR(255),
    directions TEXT NOT NULL,
    ingredients TEXT NOT NULL
);

-- User table
CREATE TABLE dbs.user (
    user_id INT PRIMARY KEY,
    name VARCHAR(90),
    date_of_birth DATE,
    weight TINYINT UNSIGNED,
    height TINYINT UNSIGNED,
    sex ENUM('M', 'F'),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Admin Subclass Table
CREATE TABLE dbs.admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    promoted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES dbs.user(user_id) ON DELETE CASCADE
);

-- Diet Table
CREATE TABLE dbs.diet (
    diet_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL UNIQUE,
    keywords TEXT,
    description TEXT
);

-- User-Diet Relationship
CREATE TABLE dbs.user_diet (
    user_id INT NOT NULL,
    diet_id INT NOT NULL,
    PRIMARY KEY (user_id, diet_id),
    FOREIGN KEY (user_id) REFERENCES dbs.user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (diet_id) REFERENCES dbs.diet(diet_id) ON DELETE CASCADE
);

-- Nutrition Table
CREATE TABLE dbs.nutrition (
    name VARCHAR(45) PRIMARY KEY, -- Name of the nutrition (e.g., Vitamin C, Iron)
    unit VARCHAR(10) NOT NULL,    -- Unit of measurement (e.g., mg, g)
    average_daily_value DECIMAL(10, 2) NOT NULL -- Daily recommended value
);

-- User-Nutrition Relationship
CREATE TABLE dbs.user_nutrition (
    user_id INT NOT NULL,                -- User ID
    nutrition_name VARCHAR(45) NOT NULL, -- Nutrition name
    tracked_value DECIMAL(10, 2),       -- Tracked value (amount consumed)
    PRIMARY KEY (user_id, nutrition_name),
    FOREIGN KEY (user_id) REFERENCES dbs.user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (nutrition_name) REFERENCES dbs.nutrition(name) ON DELETE CASCADE
);

-- Eats (User-Recipe) Relationship
CREATE TABLE dbs.eats (
    user_id INT NOT NULL,                   -- Reference to the user
    recipe_id INT NOT NULL,                 -- Reference to the recipe
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the recipe was eaten
    PRIMARY KEY (user_id, recipe_id, created_at),
    FOREIGN KEY (user_id) REFERENCES dbs.user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES dbs.recipe(recipe_id) ON DELETE CASCADE
);
CREATE INDEX idx_user_id_created_at ON dbs.eats (user_id, created_at);


-- Rating (User-Recipe) Relationship
CREATE TABLE dbs.rating (
    user_id INT NOT NULL,                   -- Reference to the user
    recipe_id INT NOT NULL,                 -- Reference to the recipe
    rating TINYINT UNSIGNED CHECK (rating BETWEEN 1 AND 5), -- Rating value (1-5)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, recipe_id, created_at),
    FOREIGN KEY (user_id) REFERENCES dbs.user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES dbs.recipe(recipe_id) ON DELETE CASCADE
);


-- Contains (Recipe-Nutrition) Relationship
CREATE TABLE dbs.contains (
    recipe_id INT NOT NULL,                 -- Reference to the recipe
    nutrition_name VARCHAR(45) NOT NULL,   -- Reference to the nutrition
    value DECIMAL(10, 2) NOT NULL,         -- Amount of the nutrition in the recipe
    PRIMARY KEY (recipe_id, nutrition_name),
    FOREIGN KEY (recipe_id) REFERENCES dbs.recipe(recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (nutrition_name) REFERENCES dbs.nutrition(name) ON DELETE CASCADE
);

-- Fits (Recipe-Diet) Relationship
CREATE TABLE dbs.fits (
    recipe_id INT NOT NULL,                 -- Reference to the recipe
    diet_id INT NOT NULL,                   -- Reference to the diet
    PRIMARY KEY (recipe_id, diet_id),
    FOREIGN KEY (recipe_id) REFERENCES dbs.recipe(recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (diet_id) REFERENCES dbs.diet(diet_id) ON DELETE CASCADE
);
