from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel
from app.monitor import get_process_stats, load_config
from app.utils import sort_processes, filter_processes, detect_anomalies, mark_child_processes

app = FastAPI(
    title="Process Monitoring API",
    description="API for monitoring and analyzing system processes",
    version="1.0.0"
)



class ProcessResponse(BaseModel):
    """Response model for process data with anomalies"""
    processes: List[Dict]


class AnomalyResponse(BaseModel):
    """Response model for anomaly detection results"""
    anomalies: List[Dict]


class ValidationError(BaseModel):
    """Validation error schema"""
    loc: List[str]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """HTTP validation error schema"""
    detail: List[ValidationError]


@app.get("/", include_in_schema=False)
def root():
    """Health check endpoint

    Returns:
        dict: Simple status message
    """
    return {"message": "It works!"}


@app.get(
    "/processes",
    response_model=ProcessResponse,
    responses={
        400: {"model": HTTPValidationError, "description": "Invalid request parameters"},
        500: {"description": "Internal server error"}
    }
)
def get_processes(
        sort: Optional[str] = Query(
            None,
            description="Sort by: pid, name, cpu_percent, memory_percent",
            example="cpu_percent"
        ),
        desc: bool = Query(
            False,
            description="Sort in descending order",
            example=True
        ),
        filtering: Optional[str] = Query(
            None,
            description="Filter by process name substring",
            example="chrome"
        ),
        anomalies: bool = Query(
            False,
            description="Include anomaly detection markers",
            example=True
        )
) -> ProcessResponse:
    """Get system processes with optional sorting, filtering, and anomaly detection

    Args:
        sort: Field to sort results by
        desc: Sort direction
        filtering: Name substring filter
        anomalies: Enable anomaly detection

    Returns:
        ProcessResponse: Process data with optional anomalies

    Raises:
        HTTPException: 400 for invalid sort parameter
    """
    try:
        data = get_process_stats()
        data = mark_child_processes(data)

        if filtering:
            data = filter_processes(data, filtering.lower())

        if sort:
            valid_sorts = {"pid", "name", "cpu_percent", "memory_percent"}
            if sort not in valid_sorts:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid sort parameter. Valid options: {', '.join(valid_sorts)}"
                )
            data = sort_processes(data, sort, reverse=desc)

        if anomalies:
            data = detect_anomalies(data)

        return ProcessResponse(processes=data)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e


@app.get(
    "/anomalies",
    response_model=AnomalyResponse,
    responses={
        400: {"model": HTTPValidationError, "description": "Invalid threshold values"},
        500: {"description": "Internal server error"}
    }
)
def detect_process_anomalies(
        cpu_threshold: float = Query(
            80.0,
            ge=0,
            le=100,
            description="CPU usage threshold percentage",
            example=85.5
        ),
        mem_threshold: float = Query(
            80.0,
            ge=0,
            le=100,
            description="Memory usage threshold percentage",
            example=90.0
        )
) -> AnomalyResponse:
    """Detect processes exceeding resource thresholds

    Args:
        cpu_threshold: CPU usage threshold percentage (0-100)
        mem_threshold: Memory usage threshold percentage (0-100)

    Returns:
        AnomalyResponse: List of processes exceeding thresholds
    """
    try:
        data = get_process_stats()
        data = mark_child_processes(data)
        anomalies = detect_anomalies(data, cpu_threshold, mem_threshold)
        return AnomalyResponse(anomalies=anomalies)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e


@app.get(
    "/config",
    response_model=Dict,
    responses={
        500: {"description": "Error loading configuration"}
    }
)
def get_current_config() -> Dict:
    """Get current monitoring configuration

    Returns:
        dict: Configuration parameters

    Raises:
        HTTPException: 500 if config cannot be loaded
    """
    try:
        return load_config()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading configuration: {str(e)}"
        ) from e