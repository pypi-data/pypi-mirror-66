import datetime

from pytz import timezone as pytz_timezone
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db.models import PointField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.geos import Point
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base


class SamplingEventDevice(base.IrekuaModelBaseUser):
    sampling_event = models.ForeignKey(
        'SamplingEvent',
        on_delete=models.PROTECT,
        db_column='sampling_event_id',
        verbose_name=_('sampling event'),
        help_text=_('Sampling event in which this device was deployed'),
        blank=False,
        null=False)

    deployed_on = models.DateTimeField(
        db_column='deployed_on',
        verbose_name=_('deployed on'),
        help_text=_('Date at which the device started capturing information.'),
        blank=True,
        null=True)
    recovered_on = models.DateTimeField(
        db_column='recovered_on',
        verbose_name=_('recovered on'),
        help_text=_('Date at which the device stoped capturing information.'),
        blank=True,
        null=True)

    geo_ref = PointField(
        blank=True,
        null=True,
        db_column='geo_ref',
        verbose_name=_('geo ref'),
        help_text=_('Georeference of deployed device as Geometry'),
        spatial_index=True)
    latitude = models.FloatField(
        db_column='latitude',
        verbose_name=_('latitude'),
        help_text=_('Latitude of deployed device (in decimal degrees)'),
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True,
        blank=True)
    longitude = models.FloatField(
        db_column='longitude',
        verbose_name=_('longitude'),
        help_text=_('Longitude of deployed device (in decimal degrees)'),
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True,
        blank=True)
    altitude = models.FloatField(
        blank=True,
        db_column='altitude',
        verbose_name=_('altitude'),
        help_text=_('Altitude of deployed device (in meters)'),
        null=True)

    collection_device = models.ForeignKey(
        'CollectionDevice',
        db_column='collection_device_id',
        verbose_name=_('collection device'),
        help_text=_('Reference to collection device used on sampling event'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Sampling event commentaries'),
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to sampling event device'),
        default=empty_JSON,
        blank=True,
        null=True)
    configuration = JSONField(
        db_column='configuration',
        verbose_name=_('configuration'),
        default=empty_JSON,
        help_text=_('Configuration on device through the sampling event'),
        blank=True,
        null=True)
    licence = models.ForeignKey(
        'Licence',
        on_delete=models.PROTECT,
        db_column='licence_id',
        verbose_name=_('licence'),
        help_text=_('Licence for all items in sampling event'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Sampling Event Device')
        verbose_name_plural = _('Sampling Event Devices')

        unique_together = (
            ('sampling_event', 'collection_device'),
        )

        ordering = ['-created_on']

    def __str__(self):
        msg = _('{} (deployed)')
        msg = msg.format(self.collection_device.internal_id)
        return msg

    def validate_licence(self):
        if self.licence is not None:
            self.licence = self.sampling_event.licence

        if self.licence is not None:
            collection = self.sampling_event.collection
            collection.validate_and_get_licence(self.licence)

    def validate_user(self):
        if self.created_by is None:
            self.created_by = self.sampling_event.created_by

        if self.created_by is None:
            return

    def validate_deployed_on(self):
        starting_date = self.sampling_event.started_on

        if not starting_date:
            return

        if not self.deployed_on:
            self.deployed_on = starting_date
            return

        if starting_date > self.deployed_on:
            message = _(
                "Deployment date cannot be earlier that sampling event starting date")
            raise ValidationError(message)

    def validate_recovered_on(self):
        ending_date = self.sampling_event.ended_on

        if not ending_date:
            return

        if not self.recovered_on:
            self.recovered_on = ending_date
            return

        if ending_date < self.recovered_on:
            message = _(
                "Recovery date cannot be latter that sampling event ending date")
            raise ValidationError(message)

    def get_best_date_estimate(self, datetime_info, time_zone):
        year = datetime_info.get('year', None)
        month = datetime_info.get('month', None)
        day = datetime_info.get('day', None)
        hour = datetime_info.get('hour', None)
        minute = datetime_info.get('minute', None)
        second = datetime_info.get('second', None)

        if day is None:
            day = self.deployed_on.day

        if month is None:
            month = self.deployed_on.month
            day = 1

        if year is None:
            if self.deployed_on.year != self.recovered_on.year:
                message = _(
                    'No year was provided for date estimation and couldn\'t'
                    ' be inferred from deployment.')
                raise ValidationError(message)

            year = self.deployed_on.year

        if second is None:
            second = self.deployed_on.second

        if minute is None:
            minute = self.deployed_on.minute
            second = self.deployed_on.second

        if hour is None:
            hour = self.deployed_on.hour
            minute = self.deployed_on.minute
            second = self.deployed_on.second

        return datetime.datetime(year, month, day, hour, minute, second, 0, time_zone)

    def get_timezone(self, time_zone=None):
        if time_zone is None:
            time_zone = self.sampling_event.collection_site.site.timezone

        return pytz_timezone(time_zone)

    def validate_date(self, date_info):
        time_zone = self.get_timezone(time_zone=date_info.get('time_zone', None))
        hdate = self.get_best_date_estimate(date_info, time_zone)
        hdate_up = self.recovered_on.astimezone(time_zone)
        hdate_down = self.deployed_on.astimezone(time_zone)

        if hdate < hdate_down or hdate > hdate_up:
            mssg = _(
                'Date is not within the ranges in which the device was deployed: \n'
                'Deployment: {} \t Recovery: {} \t Date: {}').format(
                    hdate_down,
                    hdate_up,
                    hdate)
            raise ValidationError(mssg)

    def sync_coordinates_and_georef(self):
        if self.latitude is not None and self.longitude is not None:
            self.geo_ref = Point([self.longitude, self.latitude])
            return

        if self.geo_ref:
            self.latitude = self.geo_ref.y
            self.longitude = self.geo_ref.x
            return

        msg = _('Geo reference or longitude-latitude must be provided')
        raise ValidationError({'geo_ref': msg})

    def save(self, *args, **kwargs):
        if self.deployed_on is None:
            self.deployed_on = self.sampling_event.started_on

        if self.recovered_on is None:
            self.recovered_on = self.sampling_event.ended_on

        return super().save(*args, **kwargs)

    def clean(self):
        self.sync_coordinates_and_georef()

        try:
            self.validate_licence()
        except ValidationError as error:
            raise ValidationError({'licence': error})

        try:
            sampling_event_type = self.sampling_event.sampling_event_type
            device_type = self.collection_device.physical_device.device.device_type

            sampling_event_device_type = (
                sampling_event_type.validate_and_get_device_type(
                    device_type))
        except ValidationError as error:
            raise ValidationError({'physical_device': error})

        if sampling_event_device_type is not None:
            try:
                sampling_event_device_type.validate_metadata(self.metadata)
            except ValidationError as error:
                raise ValidationError({'metadata': error})

        try:
            self.validate_deployed_on()
        except ValidationError as error:
            raise ValidationError({'deployed_on': error})

        try:
            self.validate_recovered_on()
        except ValidationError as error:
            raise ValidationError({'recovered_on': error})

        try:
            physical_device = self.collection_device.physical_device
            physical_device.validate_configuration(self.configuration)
        except ValidationError as error:
            raise ValidationError({'configuration': error})

        if self.licence is not None:
            collection = self.sampling_event.collection
            try:
                collection.validate_and_get_licence(self.licence)
            except ValidationError as error:
                raise ValidationError({'licence': error})

        super().clean()
