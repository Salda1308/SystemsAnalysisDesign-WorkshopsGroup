# Model Comparison in R - Clean & Working
# Student project - chocolate sales prediction

# Setup
options(repos = c(CRAN = "https://cloud.r-project.org/"))
library(caret)
library(randomForest)
library(xgboost)
library(jsonlite)
library(data.table)

cat("=================================================================\n")
cat("MODEL COMPARISON - Functional and Stable\n")
cat("=================================================================\n\n")

# Load Data
cat("Loading data...\n")

# Auto-detect correct paths based on working directory
if (file.exists("OUT/processed_data.csv")) {
    # Running from root directory
    data <- fread("OUT/processed_data.csv")
    test_data <- fread("IN/data_test.csv")
    out_dir <- "OUT"
} else if (file.exists("../OUT/processed_data.csv")) {
    # Running from Training Layer/ directory
    data <- fread("../OUT/processed_data.csv")
    test_data <- fread("../IN/data_test.csv")
    out_dir <- "../OUT"
} else {
    stop("Cannot find data files. Please run from root or 'Training Layer/' directory")
}

# Prepare Features and Target
X <- data[, !names(data) %in% c("sales", "Id", "id"), with = FALSE]
y <- log1p(data$sales) # Simple log transform for better predictions
X_test <- test_data[, !names(test_data) %in% c("Id", "id"), with = FALSE]

# Encode categorical variables consistently between train/val/test
cat("Encoding categorical variables...\n")
encode_categoricals <- function(df) {
    tone_levels <- c("funny", "serious", "emotional")
    weather_levels <- c("sunny", "cloudy", "rainy")
    gender_levels <- c("Female", "Male")
    coffee_levels <- c("low", "medium", "high")

    # Normalize possible numeric codings to strings first
    df$Tone_of_Ad <- as.character(df$Tone_of_Ad)
    df$Weather <- as.character(df$Weather)
    df$Gender <- as.character(df$Gender)
    df$Coffee_Consumption <- as.character(df$Coffee_Consumption)

    df$Gender[df$Gender %in% c("0", "0.0", "female", "Female", "F", "f")] <- "Female"
    df$Gender[df$Gender %in% c("1", "1.0", "male", "Male", "M", "m")] <- "Male"
    df$Gender[!df$Gender %in% gender_levels] <- NA

    df$Coffee_Consumption[df$Coffee_Consumption %in% c("0", "0.0")] <- "low"
    df$Coffee_Consumption[df$Coffee_Consumption %in% c("1", "1.0")] <- "medium"
    df$Coffee_Consumption[df$Coffee_Consumption %in% c("2", "2.0")] <- "high"
    df$Coffee_Consumption[!df$Coffee_Consumption %in% coffee_levels] <- NA

    df$Tone_of_Ad[!df$Tone_of_Ad %in% tone_levels] <- NA
    df$Weather[!df$Weather %in% weather_levels] <- NA

    df$Tone_of_Ad <- as.numeric(factor(df$Tone_of_Ad, levels = tone_levels)) - 1
    df$Weather <- as.numeric(factor(df$Weather, levels = weather_levels)) - 1
    df$Gender <- as.numeric(factor(df$Gender, levels = gender_levels)) - 1
    df$Coffee_Consumption <- as.numeric(factor(df$Coffee_Consumption, levels = coffee_levels)) - 1
    return(df)
}

X <- encode_categoricals(X)
X_test <- encode_categoricals(X_test)

# Feature Engineering
cat("Engineering features...\n")
add_features <- function(df) {
    df$Web_Facebook_ratio <- df$Web_GRP / (df$Facebook_GRP + 1)
    df$TV_Web_ratio <- df$TV_GRP / (df$Web_GRP + 1)
    df$Total_ad_spend <- df$Web_GRP + df$TV_GRP + df$Facebook_GRP
    df$Competitor_density <- df$No_of_Competitors / (df$No_of_Big_Cities + 1)
    df$Internet_adoption <- df$Percent_Internet_Access * df$Percent_Uni_Degrees / 100
    return(df)
}
X <- add_features(X)
X_test <- add_features(X_test)

