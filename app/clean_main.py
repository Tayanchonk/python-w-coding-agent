"""
Main FastAPI application with Clean Architecture structure
"""
from fastapi import FastAPI
import uvicorn

from app.infrastructure.database import Base, engine
from app.presentation.controllers.auth_controller import router as auth_router
from app.presentation.controllers.employee_controller import router as employee_router
from app.presentation.controllers.position_controller import router as position_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="A CRUD API for employee management with JWT authentication using Clean Architecture",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(employee_router, prefix="/employees", tags=["Employees"])
app.include_router(position_router, prefix="/positions", tags=["Positions"])


@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint that provides API information"""
    return {
        "message": "Employee Management API",
        "version": "2.0.0",
        "architecture": "Clean Architecture",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", summary="Health check")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "architecture": "clean"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)