from fastapi import APIRouter

from . import auth, me, uploads, meals, reports, recommendations, weights, barcodes, meal_plans, localization

router = APIRouter()
