from edc_constants.constants import OTHER

EMPLOYMENT_STATUS = (
    ("working_for_pay", "Working for pay"),
    ("unemployed", "Unemployed"),
    ("not_working_for_pay", "Not working for pay (housewife, retired...)"),
)

PROFESSIONS = (
    ("professional", "Professional (e.g. office"),
    ("labourer", "Labourer"),
    ("housewife_retired", "Housewife, Retired"),
    ("self_employed", "Small business, self-employed"),
    (OTHER, "Other, specify below"),
)

EMPLOYMENT_LEVELS = (
    ("primary", "Up to primary"),
    ("secondary", "Up to high school"),
    ("tertiary", "University, college"),
    ("no_education", "No education"),
)

HEALTH_INSURANCE = (
    ("work_scheme", "Work scheme health insurance"),
    ("private", "Private health insurance"),
    ("no_insurance", "No insurance, I pay"),
    (OTHER, "Other, please specify below"),
)

HEALTH_OPINION = (
    ("excellent", "Excellent"),
    ("good", "Good"),
    ("fair", "Fair"),
    ("poor", "Poor"),
)

WORRY_SCALE = (
    ("very", "Very worried"),
    ("somewhat", "Somewhat worried"),
    ("a_little", "A little worried"),
    ("not_at_all", "Not worried at all"),
)

LIKELIHOOD_SCALE = (
    ("very", "Very likely"),
    ("somewhat", "Somewhat likely"),
    ("unlikely", "Not very likely, unlikely"),
    ("not_at_all", "Not at all"),
)
