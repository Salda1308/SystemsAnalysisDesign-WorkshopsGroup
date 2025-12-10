
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

# Load the trained model with feature names
model_obj <- readRDS("OUT/models/best_model_R.rds")

# Extract model and feature names
if (is.list(model_obj) && "model" %in% names(model_obj)) {
    model <- model_obj$model
    feature_names <- model_obj$feature_names
    model_type <- model_obj$model_type
} else {
    # Fallback for old format
    model <- model_obj
    feature_names <- NULL
    model_type <- "unknown"
}

# Load the test data
test_data <- fread(input_file)

# Save the IDs if they exist
if ("Id" %in% names(test_data)) {
    ids <- test_data$Id
} else {
    ids <- 1:nrow(test_data)
}

# Remove ID and sales columns for prediction
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

# Select only the features used during training
if (!is.null(feature_names)) {
    # Keep only columns that exist in feature_names
    X_test <- X_test[, names(X_test) %in% feature_names, with = FALSE]
    # Reorder columns to match training data
    X_test <- X_test[, feature_names, with = FALSE]
}

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
if (model_type == "stacking") {
    # Stacking ensemble - use base models and meta-model
    library(xgboost)

    base_models <- model$base_models
    meta_model_obj <- model$meta_model

    # Get predictions from base models
    pred_lm <- predict(base_models$lm, X_test)
    pred_rf <- predict(base_models$rf, X_test)

    dtest <- xgb.DMatrix(data = as.matrix(X_test))
    pred_xgb <- predict(base_models$xgb, dtest)

    # Create meta-features
    meta_features <- data.frame(
        Linear = pred_lm,
        RandomForest = pred_rf,
        XGBoost = pred_xgb
    )

    # Get predictions from meta-model
    predictions_log <- predict(meta_model_obj, meta_features)

} else if (model_type == "xgboost") {
    # XGBoost model (native)
    library(xgboost)
    dtest <- xgb.DMatrix(data = as.matrix(X_test))
    predictions_log <- predict(model, dtest)
} else if (model_type == "rf") {
    # Random Forest
    predictions_log <- predict(model, X_test)
} else {
    # Linear model or old format
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
