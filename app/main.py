"""
Main FastAPI application for Employee Management API
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import uvicorn

from app.database import engine, SessionLocal, Base
from app.auth import router as auth_router
from app.employees import router as employees_router
from app.positions import router as positions_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="A CRUD API for employee management with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

security = HTTPBearer()

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(employees_router, prefix="/employees", tags=["Employees"])
app.include_router(positions_router, prefix="/positions", tags=["Positions"])


@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint that provides API information"""
    return {
        "message": "Employee Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", summary="Health check")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)