"""


This API calls R scripts for predictions using the R-trained model.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import platform
from pathlib import Path
import tempfile
import subprocess

app = FastAPI(
    title="Chocolate Sales Prediction API",
    description="API for predicting chocolate sales using R-trained XGBoost model",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = Path(__file__).parent.parent
PRESENTATION_DIR = Path(__file__).parent
PREDICTIONS_OUTPUT_PATH = BASE_DIR / "OUT" / "predictions.csv"
R_MODEL_PATH = BASE_DIR / "OUT" / "models" / "best_model_R.rds"

# Set R executable based on OS
R_EXECUTABLE = r"C:\Program Files\R\R-4.5.2\bin\Rscript.exe" if platform.system() == "Windows" else "Rscript"

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "OUT")), name="static")

@app.on_event("startup")
async def startup_event():
    """Startup event - verify R model exists"""
    print("="*70)
    print("CHOCOLATE SALES PREDICTION API")
    print("="*70)
    print("✓ API started - Using R for predictions")
    print(f"✓ R model path: {R_MODEL_PATH}")

    if R_MODEL_PATH.exists():
        print("✓ R model found and ready")
    else:
        print("⚠ R model not found - run 'python run_pipeline.py' first")
    print("="*70)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface"""
    index_path = PRESENTATION_DIR / "index.html"
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read()
    return {"message": "Chocolate Sales Prediction API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if R_MODEL_PATH.exists() else "unhealthy",
        "r_model_exists": R_MODEL_PATH.exists(),
        "r_model_path": str(R_MODEL_PATH)
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Generate predictions using R model

    Args:
        file: CSV file with test data

    Returns:
        JSON with predictions
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")

    try:
        # Read uploaded CSV
        contents = await file.read()

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        # Call R script for predictions
        r_script = PRESENTATION_DIR / "predict.R"
        r_executable = R_EXECUTABLE

        result = subprocess.run(
            [r_executable, str(r_script), temp_path],
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR)
        )

        # Log R script output for debugging
        print(f"R script return code: {result.returncode}")
        print(f"R script stdout: {result.stdout[:500]}")
        print(f"R script stderr: {result.stderr[:500]}")

        if result.returncode != 0:
            raise Exception(f"R script failed with code {result.returncode}. STDERR: {result.stderr}")

        # Parse JSON output from R
        try:
            predictions_data = json.loads(result.stdout)
        except json.JSONDecodeError as je:
            raise Exception(f"Failed to parse R output as JSON. Output was: {result.stdout[:200]}")

        # Clean up
        Path(temp_path).unlink()

        return {
            "status": "success",
            "predictions": predictions_data,
            "count": len(predictions_data),
            "model": "R Stacking Ensemble (Linear + Random Forest + XGBoost)"
        }

    except Exception as e:
        print(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/csv")
async def predict_csv(file: UploadFile = File(...)):
    """
    Generate predictions using R and return as CSV

    Args:
        file: CSV file with test data

    Returns:
        CSV file with predictions
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")

    try:
        # Read uploaded CSV
        contents = await file.read()

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        # Call R script for predictions
        r_script = PRESENTATION_DIR / "predict.R"
        r_executable = R_EXECUTABLE

        result = subprocess.run(
            [r_executable, str(r_script), temp_path],
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR)
        )

        if result.returncode != 0:
            raise Exception(f"R script failed with code {result.returncode}. STDERR: {result.stderr}")

        # Parse JSON output from R
        predictions_data = json.loads(result.stdout)

        # Convert to DataFrame and save
        submission = pd.DataFrame(predictions_data)
        submission.to_csv(PREDICTIONS_OUTPUT_PATH, index=False)

        # Clean up
        Path(temp_path).unlink()

        # Return CSV file
        return FileResponse(
            path=PREDICTIONS_OUTPUT_PATH,
            media_type='text/csv',
            filename='predictions.csv'
        )

    except Exception as e:
        print(f"CSV Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
