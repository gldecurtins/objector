from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from common.models import Team
from inventory.models import Objekt, Location
from maintenance.models import Work


class Command(BaseCommand):
    help = "Creates demo data"

    def handle(self, *args, **options):
        self.create_users()
        self.create_teams()
        self.create_locations()
        self.create_objekts()
        self.create_work()

    def create_users(self):
        User = get_user_model()
        # Objektor
        self.user_luca_objektor, created = User.objects.get_or_create(
            username="luca@objektor.local"
        )
        # Facility Management Frauenfeld Ltd
        self.user_mia_facility, created = User.objects.get_or_create(
            username="mia@facility-management.local"
        )
        self.user_noah_facility, created = User.objects.get_or_create(
            username="noah@facility-management.local"
        )
        # Best Janitors Zurich Ltd
        self.user_matteo_best, created = User.objects.get_or_create(
            username="matteo@best-janitors.local"
        )
        self.user_paul_best, created = User.objects.get_or_create(
            username="paul@best-janitors.local"
        )
        # Chimney sweepers Wallis Corp
        self.user_liam_chimney, created = User.objects.get_or_create(
            username="liam@chimney-sweepers.local"
        )

    def create_teams(self):
        # Facility Management Frauenfeld Ltd
        self.team_facility, created = Team.objects.get_or_create(
            name="Facility Management Frauenfeld Ltd",
            description="DEMO: We manage everything!",
            owner=self.user_luca_objektor,
        )
        group_facility = Group.objects.get(id=self.team_facility.pk)
        group_facility.user_set.add(self.user_mia_facility)
        group_facility.user_set.add(self.user_noah_facility)

        # Best Janitors Zurich Ltd
        self.team_best, created = Team.objects.get_or_create(
            name="Best Janitors Zurich Ltd",
            description="DEMO: We maintain your assets!",
            owner=self.user_luca_objektor,
        )
        group_best = Group.objects.get(id=self.team_best.pk)
        group_best.user_set.add(self.user_matteo_best)
        group_best.user_set.add(self.user_paul_best)

        # Chimney sweepers Wallis Corp
        self.team_chimney, created = Team.objects.get_or_create(
            name="Chimney sweepers Wallis Corp",
            description="DEMO: A clean chimney is a good chimney.",
            owner=self.user_luca_objektor,
        )
        group_chimney = Group.objects.get(id=self.team_chimney.pk)
        group_chimney.user_set.add(self.user_liam_chimney)

    def create_locations(self):
        self.location_restaurant_zurich, created = Location.objects.get_or_create(
            name="Restaurant Zürich",
            description="DEMO: Our cosy restaurant.",
            address="Rindermarkt 12\r\n8001 Zürich",
            latitude=47.37233,
            longitude=8.5446,
            owner=self.user_luca_objektor,
        )

        self.location_flat_winterthur, created = Location.objects.get_or_create(
            name="Flat Winterthur",
            description="DEMO: Old flat, new carpet.",
            address="Schmidgasse 3\r\n8400 Winterthur",
            latitude=47.49975,
            longitude=8.72725,
            owner=self.user_luca_objektor,
        )

        self.location_chalet_zermatt, created = Location.objects.get_or_create(
            name="Chalet Zermatt",
            description="DEMO: Nice view.",
            address="Riedstrasse 18\r\n3920 Zermatt",
            latitude=46.01778,
            longitude=7.74953,
            owner=self.user_luca_objektor,
        )

        self.location_business_frauenfeld, created = Location.objects.get_or_create(
            name="Business Frauenfeld",
            description="DEMO: Many customers walking by.",
            address="Waffenplatzstrasse 70\r\n8500 Frauenfeld",
            latitude=47.57212,
            longitude=8.90573,
            owner=self.user_luca_objektor,
        )

    def create_objekts(self):
        self.objekt_boiler_restaurant, created = Objekt.objects.get_or_create(
            name="Boiler 500L",
            description="DEMO: Big",
            location=self.location_restaurant_zurich,
            owner=self.user_luca_objektor,
            management_team=self.team_facility,
            maintenance_team=self.team_best,
        )
        self.objekt_aircon_restaurant, created = Objekt.objects.get_or_create(
            name="AirConditioner",
            description="DEMO: Requires frequent replacement of filter ABC.",
            location=self.location_restaurant_zurich,
            owner=self.user_luca_objektor,
            management_team=self.team_facility,
            maintenance_team=self.team_best,
        )
        self.objekt_gas_heater_flat, created = Objekt.objects.get_or_create(
            name="Gas heater",
            description="DEMO: Hot water provider, manual injection.",
            location=self.location_flat_winterthur,
            owner=self.user_luca_objektor,
            management_team=self.team_facility,
            maintenance_team=self.team_best,
        )
        self.objekt_fireplace_chalet, created = Objekt.objects.get_or_create(
            name="Fireplace",
            description="DEMO: Requires a pile of wood.",
            location=self.location_chalet_zermatt,
            owner=self.user_luca_objektor,
            management_team=self.team_facility,
            maintenance_team=self.team_chimney,
        )
        self.objekt_garden_chalet, created = Objekt.objects.get_or_create(
            name="Garden",
            description="DEMO: Gras hight 4cm.",
            location=self.location_chalet_zermatt,
            owner=self.user_luca_objektor,
        )
        self.objekt_solar_business, created = Objekt.objects.get_or_create(
            name="Solar system",
            description="DEMO: Solar panels, 1.5 kW",
            location=self.location_business_frauenfeld,
            owner=self.user_luca_objektor,
            management_team=self.team_facility,
            maintenance_team=self.team_best,
        )

    def create_work(self):
        self.work_descale_boiler, created = Work.objects.get_or_create(
            name="Descale boiler",
            description="DEMO: Use vinegar.",
            defaults={
                "objekt": self.objekt_boiler_restaurant,
                "due_at": timezone.now() + timezone.timedelta(days=100),
                "overdue_at": timezone.now() + timezone.timedelta(days=110),
            },
        )
        self.work_replace_filter_aircon, created = Work.objects.get_or_create(
            name="Replace filter",
            description="DEMO: Use the square one.",
            defaults={
                "objekt": self.objekt_aircon_restaurant,
                "due_at": timezone.now() + timezone.timedelta(days=90),
                "overdue_at": timezone.now() + timezone.timedelta(days=120),
            },
        )
        self.work_add_fragrance_aircon, created = Work.objects.get_or_create(
            name="Add fragrance",
            description="DEMO: Lavendel No 6.",
            defaults={
                "objekt": self.objekt_aircon_restaurant,
                "due_at": timezone.now() + timezone.timedelta(days=30),
                "overdue_at": timezone.now() + timezone.timedelta(days=40),
            },
        )
        self.work_service_gas_heater, created = Work.objects.get_or_create(
            name="Gas service",
            description="DEMO: Yearly device maintenance.",
            defaults={
                "objekt": self.objekt_gas_heater_flat,
                "due_at": timezone.now() + timezone.timedelta(days=200),
                "overdue_at": timezone.now() + timezone.timedelta(days=210),
            },
        )
        self.work_clean_chimney_fireplace, created = Work.objects.get_or_create(
            name="Clean chimney",
            description="DEMO: Clean the chimney, 15cm.",
            defaults={
                "objekt": self.objekt_fireplace_chalet,
                "due_at": timezone.now() + timezone.timedelta(days=250),
                "overdue_at": timezone.now() + timezone.timedelta(days=260),
            },
        )
        self.work_add_wood_fireplace, created = Work.objects.get_or_create(
            name="Add wood",
            description="DEMO: Add birch wood, 25cm.",
            defaults={
                "objekt": self.objekt_fireplace_chalet,
                "due_at": timezone.now() + timezone.timedelta(days=250),
                "overdue_at": timezone.now() + timezone.timedelta(days=260),
            },
        )
        self.work_remove_ash_fireplace, created = Work.objects.get_or_create(
            name="Remove ash",
            description="DEMO: Put into regular rubbish for now.",
            defaults={
                "objekt": self.objekt_fireplace_chalet,
                "due_at": timezone.now() + timezone.timedelta(days=250),
                "overdue_at": timezone.now() + timezone.timedelta(days=260),
            },
        )
        self.work_mow_grass_garden, created = Work.objects.get_or_create(
            name="Mow grass",
            description="DEMO: Charge batteries prior mowing.",
            defaults={
                "objekt": self.objekt_garden_chalet,
                "due_at": timezone.now() + timezone.timedelta(days=50),
                "overdue_at": timezone.now() + timezone.timedelta(days=75),
            },
        )
        self.work_remove_weed_garden, created = Work.objects.get_or_create(
            name="Remove weed",
            description="DEMO: Just the big ones.",
            defaults={
                "objekt": self.objekt_garden_chalet,
                "due_at": timezone.now() + timezone.timedelta(days=50),
                "overdue_at": timezone.now() + timezone.timedelta(days=75),
            },
        )
        self.work_clean_panels_solar, created = Work.objects.get_or_create(
            name="Clear solar panels",
            description="DEMO: Remove dust.",
            defaults={
                "objekt": self.objekt_solar_business,
                "due_at": timezone.now() + timezone.timedelta(days=120),
                "overdue_at": timezone.now() + timezone.timedelta(days=150),
            },
        )
        self.work_check_batteries_solar, created = Work.objects.get_or_create(
            name="Check batteries",
            description="DEMO: Check voltage and if there are any leaks.",
            defaults={
                "objekt": self.objekt_solar_business,
                "due_at": timezone.now() + timezone.timedelta(days=220),
                "overdue_at": timezone.now() + timezone.timedelta(days=250),
            },
        )
        self.work_check_panels_solar, created = Work.objects.get_or_create(
            name="Check panels",
            description="DEMO: Check for scratches and shadows falling on the panels.",
            defaults={
                "objekt": self.objekt_solar_business,
                "due_at": timezone.now() + timezone.timedelta(days=120),
                "overdue_at": timezone.now() + timezone.timedelta(days=150),
            },
        )
