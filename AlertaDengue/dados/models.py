from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    """Read-only mapping for cities."""

    geocode = models.IntegerField(
        db_column="geocodigo",
        primary_key=True,
        help_text=_("Código do Município"),
    )
    name = models.CharField(
        db_column="nome",
        max_length=128,
        help_text=_("Nome do município"),
    )
    state = models.CharField(
        db_column="uf",
        max_length=20,
        help_text=_("Nome do estado"),
    )
    id_regional = models.IntegerField(
        db_column="id_regional",
        help_text=_("Geocódigo da Regional de Saúde"),
    )
    regional = models.CharField(
        db_column="regional",
        max_length=128,
        help_text=_("Nome da Regional de Saúde"),
    )
    macroregional_id = models.IntegerField(
        db_column="macroregional_id",
        help_text=_("Geocódigo da Macroregional de Saúde"),
    )
    macroregional = models.CharField(
        db_column="macroregional",
        max_length=128,
        help_text=_("Nome da Macroregional de Saúde"),
    )

    class Meta:
        db_table = '"Dengue_global"."Municipio"'
        app_label = "dados"
        managed = False
        verbose_name = "city"
        verbose_name_plural = "cities"

    def __str__(self) -> str:
        """Return the city name."""
        return self.name


class CID10(models.Model):
    """Read-only mapping for CID10 codes."""

    code = models.CharField(
        db_column="codigo",
        primary_key=True,
        max_length=512,
        help_text=_("Código da doença"),
    )
    name = models.CharField(
        db_column="nome",
        max_length=512,
        help_text=_("Nome da doença"),
    )

    class Meta:
        db_table = '"Dengue_global"."CID10"'
        app_label = "dados"
        managed = False
        verbose_name = "CID10"
        verbose_name_plural = "CID10 codes"

    def __str__(self) -> str:
        """Return the disease name."""
        return self.name


class ParameterUF(models.Model):
    """UF-level epidemic thresholds by disease."""

    pk = models.CompositePrimaryKey("state_code", "cid10")

    state_code = models.IntegerField(
        db_column="state_code",
        help_text=_("Código numérico do estado"),
    )
    state_abbr = models.CharField(
        db_column="state_abbr",
        max_length=2,
        help_text=_("Sigla do estado"),
    )
    state_name = models.TextField(
        db_column="state_name",
        help_text=_("Nome do estado"),
    )
    cid10 = models.CharField(
        db_column="cid10",
        max_length=16,
        help_text=_("Código CID10 da doença"),
    )
    limiar_preseason = models.FloatField(
        db_column="limiar_preseason",
        null=True,
        blank=True,
        help_text=_("Limiar de pré-sazonalidade"),
    )
    limiar_posseason = models.FloatField(
        db_column="limiar_posseason",
        null=True,
        blank=True,
        help_text=_("Limiar de pós-sazonalidade"),
    )
    limiar_epidemico = models.FloatField(
        db_column="limiar_epidemico",
        null=True,
        blank=True,
        help_text=_("Limiar epidêmico"),
    )

    class Meta:
        db_table = '"Dengue_global"."parameters_uf"'
        app_label = "dados"
        verbose_name = "UF parameter"
        verbose_name_plural = "UF parameters"
        indexes = [
            models.Index(
                fields=["state_code"],
                name="parameters_uf_idx_state_code",
            )
        ]

    def __str__(self) -> str:
        """Return a readable UF/disease identifier."""
        return f"{self.state_abbr} - {self.cid10}"


class HomeUfHistoryBase(models.Model):
    """Read-only UF/city history rows used by the home state charts."""

    pk = models.CompositePrimaryKey("state_abbr", "geocode", "epiweek")

    state_abbr = models.CharField(
        db_column="state_abbv",
        max_length=2,
        help_text=_("Sigla do estado"),
    )
    state_name = models.CharField(
        db_column="state_name",
        max_length=128,
        help_text=_("Nome do estado"),
    )
    geocode = models.IntegerField(
        db_column="municipio_geocodigo",
        help_text=_("Código do município"),
    )
    epiweek = models.IntegerField(
        db_column="SE",
        help_text=_("Semana epidemiológica no formato AAAASS"),
    )
    epiweek_start = models.DateField(
        db_column="data_iniSE",
        help_text=_("Data inicial da semana epidemiológica"),
    )
    estimated_cases = models.FloatField(
        db_column="casos_est",
        null=True,
        blank=True,
        help_text=_("Casos estimados"),
    )
    cases = models.IntegerField(
        db_column="casos",
        null=True,
        blank=True,
        help_text=_("Casos notificados"),
    )
    alert_level = models.SmallIntegerField(
        db_column="nivel",
        null=True,
        blank=True,
        help_text=_("Nível de alerta"),
    )
    receptive = models.SmallIntegerField(
        db_column="receptivo",
        null=True,
        blank=True,
        help_text=_("Indicador de receptividade climática"),
    )

    class Meta:
        abstract = True
        app_label = "dados"
        managed = False

    def __str__(self) -> str:
        """Return a readable UF/city/week identifier."""
        return f"{self.state_abbr} {self.geocode} {self.epiweek}"