# Convert to data.frames to keep caret/xgboost happy
X <- as.data.frame(X)
X_test <- as.data.frame(X_test)

# Handle Missing Values (median for numeric columns, using train medians for test)
cat("Handling missing values...\n")
impute_numeric <- function(train_df, test_df = NULL) {
    for (col in names(train_df)) {
        if (is.numeric(train_df[[col]])) {
            med <- suppressWarnings(median(train_df[[col]], na.rm = TRUE))
            if (is.na(med)) med <- 0
            train_df[[col]][is.na(train_df[[col]])] <- med
            if (!is.null(test_df) && col %in% names(test_df)) {
                test_df[[col]][is.na(test_df[[col]])] <- med
            }
        }
    }
    return(list(train = train_df, test = test_df))
}

imputed <- impute_numeric(X, X_test)
X <- imputed$train
X_test <- imputed$test

# Split Data
set.seed(42)
idx <- sample(1:nrow(X), 0.8 * nrow(X))
X_train <- X[idx, ]
y_train <- y[idx]
X_val <- X[-idx, ]
y_val <- y[-idx]

cat("\nTrain:", nrow(X_train), "| Val:", nrow(X_val), "| Test:", nrow(X_test), "\n\n")

# Train Models
cat("Training models...\n\n")
train_ctrl <- trainControl(method = "cv", number = 5)
results <- list()

# Helper function to calculate MAE on original scale
calc_mae <- function(pred_log, actual_log) {
    mean(abs(expm1(pred_log) - expm1(actual_log)))
}

# 1. XGBoost (Direct implementation to avoid caret issues)
cat("1. XGBoost... ")
tryCatch({
    # Convert to matrix format required by xgboost
    dtrain <- xgb.DMatrix(data = as.matrix(X_train), label = y_train)
    dval <- xgb.DMatrix(data = as.matrix(X_val), label = y_val)

    # Simple XGBoost parameters
    params <- list(
        objective = "reg:squarederror",
        eta = 0.1,
        max_depth = 3,
        subsample = 0.8,
        colsample_bytree = 0.8
    )

    # Train with early stopping
    model_xgb <- xgb.train(
        params = params,
        data = dtrain,
        nrounds = 100,
        watchlist = list(train = dtrain, val = dval),
        early_stopping_rounds = 10,
        verbose = 0
    )

    pred_xgb <- predict(model_xgb, dval)
    results$XGBoost <- calc_mae(pred_xgb, y_val)
    cat("MAE:", round(results$XGBoost, 2), "\n")
}, error = function(e) {
    cat("FAILED (", e$message, ")\n")
    model_xgb <<- NULL
    pred_xgb <<- NULL
})

# 2. Random Forest
cat("2. Random Forest... ")
tryCatch({
    model_rf <- train(
        x = X_train, y = y_train, method = "rf",
        trControl = train_ctrl, ntree = 1000, tuneLength = 3
    )
    pred_rf <- predict(model_rf, X_val)
    results$RandomForest <- calc_mae(pred_rf, y_val)
    cat("MAE:", round(results$RandomForest, 2), "\n")
}, error = function(e) {
    cat("FAILED (", e$message, ")\n")
    model_rf <<- NULL
    pred_rf <<- NULL
})

# 3. Linear Regression (Baseline)
cat("3. Linear Regression... ")
tryCatch({
    model_lm <- train(x = X_train, y = y_train, method = "lm", trControl = train_ctrl)
    pred_lm <- predict(model_lm, X_val)
    results$Linear <- calc_mae(pred_lm, y_val)
    cat("MAE:", round(results$Linear, 2), "\n")
}, error = function(e) {
    cat("FAILED (", e$message, ")\n")
    model_lm <<- NULL
    pred_lm <<- NULL
})

