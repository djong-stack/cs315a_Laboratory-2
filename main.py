from fastapi import FastAPI, Query, Path, HTTPException
from typing import Optional, List, Dict, Any

app = FastAPI()

prices_db = [1500.50, 2000.75, 3000.25, 4000.00, 5000.50, 6000.75, 7000.25, 8000.00]


@app.get("/prices")
def get_filtered_prices(
    min_price: Optional[float] = Query(
        default=None,
        ge=0.0,
        title="Minimum Price",
        description="Filter prices greater than or equal to this value",
    ),
    max_price: Optional[float] = Query(
        default=None,
        ge=0.0,
        title="Maximum Price",
        description="Filter prices less than or equal to this value",
    ),
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price",
        )

    filtered = prices_db

    if min_price is not None:
        filtered = [p for p in filtered if p >= min_price]

    if max_price is not None:
        filtered = [p for p in filtered if p <= max_price]

    return {
        "filtered_prices": filtered,
        "count": len(filtered),
    }


employee_db: dict[int, str] = {
    101: "Dean Ong",
    102: "Nino Javier",
    103: "Bongbong Marcos",
    104: "Leni Robredo",
    105: "Rene Baterbonia",
    106: "Robin Padilla",
    107: "Sarah Duterte",
    108: "Lebron James",
}


@app.get("/employees/{emp_id}")
def get_employee(
    emp_id: int = Path(
        title="Employee ID",
        description="3-digit internal employee code",
    ),
):
    if emp_id not in employee_db:
        raise HTTPException(
            status_code=404,
            detail="Employee record not found",
        )

    return {
        "emp_id": emp_id,
        "name": employee_db[emp_id],
    }