class HomeUfHistoryDengue(HomeUfHistoryBase):
    """Read-only mapping for public.hist_uf_dengue_materialized_view."""

    class Meta(HomeUfHistoryBase.Meta):
        db_table = "hist_uf_dengue_materialized_view"
        verbose_name = "home UF dengue history"
        verbose_name_plural = "home UF dengue history"
        indexes = [
            models.Index(fields=["state_abbr"], name="home_duf_state_idx"),
            models.Index(fields=["geocode"], name="home_duf_geocode_idx"),
        ]


class HomeUfHistoryChikungunya(HomeUfHistoryBase):
    """Read-only mapping for public.hist_uf_chik_materialized_view."""

    class Meta(HomeUfHistoryBase.Meta):
        db_table = "hist_uf_chik_materialized_view"
        verbose_name = "home UF chikungunya history"
        verbose_name_plural = "home UF chikungunya history"
        indexes = [
            models.Index(fields=["state_abbr"], name="home_cuf_state_idx"),
            models.Index(fields=["geocode"], name="home_cuf_geocode_idx"),
        ]


class HomeUfHistoryZika(HomeUfHistoryBase):
    """Read-only mapping for public.hist_uf_zika_materialized_view."""

    class Meta(HomeUfHistoryBase.Meta):
        db_table = "hist_uf_zika_materialized_view"
        verbose_name = "home UF zika history"
        verbose_name_plural = "home UF zika history"
        indexes = [
            models.Index(fields=["state_abbr"], name="home_zuf_state_idx"),
            models.Index(fields=["geocode"], name="home_zuf_geocode_idx"),
        ]


class HomeCityCountByUfBase(models.Model):
    """Read-only city counts used by home chart metadata."""

    pk = models.CompositePrimaryKey("state_name", "disease")

    state_name = models.CharField(
        db_column="uf",
        max_length=128,
        help_text=_("Nome do estado"),
    )
    disease = models.CharField(
        db_column="disease",
        max_length=32,
        help_text=_("Doença"),
    )
    city_count = models.IntegerField(
        db_column="city_count",
        help_text=_("Número de municípios monitorados"),
    )

    class Meta:
        abstract = True
        app_label = "dados"
        managed = False

    def __str__(self) -> str:
        """Return a readable UF/disease count."""
        return f"{self.state_name} - {self.disease}: {self.city_count}"


class HomeCityCountByUfDengue(HomeCityCountByUfBase):
    """Read-only mapping for public.city_count_by_uf_dengue_materialized_view."""

    class Meta(HomeCityCountByUfBase.Meta):
        db_table = "city_count_by_uf_dengue_materialized_view"
        verbose_name = "home dengue city count by UF"
        verbose_name_plural = "home dengue city counts by UF"
        indexes = [
            models.Index(fields=["state_name"], name="home_dcnt_uf_idx")
        ]


class HomeCityCountByUfChikungunya(HomeCityCountByUfBase):
    """Read-only mapping for chikungunya city-count materialized view."""

    class Meta(HomeCityCountByUfBase.Meta):
        db_table = "city_count_by_uf_chikungunya_materialized_view"
        verbose_name = "home chikungunya city count by UF"
        verbose_name_plural = "home chikungunya city counts by UF"
        indexes = [
            models.Index(fields=["state_name"], name="home_ccnt_uf_idx")
        ]


class HomeCityCountByUfZika(HomeCityCountByUfBase):
    """Read-only mapping for public.city_count_by_uf_zika_materialized_view."""

    class Meta(HomeCityCountByUfBase.Meta):
        db_table = "city_count_by_uf_zika_materialized_view"
        verbose_name = "home zika city count by UF"
        verbose_name_plural = "home zika city counts by UF"
        indexes = [
            models.Index(fields=["state_name"], name="home_zcnt_uf_idx")
        ]
