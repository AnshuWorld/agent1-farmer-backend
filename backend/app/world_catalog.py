"""Starter catalog for Earth-like resources and island animals.

This is game data, not a geologically accurate resource-generation model.
"""
from threading import Lock

RESOURCE_DEPOSITS = [
    {"id": "sand", "name": "Sand", "category": "sediment", "deposit_units": 1200, "uses": ["glass", "mortar", "construction"]},
    {"id": "gravel", "name": "Gravel", "category": "sediment", "deposit_units": 900, "uses": ["roads", "concrete", "drainage"]},
    {"id": "clay", "name": "Clay", "category": "mineral", "deposit_units": 700, "uses": ["bricks", "pottery"]},
    {"id": "stone", "name": "Stone", "category": "rock", "deposit_units": 1800, "uses": ["building", "tools"]},
    {"id": "limestone", "name": "Limestone", "category": "rock", "deposit_units": 650, "uses": ["cement", "lime"]},
    {"id": "quartz", "name": "Quartz", "category": "mineral", "deposit_units": 400, "uses": ["glass", "electronics"]},
    {"id": "iron_ore", "name": "Iron ore", "category": "metal_ore", "deposit_units": 800, "uses": ["iron", "steel"]},
    {"id": "copper_ore", "name": "Copper ore", "category": "metal_ore", "deposit_units": 350, "uses": ["copper", "wiring"]},
    {"id": "bauxite", "name": "Bauxite", "category": "metal_ore", "deposit_units": 500, "uses": ["aluminum"]},
    {"id": "gold_ore", "name": "Gold-bearing rock", "category": "metal_ore", "deposit_units": 90, "uses": ["gold", "trade"]},
    {"id": "silver_ore", "name": "Silver ore", "category": "metal_ore", "deposit_units": 75, "uses": ["silver", "electronics"]},
    {"id": "coal", "name": "Coal", "category": "fossil_fuel", "deposit_units": 600, "uses": ["energy", "industry"]},
    {"id": "crude_oil", "name": "Crude oil", "category": "fossil_fuel", "deposit_units": 450, "uses": ["fuel", "petrochemicals"]},
    {"id": "natural_gas", "name": "Natural gas", "category": "fossil_fuel", "deposit_units": 500, "uses": ["energy", "heating"]},
    {"id": "salt", "name": "Rock salt", "category": "mineral", "deposit_units": 220, "uses": ["food", "chemical industry"]},
    {"id": "sulfur", "name": "Sulfur", "category": "mineral", "deposit_units": 130, "uses": ["chemical industry"]},
    {"id": "gypsum", "name": "Gypsum", "category": "mineral", "deposit_units": 280, "uses": ["plaster", "drywall"]},
    {"id": "phosphate", "name": "Phosphate rock", "category": "mineral", "deposit_units": 160, "uses": ["fertilizer"]},
    {"id": "fresh_water", "name": "Fresh water", "category": "renewable_resource", "deposit_units": 2000, "uses": ["drinking", "irrigation"]},
    {"id": "timber", "name": "Timber", "category": "renewable_resource", "deposit_units": 300, "uses": ["construction", "tools"]},
]

ANIMALS = [
    {"species": "dog", "count": 2, "role": "companion; may later guard settlement", "products": []},
    {"species": "bird", "count": 7, "role": "wildlife; seed dispersal and ecosystem activity", "products": []},
    {"species": "cow", "count": 2, "role": "livestock", "products": ["milk", "manure"]},
]

_lock = Lock()
_milk_inventory_liters = 0.0


def collect_milk(hours: float = 1.0) -> dict:
    """Prototype yield; real production should depend on health, feed, age and lactation."""
    global _milk_inventory_liters
    with _lock:
        cows = next(a["count"] for a in ANIMALS if a["species"] == "cow")
        yield_liters = round(cows * 0.6 * max(0.0, min(hours, 12.0)), 2)
        _milk_inventory_liters = round(_milk_inventory_liters + yield_liters, 2)
        return {"collected_liters": yield_liters, "inventory_liters": _milk_inventory_liters,
                "note": "Illustrative prototype yield; feed, health, age and lactation are not modeled yet."}
