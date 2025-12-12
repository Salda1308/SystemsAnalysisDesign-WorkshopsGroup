
# This script loads the trained model and makes predictions on new data
# Called by the Python API when users upload CSV files

# Load required libraries
suppressPackageStartupMessages({
    library(caret)
    library(jsonlite)
    library(data.table)
})

# Get command line arguments - the API will pass the CSV file path
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
    cat("Error: No input file specified\n")
    quit(status = 1)
}

input_file <- args[1]

# Load the trained model
model <- readRDS("OUT/models/best_model_R.rds")

# Load the test data
test_data <- fread(input_file)

# Save the IDs if they exist
if ("Id" %in% names(test_data)) {
    ids <- test_data$Id
} else {
    ids <- 1:nrow(test_data)
}

# Remove ID columns for prediction
X_test <- test_data[, !names(test_data) %in% c("Id", "id", "sales"), with = FALSE]

# Encode categorical variables (same as training)
if ("Tone_of_Ad" %in% names(X_test)) {
    X_test$Tone_of_Ad <- as.numeric(factor(X_test$Tone_of_Ad, levels = c("funny", "serious", "emotional"))) - 1
}
if ("Weather" %in% names(X_test)) {
    X_test$Weather <- as.numeric(factor(X_test$Weather, levels = c("sunny", "cloudy", "rainy"))) - 1
}
if ("Gender" %in% names(X_test)) {
    X_test$Gender <- as.numeric(factor(X_test$Gender, levels = c("Female", "Male"))) - 1
}
if ("Coffee_Consumption" %in% names(X_test)) {
    X_test$Coffee_Consumption <- as.numeric(factor(X_test$Coffee_Consumption, levels = c("low", "medium", "high"))) - 1
}

# Feature Engineering (same as training)
add_features <- function(df) {
    df$Web_Facebook_ratio <- df$Web_GRP / (df$Facebook_GRP + 1)
    df$TV_Web_ratio <- df$TV_GRP / (df$Web_GRP + 1)
    df$Total_ad_spend <- df$Web_GRP + df$TV_GRP + df$Facebook_GRP
    df$Competitor_density <- df$No_of_Competitors / (df$No_of_Big_Cities + 1)
    df$Internet_adoption <- df$Percent_Internet_Access * df$Percent_Uni_Degrees / 100
    return(df)
}
X_test <- add_features(X_test)

# Handle Missing Values and Infinite Values (same as training)
for (col in names(X_test)) {
    if (is.numeric(X_test[[col]])) {
        # Replace infinite values with NA first
        X_test[[col]][is.infinite(X_test[[col]])] <- NA

        # Replace NA with median, or 0 if all values are NA
        if (any(is.na(X_test[[col]]))) {
            med <- median(X_test[[col]], na.rm = TRUE)
            if (is.na(med)) {
                med <- 0
            }
            X_test[[col]][is.na(X_test[[col]])] <- med
        }
    }
}

# Final check: replace any remaining NA or NaN with 0
X_test[is.na(X_test)] <- 0
X_test[is.nan(as.matrix(X_test))] <- 0

# Make predictions based on model type
if (is.list(model) && "meta_model" %in% names(model)) {
    # Stacking ensemble model
    pred_xgb <- predict(model$base_models$xgb, X_test)
    pred_rf <- predict(model$base_models$rf, X_test)
    pred_lm <- predict(model$base_models$lm, X_test)
    meta_features <- data.frame(XGBoost = pred_xgb, RandomForest = pred_rf, Linear = pred_lm)
    predictions_log <- predict(model$meta_model, meta_features)
} else {
    # Single model
    predictions_log <- predict(model, X_test)
}

# Convert from log scale back to original scale
predictions <- expm1(predictions_log)

# Create output dataframe
output <- data.frame(
    Id = ids,
    Expected = predictions
)

# Print as JSON so Python can read it
cat(toJSON(output, dataframe = "rows", pretty = FALSE))
