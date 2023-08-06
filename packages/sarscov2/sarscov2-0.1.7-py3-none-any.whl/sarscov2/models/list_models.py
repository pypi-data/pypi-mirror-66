from edc_list_data.model_mixins import ListModelMixin


class CoronaKapInformationSources(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "KAP Information Sources"
        verbose_name_plural = "KAP Information Sources"