# 4. Stacking Ensemble (Combines all models for best results)
cat("4. Stacking Ensemble... ")
tryCatch({
    # Only create ensemble if we have at least 2 successful models
    available_preds <- list()
    if (!is.null(pred_xgb)) available_preds$XGBoost <- pred_xgb
    if (!is.null(pred_rf)) available_preds$RandomForest <- pred_rf
    if (!is.null(pred_lm)) available_preds$Linear <- pred_lm

    if (length(available_preds) >= 2) {
        meta_features <- as.data.frame(available_preds)
        meta_model <- lm(y_val ~ ., data = meta_features)
        pred_stack <- predict(meta_model, meta_features)
        results$Stacking <- calc_mae(pred_stack, y_val)
        cat("MAE:", round(results$Stacking, 2), "\n")
    } else {
        cat("SKIPPED (need at least 2 base models)\n")
        meta_model <- NULL
        pred_stack <- NULL
    }
}, error = function(e) {
    cat("FAILED (", e$message, ")\n")
    meta_model <<- NULL
    pred_stack <<- NULL
})

# Show Results
cat("\n=================================================================\n")
cat("RESULTS (Ranked by MAE)\n")
cat("=================================================================\n")

if (length(results) == 0) {
    cat("ERROR: No models trained successfully!\n")
    cat("=================================================================\n")
    stop("All models failed to train. Check your data and parameters.")
}

sorted <- sort(unlist(results))
for (i in 1:length(sorted)) {
    cat(sprintf("%d. %-20s MAE: %.2f\n", i, names(sorted)[i], sorted[i]))
}
cat("\nWINNER:", names(sorted)[1], "\n")
cat("=================================================================\n")

# Generate Test Predictions
cat("\nGenerating test predictions...\n")
best_name <- names(sorted)[1]

if (best_name == "Stacking" && !is.null(meta_model)) {
    # For stacking, combine all model predictions
    available_test_preds <- list()
    if (!is.null(model_xgb)) {
        dtest <- xgb.DMatrix(data = as.matrix(X_test))
        available_test_preds$XGBoost <- predict(model_xgb, dtest)
    }
    if (!is.null(model_rf)) available_test_preds$RandomForest <- predict(model_rf, X_test)
    if (!is.null(model_lm)) available_test_preds$Linear <- predict(model_lm, X_test)
    meta_test <- as.data.frame(available_test_preds)
    pred_test_log <- predict(meta_model, meta_test)
} else if (best_name == "XGBoost" && !is.null(model_xgb)) {
    dtest <- xgb.DMatrix(data = as.matrix(X_test))
    pred_test_log <- predict(model_xgb, dtest)
} else if (best_name == "RandomForest" && !is.null(model_rf)) {
    pred_test_log <- predict(model_rf, X_test)
} else if (best_name == "Linear" && !is.null(model_lm)) {
    pred_test_log <- predict(model_lm, X_test)
} else {
    stop("Best model is not available for predictions")
}

# Convert back to original scale
pred_test <- expm1(pred_test_log)

# Save Outputs
models_dir <- file.path(out_dir, "models")
if (!dir.exists(models_dir)) dir.create(models_dir, recursive = TRUE)

write.csv(data.frame(Id = test_data$Id, Expected = pred_test),
    file.path(out_dir, "test_predictions.csv"),
    row.names = FALSE
)

write_json(list(
    best_model = best_name,
    best_mae = as.numeric(sorted[1]),
    all_results = lapply(names(sorted), function(n) list(model = n, mae = results[[n]]))
), file.path(out_dir, "model_comparison_results_R.json"), pretty = TRUE, auto_unbox = TRUE)

# Save best model
model_path <- file.path(models_dir, "best_model_R.rds")
if (best_name == "Stacking" && !is.null(meta_model)) {
    # Only save models that were successfully trained
    base_models_list <- list()
    if (!is.null(model_xgb)) base_models_list$xgb <- model_xgb
    if (!is.null(model_rf)) base_models_list$rf <- model_rf
    if (!is.null(model_lm)) base_models_list$lm <- model_lm

    saveRDS(
        list(
            meta_model = meta_model,
            base_models = base_models_list
        ),
        model_path
    )
} else if (best_name == "XGBoost" && !is.null(model_xgb)) {
    saveRDS(model_xgb, model_path)
} else if (best_name == "RandomForest" && !is.null(model_rf)) {
    saveRDS(model_rf, model_path)
} else if (best_name == "Linear" && !is.null(model_lm)) {
    saveRDS(model_lm, model_path)
} else {
    warning("Could not save best model: model object is NULL")
}

cat("\n[OK] Training complete! Results saved to", out_dir, "\n")
