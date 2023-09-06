schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$defs": {
        "DateRange": {
            "type": "object",
            "properties": {
                "date_debut": { "type": "string", "format": "date" },
                "date_fin": { "type": "string", "format": "date" }
            },
            "required": ["date_debut", "date_fin"]
        },
        "ClassInfo": {
            "type": "object",
            "properties": {
                "nb_eleves": { "type": "integer" },
                "cours_1": {
                    "$ref": "#/$defs/CourseInfo"
                },
                "cours_2":{
                    "$ref": "#/$defs/CourseInfo"
                }
            },
            "required": ["nb_eleves", "cours_1"]
        },
        "CourseInfo": {
            "type": "object",
            "properties": {
                "jour": { "type": "string" },
                "heure_debut": { "type": "string" },
                "heure_fin": { "type": "string" },
                "salle": { "type": "string" }
            },
            "required": ["jour", "heure_debut", "heure_fin", "salle"]
        }
    },
    "type": "object",
    "properties": {
        "infos_generales": {
            "type": "object",
            "properties": {
                "lundi_semaine_0": { "type": "string" },
                "vacances": {
                    "type": "object",
                    "properties": {
                        "automne": { "$ref": "#/$defs/DateRange" },
                        "noel": { "$ref": "#/$defs/DateRange" },
                        "carnaval": { "$ref": "#/$defs/DateRange" },
                        "paques": { "$ref": "#/$defs/DateRange" },
                        "ete": { "$ref": "#/$defs/DateRange" }
                    },
                    "required": ["automne", "noel", "carnaval", "paques", "ete"]
                },
                "jours_feries": {
                    "type": "object",
                    "properties": {
                        "toussaint": { "$ref": "#/$defs/DateRange" },
                        "immaculee_conception": { "$ref": "#/$defs/DateRange" },
                        "ascension": { "$ref": "#/$defs/DateRange" },
                        "pentecote": { "$ref": "#/$defs/DateRange" },
                        "fete-dieu": { "$ref": "#/$defs/DateRange" }
                    },
                    "required": ["toussaint", "immaculee_conception", "ascension", "pentecote", "fete-dieu"]
                }
            }
        },
        "classes": {
            "type": "object",
            "properties": {
                "gymnase": {
                    "type": "object",
                    "properties": {
                        "infos_generales": {
                            "type": "object",
                            "properties": {
                                "url_moodle": { "type": "string" },
                                "url_jupyterhub": { "type": "string" }
                            },
                            "required": ["url_moodle", "url_jupyterhub"]
                        },
                        "1gy": {
                            "type": "object",
                            "patternProperties": {
                                "^1gy\d{1,2}$": { "$ref": "#/$defs/ClassInfo" }
                            }
                        },
                        "2gy": {
                            "type": "object",
                            "patternProperties": {
                                "^2gy\d{1,2}$": { "$ref": "#/$defs/ClassInfo" }
                            }
                        }
                    }
                },
                "ecg": {
                    "type": "object",
                    "properties": {
                        "1ecg": {
                            "type": "object",
                            "patternProperties": {
                                "^1ecg\d{1,2}$": { "$ref": "#/$defs/ClassInfo" }
                            }
                        },
                        "2ecg": {
                            "type": "object",
                            "patternProperties": {
                                "^2ecg\d{1,2}$": { "$ref": "#/$defs/ClassInfo" }
                            }
                        }
                    }
                },
                "ec": {
                    "type": "object",
                    "patternProperties": {
                        "^2ec\d{1,2}$": { "$ref": "#/$defs/ClassInfo" }
                    }
                }
            }
        }
    }
}
