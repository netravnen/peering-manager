# Generated by Django 2.2.1 on 2019-05-14 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("peering", "0044_auto_20190513_2153")]

    operations = [
        migrations.CreateModel(
            name="BGPGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=128)),
                ("slug", models.SlugField(unique=True)),
                ("comment", models.TextField(blank=True)),
                (
                    "communities",
                    models.ManyToManyField(blank=True, to="peering.Community"),
                ),
                (
                    "export_routing_policies",
                    models.ManyToManyField(
                        blank=True,
                        related_name="bgpgroup_export_routing_policies",
                        to="peering.RoutingPolicy",
                    ),
                ),
                (
                    "import_routing_policies",
                    models.ManyToManyField(
                        blank=True,
                        related_name="bgpgroup_import_routing_policies",
                        to="peering.RoutingPolicy",
                    ),
                ),
                (
                    "bgp_session_states_update",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("check_bgp_session_states", models.BooleanField(default=False)),
            ],
            options={"verbose_name": "BGP group", "ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="directpeeringsession",
            name="bgp_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="peering.BGPGroup",
                verbose_name="BGP Group",
            ),
        ),
        migrations.AddField(
            model_name="router",
            name="configuration_template",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="peering.ConfigurationTemplate",
            ),
        ),
        migrations.AlterModelOptions(
            name="router",
            options={
                "ordering": ["name"],
                "permissions": [
                    ("view_configuration", "Can view router's configuration"),
                    ("deploy_configuration", "Can deploy router's configuration"),
                ],
            },
        ),
    ]