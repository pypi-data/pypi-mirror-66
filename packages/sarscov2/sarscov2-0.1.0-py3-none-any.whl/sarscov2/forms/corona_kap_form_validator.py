from edc_form_validators.form_validator import FormValidator


class CoronaKapFormValidator(FormValidator):
    def clean(self):
        self.validate_other_specify(field="employment")
        self.validate_other_specify(field="health_insurance")
        self.validate_other_specify(
            field="known_other_symptoms", other_specify_field="symptoms_other"
        )
