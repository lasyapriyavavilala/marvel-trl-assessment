"""
Universal taxonomy and configuration for TRL assessment system.
"""

# Universal 6-subsystem taxonomy (applies to ALL microreactors)
UNIVERSAL_TAXONOMY = {
    "reactor_core_fuel": {
        "name": "Reactor Core & Fuel Assembly",
        "description": "Fuel form, enrichment, cladding, core structure",
        "common_components": [
            "fuel_pins", "fuel_cladding", "core_support_structure",
            "reflector", "neutron_moderator", "fuel_assembly"
        ]
    },
    "heat_transport": {
        "name": "Heat Transport System",
        "description": "Primary coolant system, heat exchangers, thermal transfer",
        "common_components": [
            "primary_coolant", "heat_pipes", "heat_exchanger",
            "coolant_pumps", "piping_system", "thermal_interface"
        ]
    },
    "reactivity_control": {
        "name": "Reactivity Control System",
        "description": "Control rods, shutdown systems, reactivity management",
        "common_components": [
            "control_rods", "control_rod_drives", "shutdown_system",
            "burnable_poisons", "reactivity_mechanisms"
        ]
    },
    "decay_heat_removal": {
        "name": "Decay Heat Removal",
        "description": "Passive/active emergency cooling, residual heat removal",
        "common_components": [
            "passive_cooling", "emergency_cooling", "heat_sinks",
            "natural_circulation", "cavity_cooling"
        ]
    },
    "instrumentation_control": {
        "name": "Instrumentation & Control",
        "description": "Sensors, monitoring, digital I&C, safety systems",
        "common_components": [
            "neutron_detectors", "temperature_sensors", "pressure_sensors",
            "control_systems", "digital_ic", "safety_systems", "scada"
        ]
    },
    "structural_containment": {
        "name": "Structural Support & Containment",
        "description": "Reactor vessel, containment, shielding, structural support",
        "common_components": [
            "reactor_vessel", "containment_structure", "radiation_shielding",
            "structural_support", "seismic_isolation", "pressure_boundary"
        ]
    }
}

# Reactor-specific configurations
REACTOR_CONFIGS = {
    "MARVEL": {
        "full_name": "Microreactor Applications Research Validation and EvaLuation",
        "operator": "Idaho National Laboratory",
        "type": "heat_pipe_cooled",
        "fuel": "HALEU metallic",
        "coolant": "sodium",
        "power_thermal": "0.1 MWt",  # 100 kW thermal
        "first_criticality": "2023-03-31",
        "primary_purpose": "research",
        "key_features": [
            "sodium_heat_pipes",
            "metallic_haleu_fuel",
            "passive_cooling",
            "modular_design"
        ]
    },
    "KRONOS": {
        "full_name": "Kairos Mobile Microreactor",
        "operator": "Kairos Power",
        "type": "helium_cooled",
        "fuel": "TRISO in FCM matrix",
        "coolant": "helium",
        "power_thermal": "15 MWt",
        "power_electric": "5 MWe",
        "primary_purpose": "commercial",
        "key_features": [
            "triso_fuel",
            "prismatic_graphite_core",
            "helium_coolant",
            "molten_salt_storage"
        ]
    },
    "eVinci": {
        "full_name": "Westinghouse eVinci Microreactor",
        "operator": "Westinghouse Electric",
        "type": "heat_pipe_cooled",
        "fuel": "TRISO",
        "coolant": "sodium (heat pipes)",
        "power_thermal": "5 MWt",
        "power_electric": "1-5 MWe",
        "primary_purpose": "commercial_remote",
        "key_features": [
            "transportable",
            "heat_pipes",
            "triso_fuel",
            "autonomous_operation"
        ]
    }
}

# Dependency inference rules (helps Agent 1 propose edges)
DEPENDENCY_RULES = [
    {
        "from": "reactor_core_fuel",
        "to": "heat_transport",
        "type": "thermal_interface",
        "rationale": "Core generates heat that must be removed"
    },
    {
        "from": "reactivity_control",
        "to": "reactor_core_fuel",
        "type": "functional",
        "rationale": "Control system manages core reactivity"
    },
    {
        "from": "instrumentation_control",
        "to": "reactivity_control",
        "type": "informational",
        "rationale": "I&C monitors neutron flux to inform control actions"
    },
    {
        "from": "decay_heat_removal",
        "to": "heat_transport",
        "type": "safety_backup",
        "rationale": "DHR provides backup cooling if primary heat transport fails"
    },
    {
        "from": "structural_containment",
        "to": "reactor_core_fuel",
        "type": "structural",
        "rationale": "Vessel contains the core"
    }
]