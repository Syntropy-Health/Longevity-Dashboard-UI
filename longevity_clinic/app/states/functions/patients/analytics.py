"""Analytics data fetching and processing functions.

Functions for fetching and processing patient analytics data including
biomarker panels, health scores, and trend analysis.
"""

from typing import List, Dict, Any, Optional

from ....config import get_logger

logger = get_logger("longevity_clinic.analytics")


async def fetch_analytics_summary(
    patient_id: Optional[str] = None,
    period_days: int = 30,
) -> Dict[str, Any]:
    """Fetch analytics summary for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        period_days: Time period for analytics

    Returns:
        Analytics summary dict with scores and trends
    """
    logger.info(
        "Fetching analytics summary for patient: %s (%d days)",
        patient_id or "current",
        period_days,
    )

    # TODO: Implement API call
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(
    #         f"{config.analytics_api_base}/patients/{patient_id}/summary",
    #         params={"period_days": period_days},
    #     )
    #     return response.json()

    logger.debug("fetch_analytics_summary: Using demo data (API not implemented)")
    return {
        "health_score": 0,
        "biomarker_score": 0,
        "activity_score": 0,
        "nutrition_score": 0,
        "trends": {},
    }


async def fetch_biomarker_panels(
    patient_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetch biomarker panel data organized by category.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of biomarker panels with categories and markers
    """
    logger.info("Fetching biomarker panels for patient: %s", patient_id or "current")

    # TODO: Implement API call
    logger.debug("fetch_biomarker_panels: Using demo data (API not implemented)")
    return []


async def generate_analytics_report(
    patient_id: Optional[str] = None,
    format: str = "pdf",
) -> Optional[bytes]:
    """Generate an analytics report for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        format: Report format ('pdf', 'csv', 'json')

    Returns:
        Report data bytes or None if generation fails
    """
    logger.info(
        "Generating %s analytics report for patient: %s",
        format,
        patient_id or "current",
    )

    # TODO: Implement report generation
    # This could call a backend service or generate locally
    logger.debug("generate_analytics_report: Not implemented")
    return None


def calculate_health_score(
    biomarkers: List[Dict[str, Any]],
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """Calculate overall health score from biomarker data.

    Args:
        biomarkers: List of biomarker records with values and optimal ranges
        weights: Optional category weights (default: equal weighting)

    Returns:
        Health score from 0-100
    """
    if not biomarkers:
        return 0.0

    weights = weights or {}
    total_weight = 0.0
    weighted_score = 0.0

    for biomarker in biomarkers:
        value = biomarker.get("current_value", 0)
        optimal_min = biomarker.get("optimal_min", 0)
        optimal_max = biomarker.get("optimal_max", 100)
        category = biomarker.get("category", "general")

        # Calculate how close to optimal (0-1)
        if optimal_min <= value <= optimal_max:
            marker_score = 1.0
        elif value < optimal_min:
            marker_score = max(0, value / optimal_min)
        else:
            marker_score = max(0, 1 - (value - optimal_max) / optimal_max)

        # Apply weight
        weight = weights.get(category, 1.0)
        weighted_score += marker_score * weight
        total_weight += weight

    return (weighted_score / total_weight * 100) if total_weight > 0 else 0.0


def calculate_trend_analysis(
    data_points: List[Dict[str, Any]],
    metric: str = "value",
) -> Dict[str, Any]:
    """Analyze trend in time-series data.

    Args:
        data_points: List of data points with timestamps and values
        metric: The metric field to analyze

    Returns:
        Trend analysis dict with direction, change_pct, etc.
    """
    if len(data_points) < 2:
        return {
            "direction": "stable",
            "change_pct": 0.0,
            "data_points": len(data_points),
        }

    # Sort by date (oldest first for analysis)
    sorted_points = sorted(data_points, key=lambda x: x.get("date", ""))

    first_value = sorted_points[0].get(metric, 0)
    last_value = sorted_points[-1].get(metric, 0)

    if first_value == 0:
        change_pct = 0.0
    else:
        change_pct = ((last_value - first_value) / first_value) * 100

    if abs(change_pct) < 5:
        direction = "stable"
    elif change_pct > 0:
        direction = "improving"
    else:
        direction = "declining"

    return {
        "direction": direction,
        "change_pct": round(change_pct, 1),
        "first_value": first_value,
        "last_value": last_value,
        "data_points": len(data_points),
    }


def format_analytics_value(
    value: float,
    metric_type: str = "score",
) -> str:
    """Format analytics value for display.

    Args:
        value: The numeric value
        metric_type: Type of metric ('score', 'percentage', 'count')

    Returns:
        Formatted string
    """
    if metric_type == "percentage":
        return f"{value:.1f}%"
    elif metric_type == "score":
        return f"{value:.0f}"
    elif metric_type == "count":
        return f"{int(value):,}"
    else:
        return f"{value:.2f}"
