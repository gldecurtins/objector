import json
from secrets import compare_digest
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from rules.contrib.views import AutoPermissionRequiredMixin
from .models import Location, Object, Sensor
from maintenance.models import Task, Trigger, Document
from .forms import ObjectForm, SensorForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin
from jsonpath_ng import parse
from .filters import LocationFilter, ObjectFilter, SensorFilter
from django_filters.views import FilterView


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        queryset = (
            Location.objects.filter(owner=self.request.user)
            | Location.objects.filter(management_group__in=groups_as_list)
            | Location.objects.filter(maintenance_group__in=groups_as_list)
        )
        filterset = LocationFilter(self.request.GET, queryset=queryset)
        return filterset.qs

    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        filterset = LocationFilter(self.request.GET, queryset=self.queryset)
        context["filter"] = filterset
        return context


class LocationCreateView(AutoPermissionRequiredMixin, CreateView):
    model = Location
    fields = [
        "name",
        "description",
        "address",
        "latitude",
        "longitude",
        "owner",
        "management_group",
        "maintenance_group",
    ]

    def get_initial(self) -> dict:
        initial = {}
        initial["owner"] = self.request.user.id
        initial["management_group"] = int(
            self.request.GET.get("management_group", False)
        )
        initial["maintenance_group"] = int(
            self.request.GET.get("maintenance_group", False)
        )
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class LocationDetailView(AutoPermissionRequiredMixin, DetailView):
    model = Location
    raise_exception = True

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        object_queryset = (
            Object.objects.filter(owner=self.request.user)
            | Object.objects.filter(management_group__in=groups_as_list)
            | Object.objects.filter(maintenance_group__in=groups_as_list)
        )
        context["object_list"] = object_queryset
        return context


class LocationUpdateView(AutoPermissionRequiredMixin, UpdateView):
    model = Location
    raise_exception = True
    fields = [
        "name",
        "description",
        "image",
        "address",
        "latitude",
        "longitude",
        "owner",
        "management_group",
        "maintenance_group",
    ]

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class LocationDeleteView(AutoPermissionRequiredMixin, DeleteView):
    model = Location
    raise_exception = True
    success_url = reverse_lazy("inventory:location-list")


class ObjectFilterView(LoginRequiredMixin, FilterView):
    model = Object
    filterset_class = ObjectFilter
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        queryset = (
            Object.objects.filter(owner=self.request.user)
            | Object.objects.filter(management_group__in=groups_as_list)
            | Object.objects.filter(maintenance_group__in=groups_as_list)
        )
        return queryset


class ObjectCreateView(AutoPermissionRequiredMixin, CreateView):
    model = Object
    form_class = ObjectForm

    def get_initial(self) -> dict:
        initial = {}
        initial["owner"] = self.request.user.id
        initial["location"] = int(self.request.GET.get("location", False))
        initial["management_group"] = int(
            self.request.GET.get("management_group", False)
        )
        initial["maintenance_group"] = int(
            self.request.GET.get("maintenance_group", False)
        )
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ObjectDetailView(AutoPermissionRequiredMixin, DetailView):
    model = Object
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_list"] = Task.objects.filter(object=self.object.id)
        context["sensor_list"] = Sensor.objects.filter(object=self.object.id)
        context["document_list"] = Document.objects.filter(object=self.object.id)
        return context


class ObjectUpdateView(AutoPermissionRequiredMixin, UpdateView):
    model = Object
    raise_exception = True
    form_class = ObjectForm

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ObjectDeleteView(AutoPermissionRequiredMixin, DeleteView):
    model = Object
    raise_exception = True
    success_url = reverse_lazy("inventory:object-list")


class SensorFilterView(LoginRequiredMixin, FilterView):
    model = Sensor
    filterset_class = SensorFilter
    paginate_by = 10

    def get_queryset(self):
        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        queryset = (
            Sensor.objects.filter(object__owner=self.request.user)
            | Sensor.objects.filter(object__management_group__in=groups_as_list)
            | Sensor.objects.filter(object__maintenance_group__in=groups_as_list)
        )
        return queryset


class SensorCreateView(AutoPermissionRequiredMixin, CreateView):
    model = Sensor
    form_class = SensorForm

    def get_initial(self) -> dict:
        initial = {}
        initial["owner"] = self.request.user.id
        initial["object"] = int(self.request.GET.get("object", False))
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SensorDetailView(AutoPermissionRequiredMixin, DetailView):
    model = Sensor
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trigger_list"] = Trigger.objects.filter(sensor=self.object.id)
        return context


