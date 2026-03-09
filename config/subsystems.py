

"""
MARVEL subsystem definitions and TRL indicators
"""

MARVEL_SUBSYSTEMS = {
    "reactor_core_fuel": {
        "name": "Reactor Core & Fuel Assembly",
        "key_terms": ["metallic fuel", "HALEU", "fuel assembly", "reactor core", "U-Zr alloy"],
        "trl_indicators": {
            "TRL_8-9": ["first criticality", "core operational", "full power operation", "fuel performance data"],
            "TRL_6-7": ["fuel fabrication complete", "core assembly installed", "fuel loading", "integration complete"],
            "TRL_4-5": ["prototype fuel", "component testing", "fuel qualification", "design 90% complete"],
            "TRL_1-3": ["conceptual design", "feasibility study", "fuel concept", "preliminary analysis"]
        }
    },
    "heat_transport": {
        "name": "Heat Transport System (Heat Pipes)",
        "key_terms": ["heat pipe", "sodium heat pipe", "thermal management", "heat removal", "heat pipe array"],
        "trl_indicators": {
            "TRL_8-9": ["heat pipes operational", "thermal performance validated", "operational hours", "reliability data"],
            "TRL_6-7": ["heat pipe fabrication complete", "full-scale thermal testing", "system integration", "1000-hour test"],
            "TRL_4-5": ["prototype heat pipe", "thermal cycling", "startup testing", "component validation"],
            "TRL_1-3": ["heat pipe concept", "thermal analysis", "feasibility", "design study"]
        }
    },
    "reactivity_control": {
        "name": "Reactivity Control System",
        "key_terms": ["control drum", "shutdown rod", "reactivity control", "reflector control"],
        "trl_indicators": {
            "TRL_8-9": ["control system operational", "reactivity worth validated", "shutdown margin confirmed"],
            "TRL_6-7": ["control drums installed", "reactivity control integrated", "shutdown system tested"],
            "TRL_4-5": ["control drum prototype", "reactivity measurements", "mechanism testing"],
            "TRL_1-3": ["control concept", "reactivity control study", "neutronic analysis"]
        }
    },
    "decay_heat_removal": {
        "name": "Decay Heat Removal System",
        "key_terms": ["decay heat", "passive cooling", "natural circulation", "emergency cooling"],
        "trl_indicators": {
            "TRL_8-9": ["passive decay heat validated", "natural circulation confirmed", "safety system performance"],
            "TRL_6-7": ["passive system integrated", "decay heat demonstrated", "safety testing complete"],
            "TRL_4-5": ["passive cooling testing", "natural circulation validation", "transient analysis"],
            "TRL_1-3": ["passive safety concept", "decay heat study", "safety analysis"]
        }
    },
    "instrumentation_control": {
        "name": "Instrumentation & Control",
        "key_terms": ["I&C", "instrumentation", "control system", "sensors", "monitoring"],
        "trl_indicators": {
            "TRL_8-9": ["I&C operational", "sensor performance validated", "control system functioning"],
            "TRL_6-7": ["I&C 90% complete", "sensors installed", "control system integrated"],
            "TRL_4-5": ["I&C design in progress", "sensor testing", "control algorithm validation"],
            "TRL_1-3": ["I&C concept", "sensor selection", "control strategy"]
        }
    },
    "structural_containment": {
        "name": "Structural Support & Containment",
        "key_terms": ["guard vessel", "reactor vessel", "containment", "reflector support frame", "structural"],
        "trl_indicators": {
            "TRL_8-9": ["containment operational", "guard vessel performance", "structural integrity confirmed"],
            "TRL_6-7": ["guard vessel fabrication complete", "reactor vessel installed", "structural assembly complete"],
            "TRL_4-5": ["vessel design 90% complete", "structural component testing", "reflector support frame"],
            "TRL_1-3": ["containment concept", "structural design study", "vessel analysis"]
        }
    }
}

# Source mapping
SOURCE_MAPPING = {
    "TRL_8-9": {
        "sources": ["Google News", "INL operational reports", "NRC inspections"],
        "site_filters": ["site:inl.gov", "site:news.google.com", "site:nrc.gov"]
    },
    "TRL_6-7": {
        "sources": ["NRC ADAMS", "INL press releases", "DOE ARDP"],
        "site_filters": ["site:nrc.gov", "site:inl.gov", "site:energy.gov"]
    },
    "TRL_4-5": {
        "sources": ["OSTI.gov", "INL technical reports", "DOE newsletters"],
        "site_filters": ["site:osti.gov", "site:inl.gov"]
    },
    "TRL_1-3": {
        "sources": ["Google Scholar", "arXiv", "conference proceedings"],
        "site_filters": ["site:scholar.google.com", "site:arxiv.org"]
    }
}