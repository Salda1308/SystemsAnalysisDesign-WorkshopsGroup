# Model Comparison in R - Optimized & Clean
# Student project - chocolate sales prediction

# Setup
options(repos = c(CRAN = "https://cloud.r-project.org/"))
library(caret)
library(randomForest)
library(xgboost)
library(jsonlite)
library(data.table)

cat("=================================================================\n")
cat("MODEL COMPARISON - Optimized for Low MAE\n")
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
y <- log1p(data$sales) # Log transform for better predictions
X_test <- test_data[, !names(test_data) %in% c("Id", "id"), with = FALSE]

# Convert categorical variables in test data if they exist (training data already processed)
cat("Processing test data...\n")
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

# Clean data: remove NA, NaN, Inf values
cat("Cleaning data...\n")
for (col in names(X)) {
    if (is.numeric(X[[col]])) {
        # Replace infinite values with NA first
        X[[col]][is.infinite(X[[col]])] <- NA
        # Replace NA with median, or 0 if all values are NA
        if (any(is.na(X[[col]]))) {
            med <- median(X[[col]], na.rm = TRUE)
            if (is.na(med)) med <- 0
            X[[col]][is.na(X[[col]])] <- med
        }
    }
}

for (col in names(X_test)) {
    if (is.numeric(X_test[[col]])) {
        X_test[[col]][is.infinite(X_test[[col]])] <- NA
        if (any(is.na(X_test[[col]]))) {
            med <- median(X_test[[col]], na.rm = TRUE)
            if (is.na(med)) med <- 0
            X_test[[col]][is.na(X_test[[col]])] <- med
        }
    }
}

# Final safety check
X <- as.data.frame(X)
X_test <- as.data.frame(X_test)
X[is.na(X)] <- 0
X_test[is.na(X_test)] <- 0

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
train_ctrl <- trainControl(method = "cv", number = 3, verboseIter = FALSE, allowParallel = FALSE)
results <- list()

# Helper function to calculate MAE on original scale
calc_mae <- function(pred_log, actual_log) {
    mean(abs(expm1(pred_log) - expm1(actual_log)))
}

# 1. Linear Regression (Baseline - fastest)
cat("1. Linear Regression... ")
model_lm <- train(x = X_train, y = y_train, method = "lm", trControl = train_ctrl)
pred_lm <- predict(model_lm, X_val)
results$Linear <- calc_mae(pred_lm, y_val)
cat("MAE:", round(results$Linear, 2), "\n")

# 2. Random Forest (simpler configuration)
cat("2. Random Forest... ")
model_rf <- train(
    x = X_train, y = y_train, method = "rf",
    trControl = train_ctrl, ntree = 200, tuneLength = 1
)
pred_rf <- predict(model_rf, X_val)
results$RandomForest <- calc_mae(pred_rf, y_val)
cat("MAE:", round(results$RandomForest, 2), "\n")

# 3. XGBoost (using xgboost directly, more stable)
cat("3. XGBoost... ")
dtrain <- xgb.DMatrix(data = as.matrix(X_train), label = y_train)
dval <- xgb.DMatrix(data = as.matrix(X_val), label = y_val)

xgb_params <- list(
    objective = "reg:squarederror",
    max_depth = 3,
    eta = 0.1,
    subsample = 0.8,
    colsample_bytree = 0.8
)

model_xgb <- xgb.train(
    params = xgb_params,
    data = dtrain,
    nrounds = 100,
    verbose = 0
)

pred_xgb <- predict(model_xgb, dval)
results$XGBoost <- calc_mae(pred_xgb, y_val)
cat("MAE:", round(results$XGBoost, 2), "\n")

# 4. Stacking Ensemble (Meta-learner combining all base models)
cat("4. Stacking Ensemble... ")

# Create meta-features from base model predictions on validation set
meta_features <- data.frame(
    Linear = pred_lm,
    RandomForest = pred_rf,
    XGBoost = pred_xgb,
    target = y_val
)

# Train meta-model (simple linear regression on base predictions)
meta_model <- lm(target ~ Linear + RandomForest + XGBoost, data = meta_features)

# Generate stacking predictions
meta_test_features <- data.frame(
    Linear = pred_lm,
    RandomForest = pred_rf,
    XGBoost = pred_xgb
)
pred_stack <- predict(meta_model, meta_test_features)
results$Stacking <- calc_mae(pred_stack, y_val)
cat("MAE:", round(results$Stacking, 2), "\n")

# Show Results
cat("\n=================================================================\n")
cat("RESULTS (Ranked by MAE)\n")
cat("=================================================================\n")
sorted <- sort(unlist(results))
for (i in 1:length(sorted)) {
    cat(sprintf("%d. %-20s MAE: %.2f\n", i, names(sorted)[i], sorted[i]))
}
cat("\nWINNER:", names(sorted)[1], "\n")
cat("=================================================================\n")

# Generate Test Predictions
cat("\nGenerating test predictions...\n")
best_name <- names(sorted)[1]

if (best_name == "Stacking") {
    # For stacking, combine all model predictions on test set
    dtest <- xgb.DMatrix(data = as.matrix(X_test))
    pred_lm_test <- predict(model_lm, X_test)
    pred_rf_test <- predict(model_rf, X_test)
    pred_xgb_test <- predict(model_xgb, dtest)

    meta_test <- data.frame(
        Linear = pred_lm_test,
        RandomForest = pred_rf_test,
        XGBoost = pred_xgb_test
    )
    pred_test_log <- predict(meta_model, meta_test)
} else if (best_name == "XGBoost") {
    dtest <- xgb.DMatrix(data = as.matrix(X_test))
    pred_test_log <- predict(model_xgb, dtest)
} else if (best_name == "RandomForest") {
    pred_test_log <- predict(model_rf, X_test)
} else {
    pred_test_log <- predict(model_lm, X_test)
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

# Save best model with feature names
model_path <- file.path(models_dir, "best_model_R.rds")
feature_names <- names(X_train)

if (best_name == "Stacking") {
    # Save stacking ensemble with all base models and meta-model
    model_with_features <- list(
        model = list(
            base_models = list(lm = model_lm, rf = model_rf, xgb = model_xgb),
            meta_model = meta_model
        ),
        feature_names = feature_names,
        model_type = "stacking"
    )
    saveRDS(model_with_features, model_path)
} else if (best_name == "XGBoost") {
    # Save model with feature names
    model_with_features <- list(
        model = model_xgb,
        feature_names = feature_names,
        model_type = "xgboost"
    )
    saveRDS(model_with_features, model_path)
} else if (best_name == "RandomForest") {
    model_with_features <- list(
        model = model_rf,
        feature_names = feature_names,
        model_type = "rf"
    )
    saveRDS(model_with_features, model_path)
} else {
    model_with_features <- list(
        model = model_lm,
        feature_names = feature_names,
        model_type = "lm"
    )
    saveRDS(model_with_features, model_path)
}

cat("\n[OK] Training complete! Results saved to", out_dir, "\n")