class SensorUpdateView(AutoPermissionRequiredMixin, UpdateView):
    model = Sensor
    raise_exception = True
    fields = [
        "object",
        "name",
        "description",
        "image",
        "webhook_authorization",
        "webhook_payload",
        "status",
    ]

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SensorDeleteView(AutoPermissionRequiredMixin, DeleteView):
    model = Sensor
    raise_exception = True
    success_url = reverse_lazy("inventory:location-list")


@method_decorator(csrf_exempt, name="dispatch")
class SensorWebhookView(SingleObjectMixin, View):
    model = Sensor

    def post(self, request, *args, **kwargs):
        header_authorization = request.headers.get("Authorization", False)
        if not header_authorization:
            return HttpResponseForbidden(
                "Authorization not found in header.",
                content_type="text/plain",
            )

        self.object = self.get_object()
        webhook_authorization = self.object.webhook_authorization

        if not webhook_authorization:
            return HttpResponseForbidden(
                "No webhook authorization value specified on sensor.",
                content_type="text/plain",
            )

        if not compare_digest(webhook_authorization, header_authorization):
            return HttpResponseForbidden(
                "Incorrect Authorization value.",
                content_type="text/plain",
            )

        try:
            self.object.webhook_payload = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest(
                "Message contains invalid JSON.", content_type="text/plain"
            )

        self.object.status = self.get_sensor_status()
        self.object.save()
        return HttpResponse("Webhook payload saved.", content_type="text/plain")

    def get_trigger_sensor_value(
        self, match_value, trigger_condition, trigger_value
    ) -> str:
        trigger_sensor_value = ""

        if match_value and trigger_condition and trigger_value:
            try:
                type_matched_trigger_value = type(match_value)(trigger_value)
            except ValueError:
                trigger_sensor_value = "Error: Type mismatch. Matched value can't be compared to trigger value."
                return trigger_sensor_value

            if len(str(match_value)) > 200:
                trigger_sensor_value = (
                    "Error: Sensor value to long. Check JSONPath expression."
                )
                return trigger_sensor_value

            elif (
                (
                    Trigger.Conditions.EQUALS == trigger_condition
                    and match_value == type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.NOTEQUALS == trigger_condition
                    and match_value != type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.LESSTHAN == trigger_condition
                    and match_value < type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.LESSTHANOREQUALTO == trigger_condition
                    and match_value <= type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.GREATERTHAN == trigger_condition
                    and match_value > type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.GREATERTHANOREQUALTO == trigger_condition
                    and match_value >= type_matched_trigger_value
                )
            ):
                trigger_sensor_value = str(match_value)

        return trigger_sensor_value

    def get_sensor_status(self) -> int:
        sensor_status = Sensor.Statuses.GREEN
        triggers = Trigger.objects.filter(sensor=self.object.id)

        for trigger in triggers:
            trigger_status = Trigger.Statuses.GREEN
            trigger_sensor_value = ""
            jsonpath_expression = parse(trigger.jsonpath_expression)

            for match in jsonpath_expression.find(self.object.webhook_payload):
                if trigger_status > Trigger.Statuses.RED:
                    trigger_sensor_value_red = ""
                    trigger_sensor_value_red = self.get_trigger_sensor_value(
                        match.value,
                        trigger.condition,
                        trigger.red_value,
                    )
                    if trigger_sensor_value_red:
                        trigger_sensor_value = trigger_sensor_value_red
                        trigger_status = Trigger.Statuses.RED

                if trigger_status > Trigger.Statuses.AMBER:
                    trigger_sensor_value_amber = ""
                    trigger_sensor_value_amber = self.get_trigger_sensor_value(
                        match.value,
                        trigger.condition,
                        trigger.amber_value,
                    )
                    if trigger_sensor_value_amber:
                        trigger_sensor_value = trigger_sensor_value_amber
                        trigger_status = Trigger.Statuses.AMBER

                if trigger_status == Trigger.Statuses.GREEN:
                    trigger_sensor_value = match.value

            if sensor_status > trigger_status:
                sensor_status = trigger_status

            trigger.status = trigger_status
            trigger.sensor_value = trigger_sensor_value
            trigger.save()

        return sensor_status
